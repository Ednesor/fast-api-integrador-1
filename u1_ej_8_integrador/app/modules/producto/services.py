from typing import List, Optional
from sqlmodel import Session, select
from .schemas import Producto, ProductoCreate, ProductoRead


def crear(data: ProductoCreate, session: Session) -> ProductoRead:
    nuevo = Producto(**data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return ProductoRead.from_orm(nuevo)


def obtener_todos(skip: int, limit: int, session: Session = None) -> List[ProductoRead]:
    statement = select(Producto).offset(skip).limit(limit)
    productos = session.exec(statement).all()
    return [ProductoRead.from_orm(p) for p in productos]


def obtener_por_id(id: int, session: Session = None) -> Optional[ProductoRead]:
    producto = session.get(Producto, id)
    if producto:
        return ProductoRead.from_orm(producto)
    return None


def actualizar_total(id: int, data: ProductoCreate, session: Session) -> Optional[ProductoRead]:
    # Reemplazo total: Requiere todos los campos validables (ProductoCreate)
    producto = session.get(Producto, id)
    if not producto:
        return None
    
    producto.nombre = data.nombre
    producto.categoria = data.categoria
    producto.precio = data.precio
    producto.stock = data.stock
    producto.stock_minimo = data.stock_minimo
    producto.activo = data.activo
    
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return ProductoRead.from_orm(producto)


def desactivar(id: int, session: Session) -> Optional[ProductoRead]:
    # Borrado lógico: Solo altera el estado 'activo'
    producto = session.get(Producto, id)
    if not producto:
        return None
    
    producto.activo = False
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return ProductoRead.from_orm(producto)


def obtener_estado_stock(id: int, session: Session) -> Optional[dict]:
    producto = obtener_por_id(id, session)
    if not producto:
        return None

    # La lógica de negocio vive aquí
    alerta_stock = producto.stock < producto.stock_minimo

    return {
        "stock": producto.stock,
        "bajo_stock_minimo": alerta_stock,
        "activo": producto.activo,
    }
