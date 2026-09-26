from .rag import RAGService
from .guardrails import validate_input
from .web_search import web_search
from .agents import run

AGENT_TO_DEPT = {
    "IT_Service_Desk_Agent": "it",
    "Product_Client_Success_Agent": "product",
    "People_Ops_HR_Policy_Agent": "hr",
    "Talent_Management_Growth_Agent": "talent",
    "Business_Ops_Corporate_Agent": "business",
}

def build_context(results, web_results=None):
    parts = []
    if results:
        parts.append("INTERNAL RAG SOURCES:")
        for r in results:
            parts.append(f"[Source: {r['source']}, p.{r['page']}, v{r['version']}, score={r['rerank_score']:.3f}]\n{r['text']}")
    if web_results:
        parts.append("\nEXTERNAL WEB FALLBACK:")
        for w in web_results:
            parts.append(f"[Web: {w['title']}] {w['snippet']} URL: {w['link']}")
    return "\n\n".join(parts)

def answer(query, agent_name):
    check = validate_input(query)
    if not check.allowed:
        return {"answer": check.reason, "mode": "guardrail", "sources": []}

    rag = RAGService()
    department = AGENT_TO_DEPT[agent_name]
    retrieval_query = query
    if department == "hr":
        retrieval_query += " annual paid leave vacation PTO time off"
    results = rag.retrieve(retrieval_query, department=department)

    mode = "RAG"
    web_results = []
    if not rag.is_grounded_enough(results):
        # RAG-first: web is consulted only when internal knowledge is insufficient.
        web_results = web_search(query)
        mode = "WEB_FALLBACK" if web_results else "NO_SOURCE"

    context = build_context(results if mode == "RAG" else [], web_results)
    if not context:
        return {
            "answer": "I could not find enough approved internal information to answer this question, and no web fallback is configured.",
            "mode": "NO_SOURCE", "sources": results
        }
    return {"answer": run(query, context, agent_name), "mode": mode, "sources": results, "web": web_results}
