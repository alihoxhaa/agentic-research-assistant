from tools.retrieval import build_vectorstore

def ingest_docs(reset: bool = False):
    build_vectorstore(reset=reset)
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_docs(reset=True)