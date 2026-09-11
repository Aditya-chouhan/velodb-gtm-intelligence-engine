from typing import Dict

def generate_outreach(account: Dict, strategy: Dict) -> Dict[str, str]:
    company = account["company"]
    observed = strategy.get("why_now", [])
    evidence_line = observed[0] if observed else "your data-platform direction"
    motion = strategy["recommended_motion"]
    linkedin = f"Hi — I was looking at {company}'s data infrastructure and noticed {evidence_line.lower()}. That made me curious whether {motion.lower()} is something your team is evaluating. I put together a short evidence-based hypothesis on where VeloDB could fit; happy to share it if useful."
    email = f"Subject: {company} × real-time analytics\n\nI noticed {evidence_line.lower()}. Rather than assume there is a problem, I mapped a short hypothesis around {motion.lower()} and the signals that would make an evaluation worthwhile. If relevant, I can send the 1-page account brief."
    return {"linkedin": linkedin, "email": email}
