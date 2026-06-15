# Sahzade AI RAG Document Chat V5

A basic local Retrieval-Augmented Generation experiment for document question answering.

## Overview

Sahzade AI RAG Document Chat V5 is the fifth step of the Sahzade AI project.

In earlier versions, the assistant was fine-tuned, served through a local API, connected to a chat interface, and evaluated with feedback labels.
In V5, the focus is on adding a simple document-based question-answering system.

The goal of this project is to understand the core idea of RAG: searching relevant information from a document before answering a user question.

## What is RAG?

RAG means Retrieval-Augmented Generation.

Simple idea:

```text
Search first, answer second.
```

Instead of relying only on the model’s general knowledge, the system first searches inside a local document and then uses the retrieved information to answer the question.

## Project Goals

* Read a local text document
* Split the document into smaller chunks
* Create a simple searchable index
* Retrieve the most relevant chunks for a user question
* Select an answer from the retrieved text
* Save RAG test results
* Understand the basic workflow before adding advanced RAG features

## What This Version Includes

* TXT document loading
* Document chunking
* Chunk overlap
* Simple keyword-based index
* Cosine similarity search
* Top-k retrieval
* Basic answer selection
* Terminal-based RAG chat
* Saved RAG results

## What This Version Does Not Include

* PDF support
* Real embedding models
* Vector databases
* LLM-based answer generation
* FastAPI endpoint
* Frontend integration
* Source citation UI
* Production deployment

These features can be added in later versions.

## RAG Flow

```text
User question
    ↓
Load document chunks
    ↓
Search for relevant chunks
    ↓
Retrieve top matching text
    ↓
Select the best answer sentence
    ↓
Return answer
```

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

## Main Components

### `src/document_loader.py`

Loads the local text document and prints a short preview.

Main responsibilities:

* Check whether the document exists
* Read the document content
* Show basic document information
* Print a short preview for testing

### `src/chunker.py`

Splits the source document into smaller text chunks.

Main responsibilities:

* Read the document
* Split text into chunks
* Add chunk IDs
* Save chunks into `chunks.jsonl`

### `src/retriever.py`

Builds a simple searchable index and retrieves relevant chunks.

Main responsibilities:

* Tokenize chunk text
* Create word-count vectors
* Save a basic vector index
* Compare user questions with document chunks
* Return the most relevant chunks

### `src/rag_chat.py`

Runs the terminal-based RAG chat.

Main responsibilities:

* Receive user questions
* Search the document index
* Select a possible answer
* Print the answer in the terminal
* Save test results into `outputs/rag_results.txt`

## How to Run

### 1. Build the index

```bash
chmod +x scripts/build_index.sh
./scripts/build_index.sh
```

### 2. Start the RAG chat

```bash
chmod +x scripts/run_rag_chat.sh
./scripts/run_rag_chat.sh
```

### 3. Check saved results

```text
outputs/rag_results.txt
```

## Example Use Case

A local document contains private or project-specific information.

The user asks:

```text
What is the test password?
```

The system searches the document and returns the answer based on the retrieved text.

## Why This Project Matters

A useful AI assistant should not only generate text from memory.

It should also be able to:

* search documents
* use external knowledge
* answer based on provided context
* reduce unsupported guesses
* prepare for future document chat features

This project adds the first simple RAG layer to the Sahzade AI system.

## Future Improvements

* Add real embedding models
* Add PDF support
* Add source citations
* Add FastAPI endpoint
* Connect RAG to the chat UI
* Add vector database support
* Combine RAG with the local LLM assistant
* Improve answer generation quality

## Project Status

Completed as V5 basic RAG experiment.
