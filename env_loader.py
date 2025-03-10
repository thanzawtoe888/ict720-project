Import("env")

print("Running env_loader.py...")

# List installed packages
env.Execute("$PYTHONEXE -m pip list")

# Try importing the python-dotenv package
try:
    import dotenv
except ImportError:
    # If the package is not found, install it
    env.Execute("$PYTHONEXE -m pip install python-dotenv")


import os
from dotenv import load_dotenv

# # Load .env file
env_path = os.path.join(os.getcwd(), ".env")
load_dotenv(env_path)

# Read variables
wifi_ssid = os.getenv("WIFI_SSID", "default_ssid")
wifi_password = os.getenv("WIFI_PASSWORD", "default_password")

# Print the loaded values to verify
print(f"Loaded WIFI_SSID: {wifi_ssid}")
print(f"Loaded WIFI_PASSWORD: {wifi_password}")

# Pass them as compiler definitions
env.Append(CPPDEFINES=[
    ("WIFI_SSID", f'\\"{wifi_ssid}\\"'),
    ("WIFI_PASSWORD", f'\\"{wifi_password}\\"')
])

# Final confirmation print
print("Environment variables added to build.")