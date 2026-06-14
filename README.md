# Sahzade AI — RAG Document Chat V5

## Overview

**Sahzade AI RAG Document Chat V5** is a small local Retrieval-Augmented Generation experiment.

In previous versions:

```text
V1 → LoRA fine-tuning experiment
V2 → Local FastAPI chat API
V3 → Browser-based chat UI
V4 → Feedback evaluator
```

V5 adds a simple document-based question answering system.

The goal of this project is to let the assistant answer questions by searching inside a local text document instead of relying only on the model’s general knowledge.

---

## Project Goal

The main goal of this project is to build a basic RAG pipeline that can:

* read a local TXT document
* split the document into smaller chunks
* create a simple searchable index
* retrieve the most relevant chunks for a user question
* select the best answer sentence from the retrieved chunks
* save RAG test results into an output file

This version focuses on understanding the core logic of RAG before adding advanced features like embeddings, PDF support, or LLM generation.

---

## What is RAG?

RAG means **Retrieval-Augmented Generation**.

Simple meaning:

```text
Search first, answer second.
```

The system first searches the document for relevant information.
Then it uses the retrieved text to answer the user’s question.

Basic flow:

```text
User question
    ↓
Search document chunks
    ↓
Retrieve relevant text
    ↓
Select answer from document
    ↓
Return answer
```

---

## Project Scope

This version includes:

* TXT document loading
* document chunking
* chunk overlap
* simple keyword-based vector index
* cosine similarity search
* top-k retrieval
* best sentence selection
* terminal-based RAG chat
* saved RAG results

This version does **not** include:

* PDF support
* real embedding models
* vector databases
* LLM-based answer generation
* FastAPI endpoint
* frontend integration
* source citations UI
* production deployment

These features can be added in future versions.

---

## Project Structure

```text
sahzade-ai-rag-document-chat-v5/
│
├── data/
│   ├── documents/
│   │   └── sample_document.txt
│   │
│   ├── chunks/
│   │   └── chunks.jsonl
│   │
│   └── index/
│       └── vector_index.json
│
├── src/
│   ├── config.py
│   ├── document_loader.py
│   ├── chunker.py
│   ├── retriever.py
│   └── rag_chat.py
│
├── scripts/
│   ├── build_index.sh
│   └── run_rag_chat.sh
│
├── tests/
│   └── test_questions.txt
│
├── outputs/
│   └── rag_results.txt
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Main Components

### `data/documents/sample_document.txt`

This is the source document used for RAG testing.

The document contains fictional Azerbaijani test information, such as:

```text
Gizli kod adı: Mavi Qapı
Test parolu: ALFA-27
Xüsusi test rəngi: tünd bənövşəyi
```

These details are intentionally fictional so the system must retrieve them from the document.

---

### `src/config.py`

Stores project paths and RAG settings.

Main values:

```python
DOCUMENT_PATH
CHUNKS_PATH
VECTOR_INDEX_PATH
RAG_RESULTS_PATH
CHUNK_SIZE
CHUNK_OVERLAP
TOP_K
```

Meaning:

| Setting             | Meaning                                    |
| ------------------- | ------------------------------------------ |
| `DOCUMENT_PATH`     | Path to the source TXT document            |
| `CHUNKS_PATH`       | Path where document chunks are saved       |
| `VECTOR_INDEX_PATH` | Path where the search index is saved       |
| `RAG_RESULTS_PATH`  | Path where RAG results are saved           |
| `CHUNK_SIZE`        | Size of each text chunk                    |
| `CHUNK_OVERLAP`     | Repeated text between chunks               |
| `TOP_K`             | Number of most relevant chunks to retrieve |

---

### `src/document_loader.py`

Loads the TXT document and prints a short preview.

Main purpose:

* check if the document exists
* read the document
* show character count
* show preview text

Run:

```bash
python3 src/document_loader.py
```

---

### `src/chunker.py`

Splits the document into smaller chunks.

Main purpose:

* read the source document
* split it into smaller text chunks
* add chunk IDs
* save chunks into `chunks.jsonl`

Example chunk output:

```json
{"chunk_id":1,"text":"Şahzadə Qülləsi Layihəsi daxili test sənədidir..."}
```

Run:

```bash
python3 src/chunker.py
```

---

### `src/retriever.py`

Creates a simple keyword-based vector index and retrieves relevant chunks.

Main steps:

```text
chunk text
    ↓
tokenize words
    ↓
create word-count vector
    ↓
save searchable index
```

Example:

```text
Chunk text:
Layihənin test parolu ALFA-27-dir.
```

Vector:

```json
{
  "layihənin": 1,
  "test": 1,
  "parolu": 1,
  "alfa-27-dir": 1
}
```

When the user asks:

```text
Layihənin test parolu nədir?
```

The retriever compares the question vector with chunk vectors and returns the most relevant chunks.

Run:

```bash
python3 src/retriever.py
```

---

### `src/rag_chat.py`

Runs the terminal-based RAG question answering system.

Main purpose:

* receive a user question
* retrieve top relevant chunks
* split retrieved chunks into sentences
* score each sentence against the question
* return the best answer sentence
* save results into `outputs/rag_results.txt`

Run:

```bash
python3 src/rag_chat.py
```

---

## How It Works

Main pipeline:

```text
sample_document.txt
    ↓
document_loader.py
    ↓
chunker.py
    ↓
chunks.jsonl
    ↓
retriever.py
    ↓
vector_index.json
    ↓
rag_chat.py
    ↓
retrieved chunks
    ↓
best answer sentence
    ↓
rag_results.txt
```

---

## Important Concepts

### Chunk

A chunk is a small part of the document.

Example:

```text
Layihənin test parolu ALFA-27-dir.
```

Large documents are split into chunks so the system can search smaller parts more easily.

---

### Chunk Size

`CHUNK_SIZE` controls how large each chunk is.

Example:

```python
CHUNK_SIZE = 450
```

This means each chunk is about 450 characters.

---

### Chunk Overlap

`CHUNK_OVERLAP` creates repeated text between chunks.

Example:

```python
CHUNK_OVERLAP = 80
```

This helps prevent important information from being lost between two chunks.

---

### TOP_K

`TOP_K` controls how many relevant chunks are retrieved.

Example:

```python
TOP_K = 3
```

This means the system returns the top 3 most relevant chunks for each question.

---

## How to Run

### 1. Load document preview

```bash
python3 src/document_loader.py
```

---

### 2. Create chunks

```bash
python3 src/chunker.py
```

Output:

```text
data/chunks/chunks.jsonl
```

---

### 3. Build vector index

```bash
python3 src/retriever.py
```

Output:

```text
data/index/vector_index.json
```

---

### 4. Run RAG chat

```bash
python3 src/rag_chat.py
```

You can also run the script:

```bash
./scripts/run_rag_chat.sh
```

---

## Test Questions

Example test questions:

```text
Layihənin test parolu nədir?
Şahzadə Qülləsinin gizli kod adı nədir?
Layihənin xüsusi test rəngi nədir?
Layihədə neçə əsas modul var?
```

---

## Example Results

### Question 1

```text
Layihənin test parolu nədir?
```

Expected answer:

```text
Layihənin test parolu “ALFA-27” olaraq qeyd olunub.
```

---

### Question 2

```text
Şahzadə Qülləsinin gizli kod adı nədir?
```

Expected answer:

```text
Layihənin gizli kod adı “Mavi Qapı”dır.
```

---

### Question 3

```text
Layihənin xüsusi test rəngi nədir?
```

Expected answer:

```text
Layihənin xüsusi test rəngi “tünd bənövşəyi” seçilib.
```

---

## Output Files

### `data/chunks/chunks.jsonl`

Stores document chunks.

Each line contains:

```json
{
  "chunk_id": 1,
  "text": "..."
}
```

---

### `data/index/vector_index.json`

Stores chunk vectors for retrieval.

Each item contains:

```json
{
  "chunk_id": 1,
  "text": "...",
  "vector": {
    "word": 1
  }
}
```

---

### `outputs/rag_results.txt`

Stores RAG question-answer results.

Each line contains:

```json
{
  "time": "...",
  "question": "...",
  "answer": "...",
  "top_k": 3,
  "retrieved_chunks": []
}
```

---

## Current Status

```text
Status: Completed as V5 basic RAG experiment
```

This version successfully demonstrates a basic local RAG workflow using a TXT document, chunking, keyword-based retrieval, and answer sentence selection.

---

## Limitations

This version is intentionally simple.

Main limitations:

* no real embedding model
* no vector database
* no PDF support
* no LLM generation
* no source citation UI
* only one TXT document
* keyword matching can miss semantic meaning
* answer is selected from existing document sentences

---

## Future Improvements

Possible next improvements:

* add real embedding model
* add PDF document support
* support multiple documents
* add source citations
* connect RAG to V2 FastAPI backend
* connect RAG to V3 browser UI
* use local LLM to generate final answers from retrieved context
* add evaluation using V4 feedback workflow
* add document upload system

---

## Version Summary

```text
V1 → Fine-tuned LoRA adapter
V2 → Served adapter through FastAPI
V3 → Built browser chat UI
V4 → Added feedback and evaluation system
V5 → Added basic RAG document search
```

Sahzade AI RAG Document Chat V5 is a successful first RAG experiment and prepares the project for more advanced document-based assistant features.
