
# 🔁 Wild Remote-Controlled Reboot and Process Killer (via Google Doc)

This Python script monitors a **publicly shared Google Document** for specific trigger words. Based on those triggers, it can:

- 🔄 **Reboot your Windows PC**
- ❌ **Terminate a specific process**

It's ideal for controlled remote intervention without needing direct access to the machine.

---

## ✨ Features

- ✅ Polls a public read-only Google Doc at set intervals
- 🔁 Reboots the PC if `REBOOT` is found
- ❌ Kills a specified process if `KILL` is found
- ⚙️ All settings configurable via `config.ini`
- 📝 Logs all actions to a `reboot_trigger.log` file
- 🧪 Supports safe testing mode (no real reboot)

---

## 📁 Files

| File                     | Description                              |
|--------------------------|------------------------------------------|
| `rebooter.py`            | The main Python script                   |
| `config.ini`             | Configuration file (URL, intervals, etc.)|
| `reboot_trigger.log`     | Log file with timestamps and actions     |

---

## 🛠️ Installation

### 1. Download `rebooter.py` and `config.ini`.

### 2. Make sure Python is installed.

### 3. Install required libraries.

```bash
pip install psutil requests
```

---

## ⚙️ Configuration

Create an empty Google Doc and share it with the following setting: `Anyone on the internet with the link can view`. This way you are the only one that can edit the file, but the script is able to freely read it. 

Create or edit the `config.ini` file:

```ini
[Settings]
google_doc_url = https://docs.google.com/document/d/XXXXXXXXXXXXXXX
check_interval_seconds = 60
trigger_text_reboot = REBOOT
trigger_text_kill = KILL
process_to_kill = rider64.exe
perform_reboot = false
```

### Configuration Options

| Key                   | Description                                           |
|------------------------|-------------------------------------------------------|
| `google_doc_url`      | Public URL of a Google Doc                      |
| `check_interval_seconds` | How often (in seconds) to check the document     |
| `trigger_text_reboot` | Text that triggers a reboot (e.g., `REBOOT`)     |
| `trigger_text_kill`   | Text that triggers process termination (`KILL`)  |
| `process_to_kill`     | Name of the process to terminate (e.g., `rider64.exe`) |
| `perform_reboot`      | If `true`, will reboot; if `false`, logs only        |

---

## 🚀 Usage

Run the script manually:

```bash
python rebooter.py
```
Then keep using the computer. When the computer stops responding, use another machine to add `KILL` to the Google Doc, which will cause the script to kill the configured process (for example `rider64.exe`). If computer is still not responding, add `REBOOT` to the Google Doc for a forceful reboot. Clear the Google Doc after script catches the trigger word.

---

## 🧪 Triggers

Type any of the configured triggers anywhere in your shared Google Doc:

- `REBOOT` → Triggers a system reboot
- `KILL` → Terminates the specified process

> ✅ Reboot only happens once and exits.
>
> 🔁 Process termination can happen multiple times if process is restarted.

---

## 🛡️ Safety and Testing

Set `perform_reboot = false` to test the script safely without actually rebooting the system. The script will log what it **would** have done.

As an additional safety precaution, if reboot trigger is present in Google Doc when the script is started, the script will exit instead of rebooting the computer immediately.

---

## 📝 Log Output Example

```
[2025-05-12 20:44:00] Configuration loaded.
[2025-05-12 20:44:00] Monitoring: https://docs.google.com/document/d/...
[2025-05-12 20:44:01] [*] Performing initial check...
[2025-05-12 20:44:01] [+] No trigger at launch. Entering monitoring loop...
[2025-05-12 20:46:00] [!] Detected kill trigger: 'KILL'
[2025-05-12 20:46:00] [!] Terminated process: rider64.exe (PID 8516)
```

---

## 🧩 License

MIT License — feel free to modify, share, or integrate into your own systems.
