from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 5):
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(r["body"])

    return "\n".join(results)
