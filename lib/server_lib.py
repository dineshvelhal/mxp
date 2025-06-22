import json
import os


def get_servers():
    """ Get the list of saved MCP servers"""
    # load json from servers/servers.json

    servers_file = os.path.join("servers", "servers.json")
    if not os.path.exists(servers_file):
        return []
    with open(servers_file, "r") as f:
        servers = json.load(f)
    return servers

def save_server_in_file(server_name: str, transport_type: str, url: str):
    """Saves the server as a JSON object in the servers/servers.json file.
    If the server with this name already exists, it updates the existing server."""
    servers_file = os.path.join("servers", "servers.json")
    if not os.path.exists(servers_file):
        with open(servers_file, "w") as f:
            json.dump([], f)

    if transport_type not in ["SSE", "Streamable-HTTP"]:
        raise ValueError("Transport type must be either 'SSE' or 'Streamable-HTTP'.")

    with open(servers_file, "r") as f:
        servers = json.load(f)

    # Check if the server already exists
    for server in servers:
        if server["NAME"] == server_name:
            server["TRANSPORT_TYPE"] = transport_type
            server["URL"] = url
            break
    else:
        # If the server does not exist, add it
        servers.append({
            "NAME": server_name,
            "TRANSPORT_TYPE": transport_type,
            "URL": url
        })

    with open(servers_file, "w") as f:
        json.dump(servers, f, indent=4)


def delete_server(server_name: str):
    """Deletes the server with the given name from the servers/servers.json file."""
    servers_file = os.path.join("servers", "servers.json")
    if not os.path.exists(servers_file):
        return

    with open(servers_file, "r") as f:
        servers = json.load(f)

    # Filter out the server to be deleted
    servers = [server for server in servers if server["NAME"] != server_name]

    with open(servers_file, "w") as f:
        json.dump(servers, f, indent=4)