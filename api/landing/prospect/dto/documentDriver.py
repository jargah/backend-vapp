from __future__ import annotations

from typing import Dict, Iterator, Tuple
from fastapi import Form, File, UploadFile
from pydantic import BaseModel, Field, model_validator, PrivateAttr, ConfigDict


class DocumentDriverDTO(BaseModel):
    """
    TODOS los campos son OBLIGATORIOS.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # ---- Archivos (requeridos) ----
    tax_certificate: UploadFile = Field(..., description="Constancia fiscal (PDF/IMG)")
    ine_front: UploadFile = Field(..., description="INE frente")
    ine_back: UploadFile = Field(..., description="INE reverso")
    csd_certificate: UploadFile = Field(..., description="CSD certificado (.cer)")
    csd_key: UploadFile = Field(..., description="CSD llave (.key)")

    # ---- Textos (requeridos) ----
    csd_password: str = Field(..., description="Contraseña de la llave CSD")
    taxid: str = Field(..., description="RFC")
    regimen: str = Field(..., description="Régimen fiscal")

    # Interno
    _files_present: Dict[str, UploadFile] = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _collect_files(self) -> "DocumentDriverDTO":
        self._files_present = {
            "tax_certificate": self.tax_certificate,
            "ine_front": self.ine_front,
            "ine_back": self.ine_back,
            "csd_certificate": self.csd_certificate,
            "csd_key": self.csd_key,
        }
        return self

    def iter_files(self) -> Iterator[Tuple[str, UploadFile]]:
        for k, v in self._files_present.items():
            yield k, v

    @classmethod
    def as_form(
        cls,
        # Archivos requeridos
        tax_certificate: UploadFile = File(...),
        ine_front: UploadFile = File(...),
        ine_back: UploadFile = File(...),
        csd_certificate: UploadFile = File(...),
        csd_key: UploadFile = File(...),
        # Textos requeridos
        csd_password: str = Form(...),
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
