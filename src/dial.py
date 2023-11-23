from ssdp import discover_services
import xmltodict
from pprint import pprint

import requests


def get_dial_services():
    """Return a list of DIAL services found on the network."""
    services = discover_services()

    def add_detaild_service_info(service):
        location = service["location"]
        r = requests.get(location)
        service["application_url"] = r.headers["Application-URL"]
        service["device_description"] = xmltodict.parse(r.content)
        return service

    return list(map(add_detaild_service_info, services))


if __name__ == "__main__":
    pprint(get_dial_services())
