# micropip.py
import sys

async def install(package_name, **kwargs):
    print(f"Skipping network lookup... Redirecting local module scan path context for: '{package_name}'")
    return None
