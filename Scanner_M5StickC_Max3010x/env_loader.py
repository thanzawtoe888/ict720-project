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
mqtt_sever = os.getenv("MQTT_SERVER", "default_mqtt_server")
mqtt_port = os.getenv("MQTT_PORT", "default_mqtt_port")
mqtt_domain = os.getenv("MQTT_DOMAIN", "default_mqtt_domain")
mqtt_supscription = os.getenv("MQTT_SUPSCRIPTION", "default_mqtt_supscription")
# Print the loaded values to verify
print(f"Loaded WIFI_SSID: {wifi_ssid}")
print(f"Loaded WIFI_PASSWORD: {wifi_password}")
print(f"Loaded MQTT_SERVER: {mqtt_sever}")
print(f"Loaded MQTT_PORT: {mqtt_port}")
print(f"Loaded MQTT_DOMAIN: {mqtt_domain}")
print(f"Loaded MQTT_SUPSCRIPTION: {mqtt_supscription}")
# Pass them as compiler definitions
env.Append(CPPDEFINES=[
    ("WIFI_SSID", f'\\"{wifi_ssid}\\"'),
    ("WIFI_PASSWORD", f'\\"{wifi_password}\\"'),
    ("MQTT_SERVER", f'\\"{mqtt_sever}\\"'),
    ("MQTT_PORT", f'\\"{mqtt_port}\\"'),
    ("MQTT_DOMAIN", f'\\"{mqtt_domain}\\"'),
    ("MQTT_SUPSCRIPTION", f'\\"{mqtt_supscription}\\"')
])

# Final confirmation print
print("Environment variables added to build.")