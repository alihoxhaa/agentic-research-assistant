from tools.retrieval import build_vectorstore

if __name__ == "__main__":
    build_vectorstore(reset=True)
    print("Ingestion complete.")
