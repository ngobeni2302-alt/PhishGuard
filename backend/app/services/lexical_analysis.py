import re
import tldextract

SUSPICIOUS_KEYWORDS = [
    "verify", "login", "secure", "update", "account", "banking",
    "free", "claim", "sars-refund", "payout", "urgent", "suspended"
]

SUSPICIOUS_TLDS = ["xyz", "top", "club", "online", "site", "vip", "icu", "work"]

def extract_lexical_features(url: str) -> dict:
    """
    Extracts structural/lexical features from the URL string.
    """
    extracted = tldextract.extract(url)
    tld = extracted.suffix.lower()
    
    # IP address check
    is_ip = bool(re.match(r"^https?://\d{1,3}(\.\d{1,3}){3}", url))
    
    # Symbol & keyword counts
    has_at_symbol = "@" in url
    hyphen_count = url.count("-")
    subdomain_count = len(extracted.subdomain.split(".")) if extracted.subdomain else 0
    
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in url.lower()]
    is_suspicious_tld = tld in SUSPICIOUS_TLDS

    return {
        "is_ip_address": is_ip,
        "has_at_symbol": has_at_symbol,
        "hyphen_count": hyphen_count,
        "subdomain_count": subdomain_count,
        "suspicious_keywords": found_keywords,
        "is_suspicious_tld": is_suspicious_tld,
        "raw_length": len(url)
    }