from sqlmodel import SQLModel, Field as SQLField
from pydantic import BaseModel, Field
from typing import Optional


class CategoriaBase(SQLModel):
    codigo: str
    descripcion: str
    activo: bool = True


class CategoriaCreate(BaseModel):
    codigo: str = Field(..., pattern=r"^[A-Z]{3}-\d{2}$", example="MUE-01")
    descripcion: str = Field(..., min_length=3, example="Muebles de Oficina")
    activo: bool = True


class CategoriaUpdate(BaseModel):
    codigo: Optional[str] = Field(None, pattern=r"^[A-Z]{3}-\d{2}$")
    descripcion: Optional[str] = Field(None, min_length=3)
    activo: Optional[bool] = None


class Categoria(CategoriaBase, table=True):
    __tablename__ = "categorias"
    id: Optional[int] = SQLField(default=None, primary_key=True)


class CategoriaRead(CategoriaBase):
    id: int
