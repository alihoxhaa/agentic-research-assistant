from __future__ import annotations

import shutil
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DATA_DIR = "data/sample_docs"
DB_DIR = "chroma_db"
COLLECTION = "genpact_synthetic_docs"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 150


def load_documents() -> List[Document]:
    docs: List[Document] = []
    base = Path(DATA_DIR)

    for path in base.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        docs.append(Document(page_content=text, metadata={"source": str(path)}))
    for path in base.rglob("*.txt"):
        text = path.read_text(encoding="utf-8")
        docs.append(Document(page_content=text, metadata={"source": str(path)}))
    return docs


def build_vectorstore(reset: bool = True) -> Chroma:
    if reset and Path(DB_DIR).exists():
        shutil.rmtree(DB_DIR)

    raw_docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(raw_docs)

    embeddings = OpenAIEmbeddings()

    # With Chroma 0.4+ persistence is automatic when persist_directory is set.
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR,
        collection_name=COLLECTION,
    )
    return vectorstore


def query_vectorstore(query: str, k: int = 5) -> List[Document]:
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=DB_DIR,
    )
    return vectorstore.similarity_search(query, k=k)
