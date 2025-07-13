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
    return servers["servers"]


def save_server_in_file(server_name: str, transport_type: str, url: str):
    """Saves or updates a server in servers/servers.json."""
    servers_file = os.path.join("servers", "servers.json")
    # Ensure valid transport type
    if transport_type not in ["SSE", "Streamable-HTTP"]:
        raise ValueError("Transport type must be either 'SSE' or 'Streamable-HTTP'.")

    # Initialize file if it doesn't exist
    if not os.path.exists(servers_file):
        data = {"servers": {}}
    else:
        with open(servers_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"servers": {}}

    servers = data.get("servers", {})
    # Update or add the server
    servers[server_name] = {
        "TRANSPORT_TYPE": transport_type,
        "URL": url
    }
    data["servers"] = servers

    with open(servers_file, "w") as f:
        json.dump(data, f, indent=4)




def delete_server(server_name: str):
    """Deletes the server with the given name from the servers/servers.json file."""
    servers_file = os.path.join("servers", "servers.json")
    if not os.path.exists(servers_file):
        return

    with open(servers_file, "r") as f:
        data = json.load(f)

    servers = data.get("servers", {})
    if server_name in servers:
        del servers[server_name]
        data["servers"] = servers
        with open(servers_file, "w") as f:
            json.dump(data, f, indent=4)

