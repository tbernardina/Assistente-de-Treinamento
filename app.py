from typing import List, Tuple
import asyncio
import logging
from langchain_chroma.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from ollama import Client
import uvicorn

# Implementação de log para monitorar funcionamento do código
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("assistente-treinamento")

# 3 classes para padronização de configuração e envio e resposta da api
class Settings(BaseSettings):
    directory_db: str = "vectorStore"
    ollama_llm_model: str = "qwen3-coder:480b-cloud"
    ollama_embedding_model: str = "nomic-embed-text"
    similarity_threshold: float = 0.7
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    temperature: float = 0.1

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

app = FastAPI(title="Assistente de Treinamento IA", version="1.0")
server = Client()

class requestMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)

class responseMessage(BaseModel):
    response: str
    source_count: int
    model: str

@app.on_event("startup")
async def startup_event():
    logger.info("Inicializando cliente Ollama e Chroma (embedding)...")
    app.state.server = Client()
    app.state.embeddings = OllamaEmbeddings(model=settings.ollama_embedding_model)
    def _init_db():
        return Chroma(persist_directory=settings.directory_db, embedding_function=app.state.embeddings)
    app.state.db = _init_db()
    logger.info("Inicialização concluída.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Encerrando aplicação...")

async def _similarity_search(db: Chroma, query: str, k: int = 3) -> List[Tuple]:
    return await asyncio.to_thread(db.similarity_search_with_relevance_scores, query, k)

async def _stream_chat(server: Client, model: str, messages: List[dict], temperature: float) -> str:
    response = ""
    def _collect():
        partial = ""
        for part in server.chat(model=model, messages=messages, stream=True, options={"temperature": temperature}):
            try:
                partial += part['message']['content']
            except Exception:
                continue
        return partial
    response = await asyncio.to_thread(_collect)
    return response

PROMPT_TEMPLATE = """
Você é uma assistente virtual de treinamento corporativo da empresa. 
Seu papel é ajudar colaboradores a entender e aplicar corretamente os processos, políticas e treinamentos internos.

Baseie-se APENAS nas informações do contexto abaixo (que vêm dos documentos oficiais de treinamento da empresa).
Se a resposta não estiver no contexto, diga educadamente que não há informação disponível e sugira procurar o setor de Treinamento.

---------------------
CONTEXTOS RELEVANTES:
{db_context}
---------------------

PERGUNTA DO USUÁRIO:
{pergunta}

---------------------

Responda de forma clara, estruturada e profissional, priorizando a precisão das informações e a clareza das instruções.
Se possível, adicione passos numerados, exemplos ou observações úteis."""

@app.post("/api", response_model=responseMessage)
async def chat(request: requestMessage):
    q = request.message
    if not q:
        raise HTTPException(status_code=400, detail="Mensagem vazia.")
    db: Chroma = app.state.db
    server: Client = app.state.server
    
    try:
        responses = await _similarity_search(db, q, k=3)
    except Exception as e:
        logger.error("Erro ao buscar semântica no banco de vetores")
        raise HTTPException(status_code=500, detail="Erro interno ao consultar base de conhecimento.")
    
    if not responses:
        raise HTTPException(status_code=404, detail="Desculpe, não encontrei informações relevantes.")
    top_score = None
    try:
        top_score = responses[0][1]
    except Exception:
        top_score = None
    
    if top_score is None or top_score < settings.similarity_threshold:
        raise HTTPException(status_code=404, detail="Desculpe, não consegui encontrar uma resposta adequada.")
    
    responses_text = []
    for r in responses:
        try:
            doc = r[0]
            content = getattr(doc, 'page_content', None) or str(doc)
            responses_text.append(content)
        except Exception:
            continue

    db_context = "\n\n----\n\n".join(responses_text)
    prompt = PROMPT_TEMPLATE.format(db_context=db_context, pergunta=q)
    messages = [{"role": "user", "content": prompt}]

    try:
        answer = await _stream_chat(server, settings.ollama_llm_model, messages, settings.temperature)
    except Exception:
        logger.exception("Erro ao gerar resposta via LLM")
        raise HTTPException(status_code=500, detail="Erro ao gerar resposta da IA.")
    return responseMessage(response=answer, source_count=len(responses_text), model=settings.ollama_llm_model)

if __name__ == "__main__":
    uvicorn.run("app:app", host=settings.host, port=settings.port, reload=settings.reload)