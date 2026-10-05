import os
import chromadb
import ollama

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHROMA_PATH = os.path.join(BASE_DIR, "..", "chroma_db")

KNOWLEDGE_FILE = os.path.join(
    BASE_DIR,
    "..",
    "knowledge_base",
    "company_policy.txt"
)

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = chroma_client.get_or_create_collection(
    name="company_knowledge_v2"
)


def load_knowledge_base():

    if not os.path.exists(KNOWLEDGE_FILE):
        print("ERROR: company_policy.txt not found!")
        print("Expected location:")
        print(KNOWLEDGE_FILE)
        return

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        text = file.read()

    chunks = [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]

    print("Number of chunks:", len(chunks))

    if not chunks:
        print("ERROR: Knowledge base is empty!")
        return

    for index, chunk in enumerate(chunks):

        print(f"Creating embedding for chunk {index + 1}...")

        response = ollama.embed(
            model="nomic-embed-text",
            input=chunk
        )

        embedding = response["embeddings"][0]

        collection.upsert(
            ids=[f"chunk_{index}"],
            documents=[chunk],
            embeddings=[embedding]
        )

    print("Knowledge base loaded successfully!")
    print("Collection count:", collection.count())


def search_knowledge(question):

    response = ollama.embed(
        model="nomic-embed-text",
        input=question
    )

    question_embedding = response["embeddings"][0]

    count = collection.count()

    print("Collection count before search:", count)

    if count == 0:
        return []

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(3, count)
    )

    documents = results.get("documents", [[]])

    if not documents or not documents[0]:
        return []

    return documents[0]


if __name__ == "__main__":

    print("Loading AI Customer Support Knowledge Base...")

    load_knowledge_base()

    question = "How many days do I have to return a product?"

    print("\nTest Question:")
    print(question)

    results = search_knowledge(question)

    print("\nRelevant Information:")

    if results:
        for result in results:
            print("-", result)
    else:
        print("No relevant information found.")