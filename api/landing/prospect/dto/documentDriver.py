from __future__ import annotations

import re
from typing import Optional, Dict, Iterator, Tuple, Any
from fastapi import Form, File, UploadFile
from pydantic import BaseModel, Field, model_validator, PrivateAttr, ConfigDict


ALLOWED_MIME = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "application/octet-stream",  # útil para .cer/.key
}

# RFC mexicano (persona moral o física, con homoclave y dígito verificador)
RFC_RE = re.compile(
    r"^(?:[A-ZÑ&]{3}|[A-ZÑ&]{4})\d{6}[A-Z0-9]{3}$",
    re.IGNORECASE
)

# Opcional: restringe regimen a un catálogo
REGIMEN_ALLOWED: set[str] = set()  # ejemplo: {"general", "resico", "pequeños_contribuyentes"}


class DocumentDriverDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # ---- Archivos (requeridos) ----
    tax_certificate: UploadFile = Field(..., description="Constancia fiscal (PDF/IMG)")
    ine_front: UploadFile = Field(..., description="INE frente")
    ine_back: UploadFile = Field(..., description="INE reverso")

    # ---- Archivos (opcionales) ----
    csd_certificate: Optional[UploadFile] = Field(None, description="CSD certificado (.cer)")
    csd_key: Optional[UploadFile] = Field(None, description="CSD llave (.key)")

    # ---- Textos ----
    csd_password: Optional[str] = Field(None, description="Contraseña de la llave CSD")
    taxid: str = Field(..., description="RFC")
    regimen: str = Field(..., description="Régimen fiscal")

    # Interno
    _files_present: Dict[str, UploadFile] = PrivateAttr(default_factory=dict)

    # --- PRE: coerción / tipos seguros ---
    @model_validator(mode="before")
    @classmethod
    def _coerce_and_typecheck(cls, data: dict) -> dict:
        """
        - Convierte strings vacíos o 'null'/'undefined' a None para archivos opcionales y csd_password.
        - Falla si archivos requeridos llegan como string (en lugar de UploadFile).
        """
        if not isinstance(data, dict):
            return data

        def _maybe_none(v):
            return None if isinstance(v, str) and v.strip().lower() in {"", "null", "undefined"} else v

        # Opcionales
        for f in ("csd_certificate", "csd_key", "csd_password"):
            if f in data:
                data[f] = _maybe_none(data[f])

        # Requeridos: si llegan como string → error claro
        for f in ("tax_certificate", "ine_front", "ine_back"):
            if isinstance(data.get(f), str):
                raise TypeError(f"{f} must be an uploaded file (multipart/form-data), not a string.")

        return data

    # --- POST: normalización/validación de negocio ---
    @model_validator(mode="after")
    def _validate_business(self) -> "DocumentDriverDTO":
        # Normalizar textos
        if isinstance(self.taxid, str):
            self.taxid = self.taxid.strip().upper()
        if isinstance(self.regimen, str):
            self.regimen = self.regimen.strip()

        if self.csd_password is not None and isinstance(self.csd_password, str):
            self.csd_password = self.csd_password.strip() or None  # deja None si queda vacío

        # RFC válido
        if not RFC_RE.match(self.taxid):
            raise ValueError("Invalid RFC format for 'taxid'.")

        # Regimen (opcional restringir)
        if REGIMEN_ALLOWED and self.regimen.lower() not in {r.lower() for r in REGIMEN_ALLOWED}:
            raise ValueError(f"regimen '{self.regimen}' is not allowed. Allowed: {', '.join(sorted(REGIMEN_ALLOWED))}")

        # Archivos presentes + content-type permitido
        files = {
            "tax_certificate": self.tax_certificate,
            "ine_front": self.ine_front,
            "ine_back": self.ine_back,
            "csd_certificate": self.csd_certificate,
            "csd_key": self.csd_key,
        }
        present = {k: v for k, v in files.items() if v is not None}
        for name, f in present.items():
            ct = (f.content_type or "").lower()
            if ct not in ALLOWED_MIME:
                raise ValueError(
                    f"Field '{name}' has unsupported media type '{ct}'. "
                    f"Allowed: {', '.join(sorted(ALLOWED_MIME))}"
                )

        self._files_present = present
        return self

    # --- helpers de conveniencia ---
    def iter_files(self) -> Iterator[Tuple[str, UploadFile]]:
        """Archivos presentes como (campo, UploadFile)."""
        for k, v in self._files_present.items():
            yield k, v

    def non_file_values(self) -> dict[str, Any]:
        """Solo valores no archivo (útil para persistir metadatos)."""
        out = {}
        for k in ("csd_password", "taxid", "regimen"):
            out[k] = getattr(self, k)
        return out

    # --- as_form para FastAPI ---
    @classmethod
    def as_form(
        cls,
        # Archivos requeridos
        tax_certificate: UploadFile = File(...),
        ine_front: UploadFile = File(...),
        ine_back: UploadFile = File(...),
        # Archivos opcionales
        csd_certificate: UploadFile | None = File(None),
        csd_key: UploadFile | None = File(None),
        # Textos
        csd_password: str | None = Form(None),
        taxid: str = Form(...),
        regimen: str = Form(...),
    ) -> "DocumentDriverDTO":
        return cls(
            tax_certificate=tax_certificate,
            ine_front=ine_front,
            ine_back=ine_back,
            csd_certificate=csd_certificate,
            csd_key=csd_key,
            csd_password=csd_password,
            taxid=taxid,
            regimen=regimen,
        )
