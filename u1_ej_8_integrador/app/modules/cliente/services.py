from typing import List, Optional
from sqlmodel import Session, select
from .schemas import Cliente, ClienteCreate, ClienteRead

def email_existe(email: str, session: Session) -> bool:
    """Valida si un email ya está registrado"""
    statement = select(Cliente).where(Cliente.email == email)
    return session.exec(statement).first() is not None

def telefono_existe(telefono: Optional[str], session: Session) -> bool:
    """Valida si un teléfono ya está registrado"""
    if not telefono:
        return False
    statement = select(Cliente).where(Cliente.telefono == telefono)
    return session.exec(statement).first() is not None

def crear(data: ClienteCreate, session: Session) -> dict:
    """
    Crea un nuevo cliente validando unicidad de email y teléfono.
    Retorna un diccionario con 'success', 'cliente' y opcionalmente 'errores'
    """
    errores = []
    
    # Validar email único
    if email_existe(data.email, session):
        errores.append({
            "campo": "email",
            "mensaje": f"El email '{data.email}' ya está registrado"
        })
    
    # Validar teléfono único (si se proporciona)
    if data.telefono and telefono_existe(data.telefono, session):
        errores.append({
            "campo": "telefono",
            "mensaje": f"El teléfono '{data.telefono}' ya está registrado"
        })
    
    # Si hay errores, retornar
    if errores:
        return {"success": False, "errores": errores}
    
    # Crear cliente si no hay errores
    nuevo = Cliente(**data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return {"success": True, "cliente": ClienteRead.from_orm(nuevo)}
  
def obtener_todos(skip: int, limit: int, session: Session = None) -> List[ClienteRead]:
    statement = select(Cliente).offset(skip).limit(limit)
    clientes = session.exec(statement).all()
    return [ClienteRead.from_orm(c) for c in clientes]
  
def obtener_por_id(id: int, session: Session = None) -> Optional[ClienteRead]:
    cliente = session.get(Cliente, id)
    if cliente:
        return ClienteRead.from_orm(cliente)
    return None
  
def actualizar_total(id: int, data: ClienteCreate, session: Session) -> Optional[ClienteRead]:
    cliente = session.get(Cliente, id)
    if not cliente:
        return None
    
    cliente.nombre = data.nombre
    cliente.email = data.email
    cliente.telefono = data.telefono
    cliente.activo = data.activo
    
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return ClienteRead.from_orm(cliente)
  
def desactivar(id: int, session: Session) -> Optional[ClienteRead]:
    cliente = session.get(Cliente, id)
    if not cliente:
        return None
    
    cliente.activo = False
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return ClienteRead.from_orm(cliente)