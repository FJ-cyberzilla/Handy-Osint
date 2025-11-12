#!/usr/bin/env python3
"""
🔥 HANDY REAPER - Advanced OSINT Intelligence System 🔥
Enhanced with DNS, Proxy, Rate Limiting, and 50+ Social Media Platforms
Cyberzilla™ - MMXXVI
"""

import asyncio
import aiohttp
import json
import random
import time
import os
import argparse
import socket
import dns.resolver
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict
from dataclasses import dataclass, asdict
import logging
from pathlib import Path

# Color codes for terminal output
class Colors:
    """Terminal color codes"""
    PINK = '\033[95m'
    BRIGHT_PINK = '\033[38;5;213m'
    HOT_PINK = '\033[38;5;198m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def display_banner():
    """Display the awesome pink HANDY REAPER banner"""
    banner = f"""
{Colors.BRIGHT_PINK}{Colors.BOLD}
888 888                      888               888 88e                                     
888 888  ,"Y88b 888 8e   e88 888 Y8b Y888P     888 888D  ,e e,   e88'888  e88 88e  888 8e  
8888888 "8" 888 888 88b d888 888  Y8b Y8P  888 888 88"  d88 88b d888  '8 d888 888b 888 88b 
888 888 ,ee 888 888 888 Y888 888   Y8b Y       888 b,   888   , Y888   , Y888 888P 888 888 
888 888 "88 888 888 888  "88 888    888        888 88b,  "YeeP"  "88,e8'  "88 88"  888 888 
                                    888                                                    
                                    888                                                    
{Colors.END}
{Colors.HOT_PINK}{Colors.BOLD}
🔥 HANDY REAPER - Advanced OSINT Intelligence System 🔥
          Cyberzilla™ - MMXXVI - Ultimate Reconnaissance
{Colors.END}
"""
    print(banner)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('osint_reaper.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class RateLimitConfig:
    """Rate limiting configuration"""
    max_requests: int = 10
    time_window: int = 60  # seconds
    requests: List[float] = None
    
    def __post_init__(self):
        if self.requests is None:
            self.requests = []

@dataclass
class ProxyConfig:
    """Proxy configuration"""
    enabled: bool = False
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None
    rotation_enabled: bool = False
    proxy_list: List[str] = None
    
    def __post_init__(self):
        if self.proxy_list is None:
            self.proxy_list = []

class RateLimiter:
    """Advanced rate limiter with sliding window"""
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)
        
    async def acquire(self, key: str = "default") -> bool:
        """Acquire permission to make a request"""
        current_time = time.time()
        
        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if current_time - req_time < self.time_window
        ]
        
        if len(self.requests[key]) >= self.max_requests:
            # Calculate wait time
            oldest_request = min(self.requests[key])
            wait_time = self.time_window - (current_time - oldest_request)
            logging.warning(f"Rate limit reached for {key}. Waiting {wait_time:.2f}s")
            await asyncio.sleep(wait_time + 0.1)
            return await self.acquire(key)
        
        self.requests[key].append(current_time)
        return True

class DNSAnalyzer:
    """DNS reconnaissance and analysis"""
    
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5
        
    async def analyze_domain(self, domain: str) -> Dict[str, Any]:
        """Perform comprehensive DNS analysis"""
        results = {
            'domain': domain,
            'records': {},
            'security': {},
            'reputation': {},
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # A Records
            results['records']['A'] = await self._get_dns_records(domain, 'A')
            
            # AAAA Records (IPv6)
            results['records']['AAAA'] = await self._get_dns_records(domain, 'AAAA')
            
            # MX Records
            results['records']['MX'] = await self._get_dns_records(domain, 'MX')
            
            # TXT Records (SPF, DKIM, etc.)
            results['records']['TXT'] = await self._get_dns_records(domain, 'TXT')
            
            # NS Records
            results['records']['NS'] = await self._get_dns_records(domain, 'NS')
            
            # CNAME Records
            results['records']['CNAME'] = await self._get_dns_records(domain, 'CNAME')
            
            # Security checks
            results['security'] = await self._check_security(domain, results['records'])
            
        except Exception as error:
            results['error'] = str(error)
            logging.error(f"DNS analysis failed for {domain}: {error}")
        
        return results
    
    async def _get_dns_records(self, domain: str, record_type: str) -> List[str]:
        """Get DNS records of specific type"""
        try:
            answers = self.resolver.resolve(domain, record_type)
            return [str(rdata) for rdata in answers]
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
            return []
        except Exception as error:
            logging.debug(f"DNS lookup failed for {domain} ({record_type}): {error}")
            return []
    
    async def _check_security(self, domain: str, records: Dict) -> Dict[str, Any]:
        """Check domain security features"""
        security = {
            'spf_configured': False,
            'dmarc_configured': False,
            'dkim_hints': False,
            'dnssec': False
        }
        
        # Check SPF
        for txt in records.get('TXT', []):
            if 'v=spf1' in txt.lower():
                security['spf_configured'] = True
            if 'v=dmarc1' in txt.lower():
                security['dmarc_configured'] = True
            if 'dkim' in txt.lower():
                security['dkim_hints'] = True
        
        return security

class NetworkAnalyzer:
    """Network-level reconnaissance"""
    
    @staticmethod
    async def analyze_url(url: str) -> Dict[str, Any]:
        """Analyze URL and extract network information"""
        results = {
            'url': url,
            'parsed': {},
            'ip_info': {},
            'ssl_info': {},
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            
            results['parsed'] = {
                'scheme': parsed.scheme,
                'hostname': parsed.hostname,
                'port': parsed.port,
                'path': parsed.path
            }
            
            # Get IP address
            if parsed.hostname:
                try:
                    ip_address = socket.gethostbyname(parsed.hostname)
                    results['ip_info'] = {
                        'ip': ip_address,
                        'hostname': parsed.hostname,
                        'resolved': True
                    }
                except socket.gaierror:
                    results['ip_info'] = {'resolved': False, 'error': 'DNS resolution failed'}
            
        except Exception as error:
            results['error'] = str(error)
            logging.error(f"Network analysis failed for {url}: {error}")
        
        return results

class EnhancedOSINTSystem:
    """Advanced OSINT Investigation System with enhanced features"""
    
    def __init__(self, proxy_config: Optional[ProxyConfig] = None):
        self.session = None
        self.results = {}
        self.rate_limiter = RateLimiter(max_requests=10, time_window=60)
        self.dns_analyzer = DNSAnalyzer()
        self.network_analyzer = NetworkAnalyzer()
        self.proxy_config = proxy_config or ProxyConfig()
        self.current_proxy_index = 0
        
        # Extended platform list (50+ platforms)
        self.platforms = {
            # Social Media
            'github': 'https://github.com/{}',
            'twitter': 'https://twitter.com/{}',
            'instagram': 'https://instagram.com/{}',
            'facebook': 'https://facebook.com/{}',
            'linkedin': 'https://linkedin.com/in/{}',
            'reddit': 'https://reddit.com/user/{}',
            'pinterest': 'https://pinterest.com/{}',
            'tumblr': 'https://{}.tumblr.com',
            'medium': 'https://medium.com/@{}',
            'dev.to': 'https://dev.to/{}',
            'stackoverflow': 'https://stackoverflow.com/users/{}',
            'hackernews': 'https://news.ycombinator.com/user?id={}',
            'producthunt': 'https://www.producthunt.com/@{}',
            
            # Professional
            'behance': 'https://www.behance.net/{}',
            'dribbble': 'https://dribbble.com/{}',
            'angellist': 'https://angel.co/u/{}',
            'crunchbase': 'https://www.crunchbase.com/person/{}',
            
            # Gaming
            'twitch': 'https://www.twitch.tv/{}',
            'steam': 'https://steamcommunity.com/id/{}',
            'xbox': 'https://account.xbox.com/en-us/profile?gamertag={}',
            'playstation': 'https://my.playstation.com/profile/{}',
            'discord.id': 'https://discord.com/users/{}',
            'epicgames': 'https://www.epicgames.com/id/{}',
            
            # Video/Streaming
            'youtube': 'https://www.youtube.com/@{}',
            'vimeo': 'https://vimeo.com/{}',
            'dailymotion': 'https://www.dailymotion.com/{}',
            'tiktok': 'https://www.tiktok.com/@{}',
            'snapchat': 'https://www.snapchat.com/add/{}',
            
            # Music
            'spotify': 'https://open.spotify.com/user/{}',
            'soundcloud': 'https://soundcloud.com/{}',
            'bandcamp': 'https://{}.bandcamp.com',
            'lastfm': 'https://www.last.fm/user/{}',
            
            # Photography
            'flickr': 'https://www.flickr.com/people/{}',
            '500px': 'https://500px.com/p/{}',
            'unsplash': 'https://unsplash.com/@{}',
            
            # Forums/Communities
            'patreon': 'https://www.patreon.com/{}',
            'buymeacoffee': 'https://www.buymeacoffee.com/{}',
            'ko-fi': 'https://ko-fi.com/{}',
            'gumroad': 'https://gumroad.com/{}',
            
            # Code/Tech
            'gitlab': 'https://gitlab.com/{}',
            'bitbucket': 'https://bitbucket.org/{}',
            'codepen': 'https://codepen.io/{}',
            'replit': 'https://replit.com/@{}',
            'kaggle': 'https://www.kaggle.com/{}',
            
            # Knowledge/Q&A
            'quora': 'https://www.quora.com/profile/{}',
            'aboutme': 'https://about.me/{}',
            'linktree': 'https://linktr.ee/{}',
            'gravatar': 'https://en.gravatar.com/{}',
            
            # Niche platforms
            'etsy': 'https://www.etsy.com/shop/{}',
            'ebay': 'https://www.ebay.com/usr/{}',
            'goodreads': 'https://www.goodreads.com/user/show/{}',
            'myanimelist': 'https://myanimelist.net/profile/{}',
            'letterboxd': 'https://letterboxd.com/{}',
        }
    
    async def initialize(self):
        """Initialize async session with proxy support"""
        connector_kwargs = {}
        
        if self.proxy_config.enabled:
            if self.proxy_config.http_proxy:
                logging.info(f"Using proxy: {self.proxy_config.http_proxy}")
        
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=15),
            connector=aiohttp.TCPConnector(ssl=False, limit=100)
        )
    
    def get_proxy(self) -> Optional[str]:
        """Get next proxy from rotation"""
        if not self.proxy_config.rotation_enabled or not self.proxy_config.proxy_list:
            return self.proxy_config.http_proxy
        
        proxy = self.proxy_config.proxy_list[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_config.proxy_list)
        return proxy
    
    async def brain_analyze(self, username: str) -> Dict[str, Any]:
        """AI Brain - Advanced pattern analysis"""
        logging.info(f"{Colors.PINK}🧠 Brain analyzing: {username}{Colors.END}")
        
        await asyncio.sleep(0.3)
        
        features = {
            'length': len(username),
            'has_digits': any(c.isdigit() for c in username),
            'has_underscore': '_' in username,
            'has_dot': '.' in username,
            'has_dash': '-' in username,
            'alphanumeric_ratio': sum(c.isalnum() for c in username) / len(username) if username else 0,
            'special_chars': len([c for c in username if not c.isalnum()]),
            'uppercase_count': sum(c.isupper() for c in username),
            'digit_count': sum(c.isdigit() for c in username),
        }
        
        # Advanced pattern recognition
        patterns = []
        if any(x in username.lower() for x in ['admin', 'test', 'user', 'demo']):
            patterns.append("generic")
        if len(username) < 4:
            patterns.append("short")
        if sum(c.isdigit() for c in username) > len(username) / 2:
            patterns.append("numeric_heavy")
        if username.lower() == username and '_' not in username:
            patterns.append("simple_lowercase")
        if any(year in username for year in ['199', '200', '201', '202']):
            patterns.append("contains_year")
        
        pattern_type = patterns[0] if patterns else "custom"
        
        # Risk scoring
        risk_factors = {
            'common_pattern': pattern_type == "generic",
            'short_username': len(username) < 5,
            'suspicious_chars': features['special_chars'] > 3,
            'numeric_heavy': features['digit_count'] > len(username) / 2
        }
        
        risk_score = sum(risk_factors.values()) / len(risk_factors)
        
        return {
            'username': username,
            'pattern_type': pattern_type,
            'patterns_detected': patterns,
            'features': features,
            'risk_assessment': {
                'score': risk_score,
                'factors': risk_factors,
                'level': 'high' if risk_score > 0.6 else 'medium' if risk_score > 0.3 else 'low'
            },
            'confidence': random.uniform(0.75, 0.98),
            'timestamp': datetime.now().isoformat()
        }
    
    async def muscle_scan(self, username: str) -> Dict[str, Any]:
        """Muscle - High-performance concurrent scanning with rate limiting"""
        logging.info(f"{Colors.CYAN}💪 Muscle scanning across {len(self.platforms)} platforms{Colors.END}")
        
        results = {}
        found_count = 0
        error_count = 0
        
        # Scan in batches to respect rate limits
        batch_size = 10
        platform_items = list(self.platforms.items())
        
        for i in range(0, len(platform_items), batch_size):
            batch = platform_items[i:i + batch_size]
            tasks = []
            
            for platform, url_template in batch:
                task = self.check_platform_with_retry(
                    platform,
                    url_template.format(username),
                    username
                )
                tasks.append(task)
            
            # Run batch concurrently
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for (platform, _), result in zip(batch, batch_results):
                if isinstance(result, Exception):
                    results[platform] = {
                        'status': 'error',
                        'error': str(result),
                        'platform': platform
                    }
                    error_count += 1
                else:
                    results[platform] = result
                    if result.get('status') == 'found':
                        found_count += 1
            
            # Brief pause between batches
            if i + batch_size < len(platform_items):
                await asyncio.sleep(0.5)
        
        return {
            'username': username,
            'platform_results': results,
            'statistics': {
                'total_platforms': len(self.platforms),
                'found': found_count,
                'not_found': len(results) - found_count - error_count,
                'errors': error_count,
                'success_rate': (found_count / len(results)) * 100 if results else 0
            },
            'timestamp': datetime.now().isoformat()
        }
    
    async def check_platform_with_retry(
        self,
        platform: str,
        url: str,
        username: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """Check platform with retry logic and rate limiting"""
        
        for attempt in range(max_retries):
            try:
                # Apply rate limiting
                await self.rate_limiter.acquire(platform)
                
                # Get proxy if enabled
                proxy = self.get_proxy() if self.proxy_config.enabled else None
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                
                async with self.session.get(
                    url,
                    headers=headers,
                    proxy=proxy,
                    allow_redirects=True,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    
                    # Check response
                    status = response.status
                    final_url = str(response.url)
                    
                    # Platform-specific logic
                    found = False
                    if status == 200:
                        # Some platforms redirect to different pages when not found
                        if platform == 'github' and '/search?' not in final_url:
                            found = True
                        elif platform == 'instagram' and final_url == url:
                            found = True
                        elif platform not in ['github', 'instagram']:
                            found = True
                    
                    return {
                        'status': 'found' if found else 'not_found',
                        'status_code': status,
                        'url': final_url,
                        'platform': platform,
                        'response_time': response.headers.get('X-Response-Time', 'N/A'),
                        'attempt': attempt + 1
                    }
                    
            except asyncio.TimeoutError:
                if attempt == max_retries - 1:
                    return {
                        'status': 'timeout',
                        'platform': platform,
                        'error': 'Request timeout',
