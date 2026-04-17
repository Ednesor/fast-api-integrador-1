from typing import List, Optional
from sqlmodel import Session, select
from .schemas import Categoria, CategoriaCreate, CategoriaRead


def crear(data: CategoriaCreate, session: Session) -> CategoriaRead:
    nueva = Categoria(**data.model_dump())
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return CategoriaRead.from_orm(nueva)


def obtener_todas(skip: int = 0, limit: int = 10, session: Session = None) -> List[CategoriaRead]:
    statement = select(Categoria).offset(skip).limit(limit)
    categorias = session.exec(statement).all()
    return [CategoriaRead.from_orm(c) for c in categorias]


def obtener_por_id(id: int, session: Session = None) -> Optional[CategoriaRead]:
    categoria = session.get(Categoria, id)
    if categoria:
        return CategoriaRead.from_orm(categoria)
    return None


def actualizar_total(id: int, data: CategoriaCreate, session: Session) -> Optional[CategoriaRead]:
    categoria = session.get(Categoria, id)
    if not categoria:
        return None
    
    categoria.codigo = data.codigo
    categoria.descripcion = data.descripcion
    categoria.activo = data.activo
    
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return CategoriaRead.from_orm(categoria)


def desactivar(id: int, session: Session) -> Optional[CategoriaRead]:
    categoria = session.get(Categoria, id)
    if not categoria:
        return None
    
    categoria.activo = False
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return CategoriaRead.from_orm(categoria)
