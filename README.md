
# 🧠 Assistente de Treinamento Corporativo com IA (LangChain + Ollama + ChromaDB)

Este projeto implementa um **assistente virtual de treinamento corporativo**, capaz de responder perguntas de colaboradores com base em documentos internos da empresa (como manuais, políticas e procedimentos).  
A aplicação utiliza **LangChain**, **Ollama** e **ChromaDB** para criar uma base vetorial de conhecimento e responder de forma contextualizada e precisa.

---

## 🚀 Funcionalidades

- 📚 **Leitura automática de documentos PDF** da pasta `PastaDocumentos/`
- 🧩 **Divisão inteligente de textos** em *chunks* para melhor indexação
- 🧠 **Criação de embeddings** com modelo `nomic-embed-text` via Ollama
- 💾 **Armazenamento vetorial persistente** com **ChromaDB**
- 💬 **Chat interativo** com o modelo `qwen3:30b` para consultas contextuais
- ⚙️ **Filtragem por relevância** — evita respostas imprecisas (limite de confiança ≥ 0.7)
- 🔒 **Respostas seguras e profissionais**, sem extrapolar o contexto dos documentos

---

## 🧩 Estrutura do Projeto

```
📦 AssistenteTreinamentoIA/
├── app.py               # Script principal - interação com o usuário e respostas da IA
├── db.py                # Gera a base vetorial a partir dos PDFs
├── requirements.txt     # Dependências do projeto
├── PastaDocumentos/     # Diretório com os PDFs de treinamento
└── vectorStore/         # Base vetorial persistente (gerada automaticamente)
```

---

## ⚙️ Instalação e Configuração

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/tbernardina/assistente-treinamento-ia-dev.git
cd assistente-treinamento-ia-dev
```

### 2️⃣ Criar e ativar o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate       # Windows
```

### 3️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar o **Ollama**

Certifique-se de ter o [Ollama](https://ollama.com/) instalado e os modelos necessários disponíveis:

```bash
ollama pull nomic-embed-text
ollama pull qwen3:30b
```

---

## 🗂️ Preparando a Base de Conhecimento

1. Coloque todos os **arquivos PDF oficiais** de treinamento dentro da pasta:
   ```
   PastaDocumentos/
   ```

2. Execute o script `db.py` para gerar a base vetorial:

   ```bash
   python db.py
   ```

   Se tudo ocorrer bem, a mensagem **"Vetor criado com sucesso!"** será exibida e o diretório `vectorStore/` será criado.

---

## 💬 Utilizando o Assistente

Após gerar a base, execute o assistente interativo:

```bash
python app.py
```

O sistema pedirá uma pergunta:

```
Digite sua pergunta: 
```

E retornará uma resposta fundamentada nos documentos internos.  
Caso não encontre contexto suficiente, o assistente informará que não há resposta disponível e recomendará procurar o setor de Qualidade.

---

## 🧠 Tecnologias Principais

| Tecnologia                         | Função                                                  |
|------------------------------------|---------------------------------------------------------|
| **LangChain**                      | Orquestra fluxos de processamento e integração IA       |
| **Ollama**                         | Geração de embeddings e modelo de linguagem local       |
| **ChromaDB**                       | Banco vetorial persistente para armazenamento semântico |
| **PyPDFDirectoryLoader**           | Leitura e carregamento automático de documentos PDF     |
| **RecursiveCharacterTextSplitter** | Segmentação eficiente de textos longos                  |

---

## 🧰 Requisitos do Sistema

- Python 3.10 ou superior  
- Ollama instalado e configurado localmente  
- Recursos de hardware adequados (recomendado mínimo: 16 GB RAM)

---

## 🧑‍💻 Autor

**Thiago Reis Dalla Bernardina**  
📧 [trdallabernardina@gmail.com](mailto:trdallabernardina@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/thiago-reis-dalla-bernardina-6aa41b2b9/)  
💻 [GitHub](https://github.com/tbernardina)

---

## 📜 Licença

Este projeto é distribuído sob a licença **MIT** — sinta-se à vontade para usar, modificar e distribuir.
