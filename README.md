# Assistente de Treinamento Corporativo (FastAPI + Ollama + ChromaDB)

Aplicação que responde perguntas de colaboradores com base em documentos internos (PDFs). A arquitetura usa:
- Ollama para embeddings e geração de texto (modelo local).
- ChromaDB para armazenamento vetorial persistente.
- LangChain apenas para helpers (carregamento e split de documentos).
- FastAPI para expor uma API HTTP.

## Principais características
- Geração de base vetorial a partir de PDFs (script db.py).
- Consulta semântica com threshold de similaridade configurável.
- Resposta do LLM construída a partir dos trechos mais relevantes.
- Inicialização dos clientes (Ollama, Embeddings, Chroma) no evento startup do FastAPI.
- Logs básicos para diagnóstico.

## Estrutura do projeto
- app.py — API principal (FastAPI). Cria clientes no startup, realiza busca semântica e consulta o modelo em streaming.
- db.py — Constrói a base vetorial a partir dos PDFs em PastaDocumentos/ e salva em vectorStore/.
- PastaDocumentos/ — Coloque seus PDFs de treinamento aqui.
- vectorStore/ — Pasta onde o Chroma persiste o índice vetorial.
- requirements.txt — Dependências do projeto.

## Como funciona (resumo)
1. db.py carrega PDFs com PyPDFDirectoryLoader, divide em chunks e cria embeddings com `nomic-embed-text`. Persistência em `vectorStore/`.
2. app.py no startup cria:
   - app.state.server = Client() (Ollama client)
   - app.state.embeddings = OllamaEmbeddings(...)
   - app.state.db = Chroma(...) com persistência
3. Ao receber POST /api com JSON {"message": "..."}:
   - Realiza busca semântica (similarity_search_with_relevance_scores).
   - Verifica score do top-1 contra `similarity_threshold` (padrão 0.7).
   - Se aceitável, monta prompt com os trechos relevantes e envia ao modelo Ollama em streaming.
   - Retorna JSON com campos: response, source_count, model.

## Configuração e execução (Windows)
1. Criar ambiente e ativar:
   - python -m venv .venv
   - .venv\Scripts\Activate.ps1    (PowerShell)  
     ou  
     .venv\Scripts\activate.bat    (cmd)

2. Instalar dependências:
   - .venv\Scripts\python -m pip install -r requirements.txt

3. Baixar os modelos necessários no Ollama (exemplos usados no projeto):
   - ollama pull nomic-embed-text
   - ollama pull qwen3-coder:480b-cloud

4. Gerar a base vetorial (colocar PDFs em PastaDocumentos/):
   - .venv\Scripts\python db.py

5. Rodar a API:
   - .venv\Scripts\python app.py  
   ou com uvicorn:
   - .venv\Scripts\python -m uvicorn "app:app" --host 0.0.0.0 --port 8000 --reload

## Endpoint
POST /api
- Payload: JSON { "message": "<sua pergunta>" }
- Resposta (200):
  {
    "response": "<texto gerado pelo LLM>",
    "source_count": <número de trechos usados>,
    "model": "<nome do modelo usado>"
  }
- Possíveis códigos:
  - 400: mensagem vazia
  - 404: sem contexto relevante ou confiança insuficiente
  - 500: erro interno / geração da IA

Exemplo (curl / PowerShell):
```bash
curl -X POST http://localhost:8000/api -H "Content-Type: application/json" -d "{\"message\":\"Como proceder no processo X?\"}"
```

## Variáveis e ajustes
Parâmetros configuráveis via `.env` (usando pydantic-settings via Settings):
- directory_db (padrão: vectorStore)
- ollama_llm_model (padrão no projeto: qwen3-coder:480b-cloud)
- ollama_embedding_model (padrão: nomic-embed-text)
- similarity_threshold (float, padrão 0.7)
- host, port, reload, temperature

## Dicas e observações
- Verifique se o Ollama está rodando localmente e se os modelos foram baixados.
- Se o streaming do modelo não retornar conteúdo, registre (`logger.debug`) os chunks para inspecionar o formato e adaptar o extrator.
- Para ambientes de produção, desative `reload` e ajuste logs/monitoramento.

## Contato
Projeto: Assistente de Treinamento Corporativo — uso interno.  
Autor/Manutenção: Thiago Reis Dalla Bernardina (trdallabernardina@gmail.com).