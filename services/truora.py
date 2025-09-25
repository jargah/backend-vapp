# services.py
from __future__ import annotations

import os
import json
import logging
import urllib.parse
import requests
import base64
from datetime import datetime
from typing import Optional, Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TRUORA_API_KEY = os.environ["TRUORA_API_KEY"]
FLOW_ID = os.environ["TRUORA_FLOW_ID"]
DEFAULT_COUNTRY = os.getenv("TRUORA_DEFAULT_COUNTRY", "MX")

TRUORA_API_KEYS_URL = "https://api.account.truora.com/v1/api-keys"
TRUORA_IDENTITY_RESULT_URL = "https://api.identity.truora.com/v1/processes/{process_id}/result"
TRUORA_IDENTITY_BASE_URL = "https://identity.truora.com/?token="

def _b64url_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)

def _jwt_payload_unverified(token: str) -> dict:
    parts = token.split(".")
    if len(parts) < 2:
        logger.warning("Token no parece ser un JWT válido")
        return None
    return json.loads(_b64url_decode(parts[1]).decode("utf-8", "ignore"))

def _extract_process_id_from_token(token: str) -> Optional[str]:
    payload = _jwt_payload_unverified(token)
    add = payload.get("additional_data")
    if isinstance(add, str):
        try:
            add = json.loads(add)
        except Exception:
            add = None
    if isinstance(add, dict):
        return add.get("process_id") or add.get("processId")
    return None



def createLink(payload: dict) -> dict:
    
    print(payload)
    
    country = payload.get("TRUORA_COUNTRY") or payload.get("country", DEFAULT_COUNTRY)
    phone = payload.get("phone")
    email = payload.get("email")
    metadata = payload.get("metadata", {}) or {}
    _ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    redirect_url = payload.get("redirect_url")
    if not redirect_url:
        return {
            'error': True,
            'message': 'error_redirect_url_required'
        }

    form = {
        "key_type": "web",
        "grant": "digital-identity",
        "api_key_version": "1",
        "country": country,
        "redirect_url": redirect_url,
        "flow_id": FLOW_ID,
    }
    
    if phone:
        form["phone"] = phone
    if email:
        form["emails"] = email
    for k, v in metadata.items():
        form[f"start_variables.metadata.{k}"] = str(v)

    headers = {
        "Truora-API-Key": TRUORA_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    r = requests.post(TRUORA_API_KEYS_URL, headers=headers, data=form, timeout=30)
    if r.status_code >= 300:
        logger.error("Truora error: %s %s", r.status_code, r.text)
        return {
            'error': True,
            'message': 'error_truora_apis_keys'
        }

    api_key_token = r.json().get("api_key")
    link = f"{TRUORA_IDENTITY_BASE_URL}{urllib.parse.quote(api_key_token)}"

    process_id: Optional[str] = None
    try:
        process_id = _extract_process_id_from_token(api_key_token)
    except Exception as e:
        logger.warning("No se pudo extraer process_id del token: %s", e)

    return {
        'error': False,
        'data': {
            "process_link": link,
            "token": api_key_token,
            "process_id": process_id,
        }
    }

def getResult(process_id: str) -> dict:

    headers = {
        "Truora-API-Key": TRUORA_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    url = TRUORA_IDENTITY_RESULT_URL.format(process_id=process_id)
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code >= 300:
        logger.error("Truora result error: %s %s", r.status_code, r.text)
        return {
            'error': True,
            'message': 'error_truora_check_result'
        }

    data = r.json()

    status = data.get("status") or data.get("process", {}).get("status")
    failure_status = (
        data.get("failure_status")
        or data.get("failureStatus")
        or data.get("process", {}).get("failure_status")
    )
    declined_reason = (
        data.get("declined_reason")
        or data.get("declinedReason")
        or data.get("process", {}).get("declined_reason")
    )
    metadata = (
        data.get("metadata")
        or data.get("start_variables", {}).get("metadata")
        or data.get("process", {}).get("metadata")
        or {}
    )

    return {
        'error': False,
        'data': {
            "status": status,
            "failure_status": failure_status,
            "declined_reason": declined_reason,
            "metadata": metadata,
        }
    }
