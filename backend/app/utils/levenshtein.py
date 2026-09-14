import tldextract
from typing import List, Optional, Tuple

# Targeted South African institutional domains to protect
TARGET_SA_BRANDS = {
    "fnb": "fnb.co.za",
    "capitec": "capitecbank.co.za",
    "sars": "sars.gov.za",
    "postnet": "postnet.co.za",
    "absa": "absa.co.za",
    "standardbank": "standardbank.co.za",
    "nedbank": "nedbank.co.za",
    "discovery": "discovery.co.za",
}


def calculate_distance(s1: str, s2: str) -> int:
    """Calculates the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return calculate_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def check_typosquatting(
    raw_url: str, threshold: int = 2
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Checks if a URL's domain is typosquatting on any protected SA brand.
    Returns: (is_typosquatting, target_brand_name, legitimate_domain)
    """
    extracted = tldextract.extract(raw_url)
    if not extracted.domain:
        return False, None, None

    input_domain = extracted.domain.lower()

    for brand_key, legitimate_fqdn in TARGET_SA_BRANDS.items():
        legit_extracted = tldextract.extract(legitimate_fqdn)
        legit_domain = legit_extracted.domain.lower()

        # Ignore if it's an exact match (legitimate domain)
        if input_domain == legit_domain:
            return False, None, None

        # Check Levenshtein distance against registered brand domain
        distance = calculate_distance(input_domain, legit_domain)
        if 0 < distance <= threshold:
            return True, brand_key.upper(), legitimate_fqdn

    return False, None, None