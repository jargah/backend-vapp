from typing import Optional, Dict, Iterator, Tuple
from fastapi import Form, File, UploadFile
from pydantic import BaseModel, Field, model_validator, PrivateAttr

ALLOWED_MIME = {
    "application/pdf"
}
MAX_BYTES = 5 * 1024 * 1024  # 5 MB por archivo


class DocumentVehicleDTO(BaseModel):

    circulation_card: Optional[UploadFile] = Field(None, description="Tarjeta de circulación")
    insurance_policy: Optional[UploadFile] = Field(None, description="Póliza de seguro")
    invoice: Optional[UploadFile] = Field(None, description="Factura")
    verification_sticker: Optional[UploadFile] = Field(None, description="Engomado/verificación")

    _files_present: Dict[str, UploadFile] = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _validate_files(self) -> "DocumentVehicleDTO":
        files = {
            "circulation_card": self.circulation_card,
            "insurance_policy": self.insurance_policy,
            "invoice": self.invoice,
            "verification_sticker": self.verification_sticker,
        }
        present = {k: v for k, v in files.items() if v is not None}
        if not present:
            raise ValueError("Send at least one file: circulation_card | insurance_policy | invoice | verification_sticker")

        for name, f in present.items():
            if f.content_type not in ALLOWED_MIME:
                raise ValueError(
                    f"Field '{name}' has unsupported media type '{f.content_type}'. "
                    f"Allowed: {', '.join(sorted(ALLOWED_MIME))}"
                )

        self._files_present = present
        return self

    def iter_files(self) -> Iterator[Tuple[str, UploadFile]]:
        for k, v in self._files_present.items():
            yield k, v

    # 👇 CLAVE: NO uses Annotated aquí. Declara los defaults con '='.
    @classmethod
    def as_form(
        cls,
        circulation_card: UploadFile | None = File(None),
        insurance_policy: UploadFile | None = File(None),
        invoice: UploadFile | None = File(None),
        verification_sticker: UploadFile | None = File(None),
    ) -> "DocumentVehicleDTO":
        return cls(
            circulation_card=circulation_card,
            insurance_policy=insurance_policy,
            invoice=invoice,
            verification_sticker=verification_sticker,
        )