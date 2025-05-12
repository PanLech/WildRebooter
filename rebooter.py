import requests
import time
import subprocess
import configparser
import os
from datetime import datetime
import psutil

CONFIG_PATH = "config.ini"

# === Load Configuration ===
def load_config(path):
    config = configparser.ConfigParser()
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    config.read(path)
    try:
        url = config.get("Settings", "google_doc_url")
        interval = config.getint("Settings", "check_interval_seconds")
        reboot_trigger = config.get("Settings", "trigger_text_reboot")
        stop_trigger = config.get("Settings", "trigger_text_stop")
        process_name = config.get("Settings", "process_to_kill")
        perform_reboot = config.getboolean("Settings", "perform_reboot", fallback=False)
        return url, interval, reboot_trigger, stop_trigger, process_name, perform_reboot
    except Exception as e:
        raise ValueError(f"Invalid config format: {e}")

# === Logging ===
def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logline = f"[{timestamp}] {message}"
    print(logline)
    with open("reboot_trigger.log", "a") as f:
        f.write(logline + "\n")

# === Google Doc Check ===
def get_google_doc_text(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            log_event(f"[!] HTTP Error: {response.status_code}")
    except Exception as e:
        log_event(f"[!] Request failed: {e}")
    return ""

# === Reboot ===
def perform_reboot_action(should_reboot):
    if should_reboot:
        log_event("[!] Trigger detected. Rebooting system via PowerShell...")
        try:
            subprocess.run(["powershell", "-Command", "Restart-Computer -Force"], check=True)
        except subprocess.CalledProcessError as e:
            log_event(f"[!] PowerShell reboot failed: {e}")
    else:
        log_event("[!] Trigger detected. Reboot skipped (perform_reboot = false).")

# === Kill Process ===
def kill_process_by_name(name):
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            try:
                proc.kill()
                log_event(f"[!] Terminated process: {proc.info['name']} (PID {proc.info['pid']})")
                found = True
            except Exception as e:
                log_event(f"[!] Failed to kill {name}: {e}")
    if not found:
        log_event(f"[!] Process '{name}' not found.")

# === MAIN ===
if __name__ == "__main__":
    try:
        url, interval, reboot_trigger, stop_trigger, proc_to_kill, should_reboot = load_config(CONFIG_PATH)
        log_event("Configuration loaded.")
        log_event(f"Monitoring: {url}")
    except Exception as e:
        log_event(f"[!] Config error: {e}")
        exit(1)

    log_event("[*] Performing initial check...")
    initial_text = get_google_doc_text(url)

    if reboot_trigger in initial_text:
        log_event(f"[!] '{reboot_trigger}' already present at launch. No reboot performed.")
        exit(0)
    elif stop_trigger in initial_text:
        log_event(f"[!] '{stop_trigger}' already present at launch. Killing '{proc_to_kill}' once.")
        kill_process_by_name(proc_to_kill)
        exit(0)

    log_event("[+] No trigger at launch. Entering monitoring loop...")

    while True:
        text = get_google_doc_text(url)

        if reboot_trigger in text:
            log_event(f"[!] Detected reboot trigger: '{reboot_trigger}'")
            perform_reboot_action(should_reboot)
            break

        if stop_trigger in text:
            log_event(f"[!] Detected stop trigger: '{stop_trigger}'")
            kill_process_by_name(proc_to_kill)
            # Do not exit — keep monitoring in case process is restarted

        time.sleep(interval)
