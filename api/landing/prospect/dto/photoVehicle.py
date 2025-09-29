from typing import Annotated, Optional, Dict, Iterator, Tuple
from fastapi import Form, File, UploadFile
from pydantic import BaseModel, Field, model_validator, PrivateAttr

ALLOWED_MIME = {"image/jpeg", "image/png", "image/jpeg"}
MAX_BYTES = 5 * 1024 * 1024  # 5 MB por archivo


class PhotoVehicleDTO(BaseModel):

    photo_front: Optional[UploadFile] = Field(None, description="Archivo: tarjeta de circulación")
    photo_left_side: Optional[UploadFile] = Field(None, description="Archivo: póliza de seguro")
    photo_right_side: Optional[UploadFile] = Field(None, description="Archivo: factura")
    photo_rear: Optional[UploadFile] = Field(None, description="Archivo: engomado/verificación")
    photo_three_quarters: Optional[UploadFile] = Field(None, description="Archivo: engomado/verificación")

    # Atributo privado para cachear el dict de archivos presentes
    _files_present: Dict[str, UploadFile] = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _validate_files(self) -> "PhotoVehicleDTO":
        files = {
            "photo_front": self.photo_front,
            "photo_left_side": self.photo_left_side,
            "photo_right_side": self.photo_right_side,
            "photo_rear": self.photo_rear,
            "photo_three_quarters": self.photo_three_quarters,
        }
        present = {k: v for k, v in files.items() if v is not None}

        if not present:
            # ValueError hace que FastAPI devuelva 422 con detalle del campo
            raise ValueError("Send at least one file: photo_front | photo_left_side | photo_right_side | photo_rear | photo_three_quarters")

        # Validar MIME por archivo
        for name, f in present.items():
            if f.content_type not in ALLOWED_MIME:
                raise ValueError(
                    f"Field '{name}' has unsupported media type '{f.content_type}'. "
                    f"Allowed: {', '.join(sorted(ALLOWED_MIME))}"
                )

        # Guardar en atributo privado para acceso rápido
        self._files_present = present
        return self

    # Helper: iterar archivos presentes como (field, UploadFile)
    def iter_files(self) -> Iterator[Tuple[str, UploadFile]]:
        for k, v in self._files_present.items():
            yield k, v

    # === Patrón as_form: permite usar el DTO con multipart/form-data ===
    @classmethod
    def as_form(
        cls,
        photo_front: UploadFile | None = File(None),
        photo_left_side: UploadFile | None = File(None),
        photo_right_side: UploadFile | None = File(None),
        photo_rear: UploadFile | None = File(None),
        photo_three_quarters: UploadFile | None = File(None),
    ) -> "PhotoVehicleDTO":
        return cls(
            photo_front=photo_front,
            photo_left_side=photo_left_side,
            photo_right_side=photo_right_side,
            photo_rear=photo_rear,
            photo_three_quarters=photo_three_quarters
        )