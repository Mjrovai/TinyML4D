import ollama
import chromadb
import time

EMB_MODEL = "nomic-embed-text"
MODEL = "llama3.2:3b"
COLLECTION_NAME = "bee_data_interactive"

DOCUMENTS = [
    "Bee-keeping, also known as apiculture, involves the maintenance of bee colonies, typically in hives, by humans.",
    "The most commonly kept species of bees is the European honey bee (Apis mellifera).",
    "Bee-keeping dates back to at least 4,500 years ago, with evidence of ancient Egyptians practicing it.",
    "A beekeeper's primary role is to manage hives to ensure the health of the bee colony and maximize honey production.",
    "Honey bees are social insects, living in colonies with a single queen, numerous worker bees, and drones.",
    "The queen bee can lay up to 2,000 eggs per day during peak seasons.",
    "Worker bees are female and perform all the tasks in the hive except for reproduction.",
    "Drones are male bees whose primary role is to mate with a queen from another hive.",
    "Honey bees communicate with each other through the 'waggle dance,' which indicates the direction and distance to food sources.",
    "Bees produce honey from the nectar they collect from flowers, which they store in the hive for food during winter.",
    "Bees also produce beeswax, which they use to build the honeycomb structure in the hive.",
    "Propolis, another bee product, is a resin-like substance collected from tree buds and used to seal gaps in the hive.",
    "Bees play a crucial role in pollination, which is essential for the reproduction of many plants and crops.",
    "A typical bee colony can contain between 20,000 and 80,000 bees.",
    "Bee-keeping can be done for various purposes, including honey production, pollination services, and the sale of bees and related products.",
    "Beekeepers must inspect their hives regularly to check for diseases, pests, and the overall health of the colony.",
    "Common pests and diseases that affect bees include varroa mites, hive beetles, and foulbrood.",
    "Bee-keeping requires protective clothing and equipment, such as a bee suit, gloves, and a smoker to calm the bees.",
    "Sustainable bee-keeping practices are important for maintaining healthy bee populations and ecosystems.",
    "Beekeeping can be a hobby, a part-time occupation, or a full-time profession, depending on the scale and intent of the beekeeper.",
    "Almost all the honey we consume comes from western honey bees (Apis mellifera), a hybrid of European and African species.",
    "There are another 20,000 different bee species in the world.",
    "Brazil alone has more than 300 different bee species, and the vast majority, unlike western honey bees, don’t sting.",
    "Reports written in 1577 by Hans Staden, mention three native bees used by indigenous people in Brazil.",
    "The indigenous people in Brazil used bees for medicine and food purposes",
    "From Hans Staden report: probable species: mandaçaia (Melipona quadrifasciata), mandaguari (Scaptotrigona postica) and jataí-amarela (Tetragonisca angustula).",
    "Colombia has many bee species, including the introduced Africanized honey bee Apis mellifera and numerous native bees such as stingless Meliponini (e.g., Melipona, Nannotrigona) and wild solitary species like Centris and orchid bees (Eulaema)."
]

client = chromadb.Client()
existing = {c.name for c in client.list_collections()}

if COLLECTION_NAME in existing:
    collection = client.get_collection(COLLECTION_NAME)
else:
    collection = client.create_collection(name=COLLECTION_NAME)
    for i, doc in enumerate(DOCUMENTS):
        response = ollama.embeddings(model=EMB_MODEL, prompt=doc)
        collection.add(
            ids=[str(i)],
            embeddings=[response["embedding"]],
            documents=[doc]
        )

def retrieve(query, n_results=5):
    emb = ollama.embeddings(model=EMB_MODEL, prompt=query)["embedding"]
    results = collection.query(
        query_embeddings=[emb],
        n_results=n_results
    )
    docs = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0] if results.get("distances") else []
    return docs, distances

def answer_question(prompt, n_results=5, temp=0.0, top_k=10, top_p=0.5, show_context=False):
    start_time = time.perf_counter()
    docs, distances = retrieve(prompt, n_results=n_results)
    context = "\n".join(f"- {doc}" for doc in docs)

    final_prompt = f"""You are a helpful RAG assistant.
Answer ONLY from the retrieved context below.
If the answer is not in the context, say: I couldn't find that in the knowledge base.

Context:
{context}

Question: {prompt}
Answer:"""

    output = ollama.generate(
        model=MODEL,
        prompt=final_prompt,
        options={
            "temperature": temp,
            "top_k": top_k,
            "top_p": top_p
        }
    )

    elapsed_time = round(time.perf_counter() - start_time, 2)

    if show_context:
        print("\nRetrieved context:")
        for idx, doc in enumerate(docs, start=1):
            score = distances[idx - 1] if idx - 1 < len(distances) else "n/a"
            print(f"{idx}. ({score}) {doc}")

    print(f"\nAnswer:\n{output['response']}")
    print(f"\n[INFO] Model: {MODEL} | Embeddings: {EMB_MODEL} | Time: {elapsed_time}s")

def interactive_chat():
    print("Simple Interactive RAG over Bee Knowledge")
    print("Type your question and press Enter.")
    print("Commands: /exit, /quit, /context on, /context off, /k <n>")

    n_results = 5
    show_context = False

    while True:
        try:
            user_input = input("\nAsk> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not user_input:
            continue
        if user_input.lower() in {"/exit", "/quit"}:
            print("Goodbye.")
            break
        if user_input.lower() == "/context on":
            show_context = True
            print("Retrieved context display enabled.")
            continue
        if user_input.lower() == "/context off":
            show_context = False
            print("Retrieved context display disabled.")
            continue
        if user_input.lower().startswith("/k "):
            try:
                n_results = max(1, int(user_input.split()[1]))
                print(f"n_results set to {n_results}")
            except (IndexError, ValueError):
                print("Usage: /k <integer>")
            continue

        answer_question(user_input, n_results=n_results, show_context=show_context)

if __name__ == "__main__":
    interactive_chat()
