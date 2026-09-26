import json

from src.rag import RAGService

CASES = [
    ("How many annual paid leave days are provided?", "hr", "employee_handbook.pdf"),
    ("When are performance reviews conducted?", "talent", "appraisal_and_growth_policy.pdf"),
    ("How long should a complete invoice take to process?", "business", "business_operations_policy.pdf"),
    ("What should a bug report contain?", "product", "product_client_success_guide.pdf"),
    ("How many failed logins cause a temporary lock?", "it", "it_service_desk_policy.pdf"),
]

def main():
    rag = RAGService()
    hits, mrr = 0, 0.0
    details = []
    for q, dept, expected in CASES:
        results = rag.retrieve(q, dept)
        ranks = [i+1 for i,r in enumerate(results) if r["source"] == expected]
        hit = bool(ranks)
        hits += int(hit)
        if ranks: mrr += 1/ranks[0]
        details.append({"question":q, "expected":expected, "hit":hit, "rank":ranks[0] if ranks else None,
                        "top_score":results[0]["rerank_score"] if results else None})
    report = {"hit_rate": hits/len(CASES), "mrr": mrr/len(CASES), "cases":details}
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
