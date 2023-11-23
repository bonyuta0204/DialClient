import socket


def discover_services():
    # SSDP Constants
    SSDP_ADDR = "239.255.255.250"
    SSDP_PORT = 1900
    SSDP_MX = 1
    SSDP_ST = "urn:dial-multiscreen-org:service:dial:1"

    # Construct the SSDP search request
    ssdp_request = (
        "M-SEARCH * HTTP/1.1\r\n"
        "HOST: {}: {}\r\n"
        'MAN: "ssdp:discover"\r\n'
        "MX: {}\r\n"
        "ST: {}\r\n\r\n".format(SSDP_ADDR, SSDP_PORT, SSDP_MX, SSDP_ST)
    )

    # Create a socket for sending the request
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    sock.settimeout(5)
    sock.sendto(ssdp_request.encode(), (SSDP_ADDR, SSDP_PORT))

    services = []

    try:
        # Receive responses
        while True:
            data, addr = sock.recvfrom(1024)
            services.append(parse_response(data.decode()))
    except socket.timeout:
        print("timeout")

    sock.close()

    return services


def parse_response(response_text):
    """
    Parses the SSP response and returns a dictionary of headers.

    :param response_text: A string containing the HTTP response.
    :return: A dictionary where keys are header names and values are header values.
    """
    lines = response_text.split("\n")
    headers = {}

    # Process each line, skipping the first line which is the status line
    for line in lines[1:]:
        if line.strip():  # Check if line is not empty
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

    parsed_response = {}
    parsed_response["location"] = headers.get("LOCATION")
    parsed_response["cache_control"] = headers.get("CACHE-CONTROL")
    parsed_response["usn"] = headers.get("USN")
    parsed_response["WAKEUP"] = headers.get("WAKEUP")

    return parsed_response


if __name__ == "__main__":
    print(discover_services())
