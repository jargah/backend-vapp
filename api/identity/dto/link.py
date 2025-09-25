from __future__ import annotations
from typing import Optional, Dict
from pydantic import BaseModel, EmailStr, Field

class TruoraLinkDTO(BaseModel):
    country: Optional[str] = Field(None, description="error_empty_country_required")
    phone: Optional[str] = Field(None, description="error_empty_phone_required")
    email: Optional[EmailStr] = Field(None, description="error_empty_email_required")
    metadata: Optional[Dict[str, str]] = Field(default_factory=dict, description="error_empty_metadata_required")
    redirect_url: Optional[str] = Field(None, description="error_empty_redirect_url_required")

    model_config = {
        "extra": "forbid",
        "str_strip_whitespace": True,
        "json_schema_extra": {
            "example": {
                "country": "MX",
                "phone": "+523322238886",
                "email": "jaime.gonzalez@ven-app.com.mx",
                "metadata": {"id_passenger": "1", "type": "register"},
                "redirect_url": "https://identity.ven-app.taxi/validation"
            }
        },
    }