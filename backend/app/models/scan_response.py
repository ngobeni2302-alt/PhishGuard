from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class Verdict(str, Enum):
    GREEN = "GREEN"    # Safe / Low Risk
    YELLOW = "YELLOW"  # Caution / Moderate Risk
    RED = "RED"        # Phishing / High Risk

class ScanResponse(BaseModel):
    verdict: Verdict = Field(..., description="Final security classification")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence rating from 0.0 to 1.0")
    target_brand: Optional[str] = Field(default=None, description="Brand being impersonated if detected (e.g., FNB, SARS)")
    reasons: List[str] = Field(default_factory=list, description="Plain-language explanations backing the verdict")
    recommended_action: str = Field(..., description="Actionable safety guidance for the user")
    final_destination_url: Optional[str] = Field(default=None, description="Resolved target URL after unrolling redirects")

    class Config:
        json_schema_extra = {
            "example": {
                "verdict": "RED",
                "confidence_score": 0.96,
                "target_brand": "FNB",
                "reasons": [
                    "Domain 'fnb-secure-login.co.za' closely mimics 'fnb.co.za' (Typosquatting detected).",
                    "Domain was registered less than 48 hours ago.",
                    "Link was shortened using bit.ly to obscure destination."
                ],
                "recommended_action": "Do not tap the link or enter credentials. Report and delete the message.",
                "final_destination_url": "http://fnb-secure-login.co.za/verify"
            }
        }