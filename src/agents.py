from openai import AuthenticationError
from openai import OpenAI
from .config import OPENAI_API_KEY, CHAT_MODEL

termination = (
    "\n\nCRITICAL: Answer only from the supplied context. "
    "If context is insufficient, explicitly say so. Do not invent policy numbers, dates or entitlements."
)

agent_specs = {
    "IT_Service_Desk_Agent": """You are the IT Service Desk & Infrastructure AI Agent.
Handle hardware/software troubleshooting, account access, VPN, networking, approved software and security incident reporting.""",
    "Product_Client_Success_Agent": """You are the Product & Client Success AI Agent.
Handle product features, user guides, SLAs, releases, onboarding and bug-report information.""",
    "People_Ops_HR_Policy_Agent": """You are the People Operations & HR Policy AI Agent.
Handle employee handbook, leave, attendance, benefits, wellness and holiday information.""",
    "Talent_Management_Growth_Agent": """You are the Talent Management & Growth AI Agent.
Handle appraisal, performance reviews, promotion guidelines, career paths, learning and certification reimbursement.""",
    "Business_Ops_Corporate_Agent": """You are the Business Operations & Corporate Services AI Agent.
Handle expenses, reimbursements, corporate cards, invoices, payroll/tax schedules, NDAs and procurement.""",
}

ROUTER_SYSTEM_MESSAGE = """You are the support router. Return exactly one specialist name and nothing else.
IT_Service_Desk_Agent = IT, accounts, VPN, hardware, network, security
Product_Client_Success_Agent = product, platform, bugs, releases, SLA
People_Ops_HR_Policy_Agent = handbook, leave, benefits, holidays, attendance
Talent_Management_Growth_Agent = appraisal, performance, promotion, career, training
Business_Ops_Corporate_Agent = expense, invoice, payroll, tax, NDA, procurement"""

VALID = set(agent_specs)

def _complete(system_message, user_message):
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env before starting the app.")
    response = OpenAI(api_key=OPENAI_API_KEY).chat.completions.create(
        model=CHAT_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content or ""

def route_agent(query):
    try:
        reply = _complete(ROUTER_SYSTEM_MESSAGE, query)
    except AuthenticationError as e:
        if getattr(e, "status_code", None) == 401:
            raise RuntimeError("OpenAI rejected the API key. Check OPENAI_API_KEY in .env.")
        raise
    text = str(reply).strip()
    for name in VALID:
        if name in text:
            return name
    return "Product_Client_Success_Agent"

def run(query, context, agent_name):
    prompt = f"""USER QUESTION:
{query}

APPROVED CONTEXT:
{context}

Answer the user directly and concisely.
Rules:
1. Prefer internal RAG evidence.
2. If external web evidence is present, clearly say that it is external.
3. Never invent policy numbers, dates, entitlements or product behavior.
4. Cite internal sources inline like [Source: filename, p.X].
5. For web fallback, cite the title and URL.
6. If evidence is insufficient, say what is unknown rather than guessing.
"""
    try:
        reply = _complete(agent_specs[agent_name] + termination, prompt)
        return str(reply).strip()
    except AuthenticationError as e:
        if getattr(e, "status_code", None) == 401:
            return "OpenAI rejected the API key. Check OPENAI_API_KEY in .env."
        raise
