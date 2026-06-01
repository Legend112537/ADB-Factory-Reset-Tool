def validate_ip(ip: str) -> bool:
    """Basic IP validation."""
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or int(part) > 255:
            return False
    return True

def load_devices(filename: str = "devices.json") -> list:
    """Load known devices from a JSON file."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []
