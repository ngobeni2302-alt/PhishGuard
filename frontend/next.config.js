from enum import Enum
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field

class ScanSource(str, Enum):
    SMS = "sms"
    SOCIAL_DM = "social_dm"
    CLIPBOARD = "clipboard"
    QR_CODE = "qr_code"
    SYSTEM = "system"

class ScanRequest(BaseModel):
    url: str = Field(..., description="The URL or link extracted from the source message", example="http://bit.ly/3xY123")
    source: ScanSource = Field(default=ScanSource.CLIPBOARD, description="The vector/channel where the link was encountered")
    raw_message_text: Optional[str] = Field(default=None, description="The full message or text context surrounding the link")

    class Config:
        json_schema_extra = {
            "example": {
                "url": "http://fnb-secure-login.co.za/verify",
                "source": "sms",
                "raw_message_text": "FNB: Your account is locked. Verify details here: http://fnb-secure-login.co.za/verify"
            }
        }