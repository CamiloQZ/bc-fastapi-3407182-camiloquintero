from fastapi import FastAPI, HTTPException

# ============================================
# CONFIGURACIÓN
# ============================================

MESSAGES: dict[str, str] = {
    "es": "Hola {name}, bienvenido a nuestro acuario.",
    "en": "Hello {name}, welcome to our aquarium.",
    "fr": "Bonjour {name}, bienvenue dans notre aquarium.",
}

SUPPORTED_LANGUAGES = list(MESSAGES.keys())

# ============================================
# APP
# ============================================

app = FastAPI(
    title="Acuario API",
    description="API para gestión básica de un acuario",
    version="1.0.0"
)

# ============================================
# RF-01: INFO API
# ============================================

@app.get("/")
async def root() -> dict[str, str]:
    """Información de la API del acuario."""
    return {
        "name": "Acuario API",
        "version": "1.0.0",
        "domain": "acuario"
    }

# ============================================
# RF-02: BIENVENIDA
# ============================================

@app.get("/visitor/{name}")
async def welcome_visitor(
    name: str,
    language: str = "es"
) -> dict[str, str]:
    """Bienvenida personalizada para visitantes del acuario."""

    template = MESSAGES.get(language, MESSAGES["es"])
    message = template.format(name=name)

    return {
        "message": message,
        "visitor": name,
        "language": language if language in MESSAGES else "es"
    }

# ============================================
# RF-03: INFORMACIÓN DE TANQUE
# ============================================

@app.get("/tank/{tank_id}/info")
async def tank_info(
    tank_id: str,
    detail_level: str = "basic"
) -> dict:
    """Información de un tanque del acuario."""

    basic_info = {
        "tank_id": tank_id,
        "status": "activo",
        "species": "peces tropicales"
    }

    if detail_level == "full":
        basic_info.update({
            "temperature": "24°C",
            "capacity": "500 litros",
            "maintenance": "diaria"
        })

    return basic_info

# ============================================
# RF-04: SERVICIO SEGÚN HORARIO
# ============================================

@app.get("/service/schedule")
async def service_schedule(hour: int) -> dict:
    """Disponibilidad del acuario según la hora."""

    if hour < 0 or hour > 23:
        raise HTTPException(status_code=400, detail="Hora inválida (0-23)")

    if 6 <= hour <= 11:
        return {
            "message": "Mañana - Alimentación de peces",
            "available": ["alimentación", "limpieza"]
        }
    elif 12 <= hour <= 17:
        return {
            "message": "Tarde - Exhibiciones abiertas",
            "available": ["exhibiciones", "guías"]
        }
    else:
        return {
            "message": "Noche - Mantenimiento del acuario",
            "available": ["mantenimiento básico"]
        }

# ============================================
# RF-05: HEALTH CHECK
# ============================================

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Estado de la API."""
    return {
        "status": "healthy",
        "domain": "acuario"
    }