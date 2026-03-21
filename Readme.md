# 🚀 FastAPI Backend - Unidad 1

Proyecto completo de API RESTful con FastAPI, implementando conceptos de Path, Query, Body, Pydantic y manejo de errores.

## 📁 Estructura del Proyecto

```
fastapi_backend/
├── u_01/                          # Ejercicios iniciales (1-7)
│   ├── u1_ej1, u1_ej2, ... u1_ej7
├── u1_ej_8_integrador/            # Proyecto integrador FINAL
│   └── app/
│       ├── main.py                # Punto de entrada
│       ├── modules/               # Módulos organizados por dominio
│       │   ├── cliente/           # ✨ Gestión de Clientes
│       │   ├── producto/          # Gestión de Productos
│       │   └── categoria/         # Gestión de Categorías
│       └── __init__.py
├── requirements.txt               # Dependencias del proyecto
├── ENTREGA_INFORME.md            # Informe detallado de entrega
└── Readme.md
```

## 🎯 Funcionalidad Implementada

### Módulo de Cliente (NUEVO)
- ✅ Crear cliente (POST `/clientes`)
- ✅ Listar clientes con paginación (GET `/clientes`)
- ✅ Obtener detalle de cliente (GET `/clientes/{id}`)
- ✅ Actualizar cliente (PUT `/clientes/{id}`)
- ✅ Desactivar cliente (PUT `/clientes/{id}/desactivar`)

### Módulo de Producto
- Crear, listar, obtener, actualizar y desactivar productos
- Consultar estado de stock

### Módulo de Categoría
- Crear, listar, obtener, actualizar y desactivar categorías

## 🛠️ Instalación y Uso

### 1. Activar entorno virtual

En directorio: `fastapi_backend`

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el servidor

```bash
cd u1_ej_8_integrador/app
python -m fastapi dev main.py
```

### 4. Acceder a la API

- **Swagger UI (Documentación interactiva):** http://localhost:8000/docs
- **ReDoc (Documentación alternativa):** http://localhost:8000/redoc
- **API Base:** http://localhost:8000

## 📚 Ejemplos de Uso

### Crear un Cliente

```bash
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan.perez@example.com",
    "telefono": "555-1234"
  }'
```

**Response:**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan.perez@example.com",
  "telefono": "555-1234",
  "activo": true
}
```

### Listar Clientes

```bash
curl http://localhost:8000/clientes?skip=0&limit=10
```

### Obtener Detalle de Cliente

```bash
curl http://localhost:8000/clientes/1
```

### Actualizar Cliente

```bash
curl -X PUT http://localhost:8000/clientes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez Actualizado",
    "email": "juan.nuevo@example.com",
    "telefono": "555-9999",
    "activo": true
  }'
```

### Desactivar Cliente

```bash
curl -X PUT http://localhost:8000/clientes/1/desactivar
```

## 🏗️ Arquitectura

El proyecto utiliza arquitectura **MVC Modular**:

- **Models (Schemas)**: Validación de datos con Pydantic
- **Views (Routers)**: Endpoints HTTP con documentación
- **Controllers (Services)**: Lógica de negocio

Cada módulo es independiente y reutilizable.

## 📊 Validaciones Implementadas

### Nivel 1: Validación de Datos (Pydantic)
- ✅ Nombre: 3-100 caracteres
- ✅ Email: formato válido
- ✅ Teléfono: 7-20 caracteres (opcional)
- ❌ Errores → HTTP 422

### Nivel 2: Validación de Unicidad (Lógica de Negocio)
- ✅ Email único por cliente (case-insensitive)
- ✅ Teléfono único por cliente (case-insensitive)
- ✅ Múltiples clientes pueden no tener teléfono
- ❌ Duplicados → HTTP 409 Conflict

**Ejemplo de Error por Duplicación:**
```json
{
  "detail": {
    "mensaje": "El cliente no pudo ser creado por duplicación de datos",
    "errores": [
      {
        "campo": "email",
        "mensaje": "El email 'juan.perez@example.com' ya está registrado"
      }
    ]
  }
}
```

## 📝 Archivo requirements.txt

```
fastapi[standard]
httpx
```

**Nota**: `fastapi[standard]` incluye `uvicorn`, `pydantic`, y otras dependencias necesarias.

## 🧪 Pruebas

Se incluye un script de pruebas completo:

```bash
python test_validaciones.py    # 14 casos de validación Pydantic
python test_unicidad.py        # 10 casos de unicidad de datos
python test_endpoints.py       # Pruebas CRUD completas
```

Este script valida:
- ✅ Casos válidos (201, 200)
- ✅ Casos inválidos (422, 409, 404)
- ✅ Manejo de errores

## ✨ Conceptos Implementados

- ✅ Path Parameters (ej: `/clientes/{id}`)
- ✅ Query Parameters (ej: `?skip=0&limit=10`)
- ✅ Request Body (validado con Pydantic)
- ✅ Validación de datos automática (Pydantic)
- ✅ Validación de unicidad de negocio (email, telefono)
- ✅ Manejo de errores HTTP (404, 422, 409)
- ✅ Paginación
- ✅ Borrado lógico (activación/desactivación)
- ✅ Documentación automática con Swagger

## 📚 Documentación Adicional

- **[ENTREGA_FINAL.md](ENTREGA_FINAL.md)** - Informe completo con ejemplos
- **[UNICIDAD_DOCUMENTACION.md](UNICIDAD_DOCUMENTACION.md)** - Validación de email/telefono único
- **[VALIDACIONES_DOCUMENTACION.md](VALIDACIONES_DOCUMENTACION.md)** - Validación de formato

## 📊 Validaciones Implementadas

### Clientes
- `nombre`: Requerido (string)
- `email`: Requerido (string con formato email)
- `telefono`: Opcional (string)
- `activo`: Booleano con valor por defecto `true`

### Productos
- `nombre`: Requerido
- `categoria`: Requerido con patrón `^[A-Z]{3}-\d{2}$`
- `precio`: Requerido (float > 0)
- `stock`: Requerido (int ≥ 0)
- `stock_minimo`: Requerido (int ≥ 0)
- `activo`: Booleano

### Categorías
- `codigo`: Requerido con patrón `^[A-Z]{3}-\d{2}$`
- `descripcion`: Requerido (min 3 caracteres)
- `activo`: Booleano

## 🔗 Repositorio GitHub

El proyecto se encuentra disponible en: [github.com/usuario/fastapi_backend](https://github.com/usuario/fastapi_backend)

## 📄 Documentación Adicional

Ver el archivo `ENTREGA_INFORME.md` para:
- Descripción detallada de funcionalidad
- Ejemplos de request/response completos
- Casos de error documentados
- Verificación en Swagger

---

**Última actualización:** 21 de Marzo, 2026  
**Versión:** 1.0.0  
**Estado:** ✅ COMPLETADO
