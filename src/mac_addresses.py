from cat.mad_hatter.decorators import tool
from cat.log import log

import os
import json


class MacAddresses:
    def __init__(self, file_name="mac_addresses.json", directory_path="cat/plugins/mikrotik/db"):
        self._directory_path = directory_path
        self._file_name = file_name
        self._mac_addresses = []

        self.load()

    def load(self):
        file_name = os.path.join(self._directory_path, self._file_name)

        if os.path.isfile(file_name):
            try:
                with open(file_name, "r") as file:
                    self._mac_addresses = json.load(file)
            except Exception as e:
                log.error(f"Unable to load mac addresses database")
                log.error(e)
        else:
            self.save()

    def save(self):
        if not os.path.exists(self._directory_path):
            os.makedirs(self._directory_path)

        file_name = os.path.join(self._directory_path, self._file_name)

        try:
            if self._mac_addresses is None:
                self._mac_addresses = []

            with open(file_name, "w") as file:
                json.dump(self._mac_addresses, file)
        except Exception as e:
            log.error(f"Unable to save on mac addresses database")
            log.error(e)

    def get(self, name):
        items = [item for item in self._mac_addresses if item["name"] == name]

        if len(items) == 1:
            return items[0]

        return None

    def set(self, value, name):
        for item in self._mac_addresses:
            if item["name"] == name:
                item["mac_address"] = value

                return item

        item = {
            "name": name,
            "mac_address": value,
        }

        self._mac_addresses.append(item)

    def remove(self, name):
        item = self.get(name)

        if item is not None:
            self._mac_addresses.remove(item)

            return item

        return None


mac_addresses = MacAddresses()


def entity_to_mac(entity):
    mac_address = mac_addresses.get(entity)

    if mac_address is None:
        return None

    return mac_address["mac_address"] if "mac_address" in mac_address else None


@tool(return_direct=False)
def mac_get(entity, cat):
    """This tool returns the mac address of the entity. Replies to "get the mac address of the entity". Input is the
    entity."""

    mac_address = entity_to_mac(entity)

    if mac_address is None:
        return "I do not know who {entity} is, tell me about"

    return f"The mac address is {mac_address}"


@tool(return_direct=False)
def mac_get(input, cat):
    """This tool adds a mac address of an entity in the list. Replies to "add the mac address of the entity". Inputs
    are two values separated with a minus: the first one is the entity; the second one is the mac address."""

    entity, mac_address = input.split("-")

    mac_addresses.set(mac_address, entity)
    mac_addresses.save()

    return "Ok, got it!"
