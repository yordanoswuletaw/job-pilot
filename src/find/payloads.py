import json

roles = [
    "Remote AI Engineer",
    "AI Engineer",
    "ML/AI Engineer"
]

def define_payloads():
    payloads = []
    for role in roles:
        payloads.append({"q": role})
        
    return json.dumps(payloads)