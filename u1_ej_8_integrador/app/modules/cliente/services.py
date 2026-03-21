from typing import List, Optional
from .schemas import ClienteCreate, ClienteRead

db_clientes: List[ClienteRead] = []
id_counter = 1

def email_existe(email: str) -> bool:
    """Valida si un email ya está registrado"""
    for c in db_clientes:
        if c.email.lower() == email.lower():
            return True
    return False

def telefono_existe(telefono: Optional[str]) -> bool:
    """Valida si un teléfono ya está registrado"""
    if not telefono:
        return False
    for c in db_clientes:
        if c.telefono and c.telefono.lower() == telefono.lower():
            return True
    return False

def crear(data: ClienteCreate) -> dict:
    """
    Crea un nuevo cliente validando unicidad de email y teléfono.
    Retorna un diccionario con 'success', 'cliente' y opcionalmente 'errores'
    """
    global id_counter
    errores = []
    
    # Validar email único
    if email_existe(data.email):
        errores.append({
            "campo": "email",
            "mensaje": f"El email '{data.email}' ya está registrado"
        })
    
    # Validar teléfono único (si se proporciona)
    if data.telefono and telefono_existe(data.telefono):
        errores.append({
            "campo": "telefono",
            "mensaje": f"El teléfono '{data.telefono}' ya está registrado"
        })
    
    # Si hay errores, retornar
    if errores:
        return {"success": False, "errores": errores}
    
    # Crear cliente si no hay errores
    nuevo = ClienteRead(id=id_counter, **data.model_dump())
    db_clientes.append(nuevo)
    id_counter += 1
    return {"success": True, "cliente": nuevo}
  
def obtener_todos(skip: int, limit: int) -> List[ClienteRead]:
    return db_clientes[skip : skip + limit]
  
def obtener_por_id(id: int) -> Optional[ClienteRead]:
    for c in db_clientes:
        if c.id == id:
            return c
    return None
  
def actualizar_total(id: int, data: ClienteCreate) -> Optional[ClienteRead]:
    # Reemplazo total: Requiere todos los campos validables (ClienteCreate)
    for index, c in enumerate(db_clientes):
        if c.id == id:
            cliente_actualizado = ClienteRead(id=id, **data.model_dump())
            db_clientes[index] = cliente_actualizado
            return cliente_actualizado
    return None
  
def desactivar(id: int) -> Optional[ClienteRead]:
    # Borrado lógico: Solo altera el estado 'activo'
    for index, c in enumerate(db_clientes):
        if c.id == id:
            c_dict = c.model_dump()
            c_dict["activo"] = False
            cliente_actualizado = ClienteRead(**c_dict)
            db_clientes[index] = cliente_actualizado
            return cliente_actualizado
    return None