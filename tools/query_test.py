from tools.retrieval import query_vectorstore

if __name__ == "__main__":
    q = "Summarize competitor positioning and pricing risks"
    results = query_vectorstore(q, k=5)

    print(f"Query: {q}\n")
    for i, d in enumerate(results, start=1):
        src = d.metadata.get("source", "unknown")
        preview = d.page_content.strip().replace("\n", " ")
        preview = preview[:220] + ("..." if len(preview) > 220 else "")
        print(f"[{i}] source={src}")
        print(f"    {preview}\n")
