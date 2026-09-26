from dataclasses import dataclass
import re

ALLOWED_TOPICS = {
    "it": ["password", "login", "vpn", "network", "laptop", "computer", "software", "hardware", "account", "phishing", "malware", "mfa"],
    "product": ["product", "acmeflow", "feature", "bug", "release", "sla", "dashboard", "platform", "workflow", "support"],
    "hr": ["leave", "holiday", "attendance", "benefit", "insurance", "handbook", "hr", "employee", "parental"],
    "talent": ["appraisal", "performance", "review", "promotion", "career", "training", "learning", "certification", "goal", "feedback"],
    "business": ["expense", "reimbursement", "invoice", "payroll", "tax", "corporate card", "nda", "procurement", "finance"],
}

BLOCKED = [
    "medical diagnosis", "medical treatment", "investment advice",
    "political campaign", "election campaign", "weapon construction",
    "malware creation", "credential theft", "password cracking"
]

@dataclass
class GuardrailResult:
    allowed: bool
    reason: str = ""

def validate_input(query: str) -> GuardrailResult:
    q = query.lower().strip()
    if not q:
        return GuardrailResult(False, "Please enter a question.")
    if any(term in q for term in BLOCKED):
        return GuardrailResult(False, "That topic is outside this customer-support assistant's scope.")
    if len(q) > 2000:
        return GuardrailResult(False, "Please shorten the question to 2000 characters or less.")
    return GuardrailResult(True)

def topic_fit(query: str, department: str) -> bool:
    q = query.lower()
    terms = ALLOWED_TOPICS.get(department, [])
    return any(re.search(r"\b" + re.escape(t) + r"\b", q) for t in terms)
