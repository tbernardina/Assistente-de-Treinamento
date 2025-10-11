from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma.vectorstores import Chroma

PASTA_BASE = "PastaDocumentos"

def conn_db():
    # Faz toda a alimentação do banco de vetores
    docs = process_document()
    chunks = chunk_processing(docs)
    vetor_chunks(chunks)

def process_document():
    # Carrega documentos da pasta
    carrier = PyPDFDirectoryLoader(PASTA_BASE, glob="*.pdf")
    docs = carrier.load()
    return docs

def chunk_processing(docs):
    # Divide os documentos em pedaços menores de texto chamados chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True
    )

    chunks = splitter.split_documents(docs)
    return chunks

def vetor_chunks(chunks):
    # Utiliza da IA do Ollama para criar a vetorização dos chunks e guardar no ChromaDB
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma.from_documents(chunks, embeddings, persist_directory="vectorStore")
    print("Vetor criado com sucesso!")

conn_db()