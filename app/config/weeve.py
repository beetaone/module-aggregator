"""
All constants specific to weeve
"""
from app.utils.env import env

WEEVE = {
    "MODULE_NAME": env("MODULE_NAME", "weevagator"),
    "EGRESS_API_HOST": env("EGRESS_API_HOST", "http://localhost:8000"),
    "HANDLER_HOST": env("HANDLER_HOST", "0.0.0.0"),
    "HANDLER_PORT": env("HANDLER_PORT", "80"),
}
