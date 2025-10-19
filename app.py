from langchain_chroma.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from ollama import Client
from langchain_ollama import ChatOllama
import uvicorn


DIRECTORY_DB = "vectorStore"
OLLAMA_LLM_MODEL = "qwen3-coder:480b-cloud"
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"
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

app = FastAPI(title="Assistente de Treinamento IA", version="1.0")
server = Client()

class requestMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)

class responseMessage(BaseModel):
    response: str
    model: str = Field(..., example=OLLAMA_LLM_MODEL)

@app.post("/api")
async def chat(request: requestMessage):
    q = request.message
    db = Chroma(persist_directory=DIRECTORY_DB, embedding_function=OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL))

    responses = db.similarity_search_with_relevance_scores(q, k=3)
    if len(responses) == 0 or responses[0][1] < 0.7:
        raise HTTPException(status_code=404, detail="Desculpe, não consegui encontrar uma resposta adequada.")
    
    response = ""
    responses_text = [r[0].page_content for r in responses]
    db_context = "\n\n----\n\n".join(responses_text)
    prompt = PROMPT_TEMPLATE.format(db_context=db_context, pergunta=q)
    # prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    # prompt = prompt.invoke({"db_context": db_context, "pergunta": q})
    messages = [{"role": "user", "content": prompt}]
    response = "Reposta da IA:\n\n-------\n\n"
    for part in server.chat(model=OLLAMA_LLM_MODEL, messages=messages, stream=True, options={"temperature": 0.1}):
        response += part['message']['content']
    return responseMessage(response=response, model=OLLAMA_LLM_MODEL)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)