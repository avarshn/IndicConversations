# IndicConversations - A Multilingual Wikipedia-Grounded Voice Chatbot
A multilingual, voice-enabled chatbot that retrieves grounded information from Wikipedia using a vector database and answers in multiple Indian languages via LLMs and translation APIs.

# 🚀 Getting Started

## Clone the repo
```bash
git clone https://github.com/avarshn/IndicConversations.git
cd IndicConversations
```

## Environment Setup (uv-managed)

This project uses **uv** for managing Python dependencies.

### 1. Install uv

Follow the official guide:
[https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

---

### 2. Set Up the Environment

```bash
uv sync
source .venv/bin/activate
```

This will:

* Create a virtual environment
* Install all required dependencies

---

## 🔑 Configure API Keys

Create a `.env` file and add your API keys/tokens as shown in `.env.example`.

```bash
cp .env.example .env
```
---

# ▶️ Running the Application

## Step 1: Create a Knowledge Base (Wikipedia Grounding)

Before launching the UI, you must build a knowledge base.

The script below:

* Performs a web search
* Fetches the top Wikipedia link
* Scrapes its content using Wikipedia API
* Saves it as a `.txt` file
* Chunks the text
* Stores embeddings in a vector database

```bash
mkdir db

# This step may take some time the first time it runs,
# as it also downloads and loads an embedding model from HuggingFace.
python src/tasks/task_1_2_data_collection_ingestion.py \
  --topic "Python language" \
  --collection_name "wikipedia_docs" \
  --uri "./db/wiki.db"
```

### Example Topics

```bash
python src/tasks/task_1_2_data_collection_ingestion.py --topic "Python language"
python src/tasks/task_1_2_data_collection_ingestion.py --topic "Artificial Intelligence"
python src/tasks/task_1_2_data_collection_ingestion.py --topic "Industrial Revolution"
```

You can run this multiple times for different topics to expand your knowledge base.

---

## Step 2: Launch the Streamlit UI

```bash
uv run streamlit run app.py -- --collection_name "wiki_docs" --uri "./db/wiki.db"
```

This launches an interactive **Streamlit UI** for multilingual voice conversations.

---

# Features

* Voice-based interaction
* Wikipedia-grounded responses
* Source citations
* Multilingual conversation
* Multilingual output

### Supported Languages

Input:

* Hindi
* Bengali
* Gujarati
* Kannada
* Malayalam
* Marathi
* Odia
* Punjabi
* Tamil
* Telugu
* English

Output:

* Hindi
* Bengali
* Marathi
* Telugu
* Tamil
* Punjabi

*(Easily extendable to more languages.)*

---

# How to Use the UI

1. Select your desired **output language**
2. Click **“Press to Speak”**
3. Speak your query
4. Click **“Stop”**
5. Wait for processing
6. The system retrieves relevant Wikipedia chunks and answers with sources
7. Continue the conversation in any supported language

---

# 🛠️ Tech Stack

### LLM

**Sarvam AI – Sarvam-M (24B parameters)**

* Multilingual
* Hybrid reasoning
* Open weights
* Text-only model

### Translation

**Sarvam AI Translation API**

* Modern-colloquial style
* Casual and direct
* Optimized for chatbots

### Chunk Embeddings

```
sentence-transformers/all-mpnet-base-v2
```

### Vector Database

**Milvus (by Zilliz)**

---

# Tasks Overview

All task scripts (Task 1 to Task 5) are located in:

src/tasks
---
## 🔹 Phase 1 — Data Ingestion  
*(Combines Task 1 & Task 2 — Web Scraping + Vector Database Creation)*

This phase handles:

- Web scraping  
- Wikipedia content extraction  
- Text chunking  
- Embedding generation  
- Vector database creation  

Run these tasks first to build your knowledge base before using the RAG pipeline.

---

## 🔹 Phase 2 — RAG Pipeline

Executed after data ingestion, this phase includes:

- Query processing  
- Retrieval from vector database  
- Grounded response generation using LLMs  
- Source attribution  

---

## 🎁 Bonus Task — UI Application

An interactive Streamlit-based UI that enables:

- Voice-based interaction  
- Multilingual conversation  
- Wikipedia-grounded responses  
- Real-time chatbot experience  

Run the UI after completing Phase 1 to interact with your knowledge base.

---

# Observations & Challenges

Look into implementation_report.pdf

---