import platform
import subprocess
import re

def get_system_ram_gb() -> float:
    """Securely scans local hardware specs without sending data outward."""
    try:
        if platform.system() == "Darwin":
            mem_bytes = int(subprocess.check_output(['sysctl', '-n', 'hw.memsize']).strip())
            return mem_bytes / (1024**3)
        elif platform.system() == "Linux":
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if 'MemTotal' in line:
                        return int(line.split()[1]) / (1024**2)
    except Exception:
        pass
    return 8.0 # Safe fallback

def estimate_ram_required(model_name: str) -> float:
    """Estimates RAM footprint based on parameter count."""
    match = re.search(r'([0-9]+(?:\.[0-9]+)?)b', model_name.lower())
    if match:
        params = float(match.group(1))
        return params * 0.7 
    return 100.0