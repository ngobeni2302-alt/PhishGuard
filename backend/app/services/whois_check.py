from datetime import datetime
import asyncio
import tldextract
import whois

async def analyze_domain_age(url: str) -> dict:
    """
    Retrieves WHOIS registration data to determine domain age.
    Young domains (<30 days) are high-risk zero-day indicators.
    """
    extracted = tldextract.extract(url)
    domain_name = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain

    if not domain_name:
        return {"domain": "", "age_days": None, "creation_date": None, "is_new_domain": False}

    def _fetch_whois():
        try:
            return whois.whois(domain_name)
        except Exception:
            return None

    # Run blocking WHOIS call in an async executor
    loop = asyncio.get_event_loop()
    w = await loop.run_in_executor(None, _fetch_whois)

    if not w or not w.creation_date:
        return {"domain": domain_name, "age_days": None, "creation_date": None, "is_new_domain": False}

    creation_date = w.creation_date
    if isinstance(creation_date, list):
        creation_date = creation_date[0]

    age_days = (datetime.utcnow() - creation_date).days
    return {
        "domain": domain_name,
        "age_days": age_days,
        "creation_date": creation_date.isoformat(),
        "is_new_domain": age_days < 30
    }