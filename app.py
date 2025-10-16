from langchain_chroma.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

DIRECTORY_DB = "vectorStore"

prompt_template = """
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

def perguntar():
    q = input("Digite sua pergunta: ")

    db = Chroma(persist_directory=DIRECTORY_DB, embedding_function=OllamaEmbeddings(model="nomic-embed-text"))

    responses = db.similarity_search_with_relevance_scores(q, k=3)
    if len(responses) == 0 or responses[0][1] < 0.7:
        print("Desculpe, não consegui encontrar uma resposta adequada.")
        return
    responses_text = [r[0].page_content for r in responses]
    db_context = "\n\n----\n\n".join(responses_text)
    prompt = ChatPromptTemplate.from_template(prompt_template)
    prompt = prompt.invoke({"db_context": db_context, "pergunta": q})
    model = ChatOllama(model="granite3.3:8b", temperature=0.1 )
    print("Reposta da IA:\n", model.invoke(prompt))

perguntar()