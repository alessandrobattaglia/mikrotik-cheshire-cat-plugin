from cat.mad_hatter.decorators import tool, plugin
from pydantic import BaseModel
import requests
import json
from requests.auth import HTTPBasicAuth


class RouterSettings(BaseModel):
    router_ip: str
    router_user: str = "admin"
    router_password: str = ""


@plugin
def settings_schema():
    return RouterSettings.schema()


def get_setting(cat, name):
    settings = cat.mad_hatter.plugins['mikrotik'].load_settings()

    return settings[name] if name in settings else None


def load_auth(cat):
    return HTTPBasicAuth(get_setting(cat, "router_user"), get_setting(cat, "router_password"))


def perform(url, auth):
    return requests.get(url, auth=auth, verify=False).json()


@tool(return_direct=False)
def mikrotik_info(tool_input, cat):
    """This tool returns the info of the mikrotik router. Replies to "get the info of the mikrotik router". Input is
    always None."""

    return str(perform("https://" + get_setting(cat, "router_ip") + "/rest/system/resource", load_auth(cat)))


def map_interface(interface):
    return {
        'id': interface['.id'],
        'default-name': interface['default-name'] if 'default-name' in interface else None,
        'name': interface['name'],
        'running': interface['running'],
        'disabled': interface['disabled'],
        'mac-address': interface['mac-address'] if 'mac-address' in interface else None
    }


@tool(return_direct=False)
def mikrotik_interfaces(tool_input, cat):
    """This tool returns the list of the interfaces of the mikrotik router. Replies to "get the list of interfaces of
    the mikrotik router". Input is always None."""

    return str(json.dumps(list(map(
        map_interface,
        perform("https://" + get_setting(cat, "router_ip") + "/rest/interface", load_auth(cat))
    ))))
