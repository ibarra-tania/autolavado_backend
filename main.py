from fastapi import FastAPI
from routes.routes_login import login_router
from routes.routes_rol import rol
from routes.routes_usuario import usuario
from routes.routes_servicio import servicio
from routes.routes_vehiculo import vehiculo
from routes.routes_usuario_vehiculo_servicio import usuario_vehiculo_servicio
from routes.routes_producto import producto                        # ✅ Nuevo

# ─── Configuración del candadito 🔒 en Swagger UI ────────────────────────────
app = FastAPI(
    title="Sistema de Autolavado",
    description="""
## API para gestión de autolavado

### Autenticación
1. Usa el endpoint **`/login`** con tu correo y contraseña
2. Copia el `access_token` que recibes
3. Haz clic en el botón **🔒 Authorize** (arriba a la derecha)
4. Escribe `Bearer <tu_token>` y confirma
5. ¡Listo! Ya puedes usar todos los endpoints protegidos
    """,
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True},
)

# ─── Esquema de seguridad visible en Swagger ──────────────────────────────────
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Aplicar seguridad a todos los endpoints excepto /login
    for path, methods in openapi_schema["paths"].items():
        if path == "/login":
            continue
        for method in methods.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(login_router)                  # 🔐 Ruta pública de login
app.include_router(rol)
app.include_router(usuario)
app.include_router(vehiculo)
app.include_router(servicio)
app.include_router(usuario_vehiculo_servicio)
app.include_router(producto)                      # ✅ Nuevo