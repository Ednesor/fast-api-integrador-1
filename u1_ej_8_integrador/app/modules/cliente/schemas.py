from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str = Field(
        ..., 
        min_length=3, 
        max_length=100,
        example="Juan Pérez",
        description="Nombre del cliente (mínimo 3 caracteres, máximo 100)"
    )
    email: EmailStr = Field(
        ..., 
        example="juan.perez@example.com",
        description="Email válido del cliente"
    )
    telefono: Optional[str] = Field(
        None, 
        min_length=7,
        max_length=20,
        example="555-1234",
        description="Teléfono del cliente (opcional, entre 7 y 20 caracteres)"
    )
    activo: bool = True
    
class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(
        None, 
        min_length=3, 
        max_length=100,
        example="Juan Pérez"
    )
    email: Optional[EmailStr] = Field(
        None, 
        example="juan.perez@example.com"
    )
    telefono: Optional[str] = Field(
        None, 
        min_length=7,
        max_length=20,
        example="555-1234"
    )
    activo: Optional[bool] = None
    
class ClienteRead(ClienteBase):
    id: int  # Contrato de salida: siempre incluye el ID generado
    
class ClienteListResponse(BaseModel):
    clientes: list[ClienteRead]
    total: int