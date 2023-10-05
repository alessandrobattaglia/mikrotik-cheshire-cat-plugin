from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel
import os


class RouterSettings(BaseModel):
    router_ip: str
    router_user: str = "admin"
    router_password: str = ""


@plugin
def settings_schema():
    return RouterSettings.schema()


def get_setting(cat, name=None):
    settings = cat.mad_hatter.plugins['mikrotik']

    if name is not None:
        settings = settings.load_settings()
        return settings[name] if name in settings else None

    return settings
