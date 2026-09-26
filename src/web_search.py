import os, requests

SERPER_URL = "https://google.serper.dev/search"

def web_search(query, num=5):
    key = os.getenv("SERPER_API_KEY")
    if not key:
        return []
    resp = requests.post(
        SERPER_URL,
        headers={"X-API-KEY": key, "Content-Type": "application/json"},
        json={"q": query, "num": num},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    results = []
    for item in data.get("organic", [])[:num]:
        results.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", ""),
        })
    return results
