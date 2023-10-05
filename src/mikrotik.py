from cat.mad_hatter.decorators import tool
from cat.plugins.mikrotik.src.mac_addresses import entity_to_mac
from cat.plugins.mikrotik.settings import get_setting
from cat.plugins.mikrotik.utils.request import Request, load_mikrotik_auth
import json


@tool(return_direct=False)
def mikrotik_info(input, cat):
    """This tool returns the info of the mikrotik router. Replies to "get the info of the mikrotik router". Input is
    always None."""

    request = Request("https://" + get_setting(cat, "router_ip"), load_mikrotik_auth(cat))

    return str(request.perform("/rest/system/resource"))


@tool(return_direct=False)
def mikrotik_interfaces(input, cat):
    """This tool returns the list of the interfaces of the mikrotik router. Replies to "get the list of interfaces of
    the mikrotik router". Input is always None."""

    request = Request("https://" + get_setting(cat, "router_ip"), load_mikrotik_auth(cat))

    return str(json.dumps(list(map(
        lambda interface: {
            'id': interface['.id'],
            'default-name': interface['default-name'] if 'default-name' in interface else None,
            'name': interface['name'],
            'running': interface['running'],
            'disabled': interface['disabled'],
            'mac-address': interface['mac-address'] if 'mac-address' in interface else None
        },
        request.perform("/rest/interface")
    ))))


def get_devices(cat):
    request = Request("https://" + get_setting(cat, "router_ip"), load_mikrotik_auth(cat))

    return map(
        lambda interface: {
            'id': interface['.id'],
            'address': interface['address'],
            'disabled': interface['disabled'],
            'host-name': interface['host-name'] if 'host-name' in interface else None,
            'last-seen': interface['last-seen'] if 'last-seen' in interface else None,
            'mac-address': interface['mac-address'] if 'mac-address' in interface else None,
            'server': interface['server'],
            'status': interface['status']
        },
        request.perform("/rest/ip/dhcp-server/lease")
    )


@tool(return_direct=False)
def mikrotik_devices(input, cat):
    """This tool returns the list of the devices of the mikrotik router. Replies to "get the list of the devices of
    the mikrotik router". Input is always None."""

    return str(json.dumps(list(get_devices(cat))))


@tool(return_direct=False)
def mikrotik_status_devices(status, cat):
    """This tool returns the list of the devices with a specific status of the mikrotik router. Replies to "get the
    list of the devices of the mikrotik router with status bound/waiting". Input is the status."""

    return str(json.dumps(list(filter(
        lambda interface: interface['status'] == status,
        get_devices(cat)
    ))))


@tool(return_direct=False)
def is_connected(entity, cat):
    """This tool returns if a person is at home. The input is the person alias (the name or the nickname). Use when
    the user says something like: 'Is mum at home?' or 'Is Andrea at home?'"""

    devices = get_devices(cat)

    devices = filter(
        lambda interface: interface["status"] == "bound",
        devices
    )

    devices = map(
        lambda interface: interface["mac-address"],
        devices
    )

    devices = filter(
        lambda address: address is not None,
        devices
    )

    mac = entity_to_mac(entity)

    return f"yes, {entity} is at home" if mac is not None and mac in devices else f"no, {entity} is not at home"
