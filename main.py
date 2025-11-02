import asyncio
import ujson, json
import os
import subprocess
import winreg
import win32api
import psutil
import shutil
import requests
import ssl
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from mitmproxy import certs, http, options
from mitmproxy.tools.dump import DumpMaster
import sys
from datetime import datetime
import traceback
from mitmproxy.tools.web.master import WebMaster
from colorama import Fore, Style, init
import logging
from pathlib import Path

HERE = Path(__file__).parent  
RETRAC = HERE / "retrac.json"


init(autoreset=True)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def clear_fortnite_cms():
    local_appdata = os.getenv('LOCALAPPDATA')
    target_path = os.path.join(local_appdata, 'FortniteGame', 'Saved', 'PersistentDownloadDir', 'CMS')
    
    if not os.path.exists(target_path):
        return
    
    try:
        for filename in os.listdir(target_path):
            file_path = os.path.join(target_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception:
                pass
    except Exception:
        pass

def set_proxy_settings(proxy_server, enable_proxy):
    reg_path = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, 'ProxyServer', 0, winreg.REG_SZ, proxy_server)
        winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, enable_proxy)
        winreg.CloseKey(key)
    except Exception:
        pass

def kill_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if name.lower() in proc.info['name'].lower():
            try:
                proc.kill()
            except psutil.NoSuchProcess:
                pass

def on_exit(signal_type):
    set_proxy_settings("", 0)
    kill_process_by_name("FortniteClient-Win64-Shipping_EAC_EOS.exe")
    kill_process_by_name("FortniteClient-Win64-Shipping.exe")
    kill_process_by_name("FortniteLauncher.exe")
    clear_fortnite_cms()

class Proxy:
    def __init__(self):
        self.config_file = "config.json"
        print("Proxy addon initialized")

    def request(self, flow: http.HTTPFlow):
        if "fortnite" in flow.request.host.lower() or "epicgames" in flow.request.host.lower():
            print(f"Retrac request: {flow.request.method} {flow.request.url}")

    def response(self, flow: http.HTTPFlow) -> None:
        url = flow.request.url.lower()
        if ("athena" in url or "profileid=athena" in url) and flow.request.method == "GET":
            with RETRAC.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)             
            body = json.dumps(payload)             
            flow.response = http.HTTPResponse.make(
                200,
                body,
                {"Content-Type": "application/json"}
            )

def is_certificate_installed():
    try:
        cert_dir = os.path.expanduser("~/.mitmproxy")
        if not os.path.exists(cert_dir):
            return False
            
        cert_files = [f for f in os.listdir(cert_dir) if f.endswith('.pem')]
        if not cert_files:
            return False
            
        cert_path = os.path.join(cert_dir, cert_files[0])
        with open(cert_path, "rb") as f:
            mitm_cert = x509.load_pem_x509_certificate(f.read())
            mitm_fingerprint = mitm_cert.fingerprint(hashes.SHA256())
        
        for cert, encoding, trust in ssl.enum_certificates("ROOT"):
            if encoding == "x509_asn":
                try:
                    cert_obj = x509.load_der_x509_certificate(cert)
                    if cert_obj.fingerprint(hashes.SHA256()) == mitm_fingerprint:
                        return True
                except:
                    continue
        return False
    except Exception as e:
        print(f"Certificate check error: {e}")
        return False

async def install_certificate():
    cert_dir = os.path.expanduser("~/.mitmproxy")
    if not os.path.exists(cert_dir):
        os.makedirs(cert_dir)
    
    if not any(f.endswith('.pem') for f in os.listdir(cert_dir) if os.path.isfile(os.path.join(cert_dir, f))):
        print("Generating MITMproxy certificates...")
        try:
            subprocess.run([
                "mitmdump", 
                "--set", f"confdir={cert_dir}",
                "--certsserver"
            ], capture_output=True, timeout=30)
            print("Certificates generated successfully")
        except Exception as e:
            print(f"Error generating certificates: {e}")
            return
    
    pem_path = os.path.join(cert_dir, "mitmproxy-ca.pem")
    cer_path = os.path.join(cert_dir, "mitmproxy-ca.cer")
    
    if os.path.exists(pem_path) and not os.path.exists(cer_path):
        try:
            with open(pem_path, "rb") as pem_file:
                pem_data = pem_file.read()
            with open(cer_path, "wb") as cer_file:
                cer_file.write(pem_data)
            print("Certificate converted to CER format")
        except Exception as e:
            print(f"Error converting certificate: {e}")
    
    if not is_certificate_installed():
        print("Installing MITMproxy certificate...")
        try:
            result = subprocess.run([
                "certutil.exe",
                "-user",
                "-addstore",
                "Root",
                cer_path
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("Certificate installed successfully")
            else:
                print(f"Certificate installation failed: {result.stderr}")
        except Exception as e:
            print(f"Error installing certificate: {e}")
    else:
        print("Certificate already installed")

async def run_proxy():
    try:
        clear_fortnite_cms()

        opts = options.Options(
            listen_host="0.0.0.0",
            listen_port=1944
        )
        
        master = DumpMaster(opts)
        master.addons.add(Proxy())

        logging.getLogger('mitmproxy').setLevel(logging.WARNING)
        logging.getLogger('asyncio').setLevel(logging.WARNING)

        set_proxy_settings("127.0.0.1:1944", 1)

        print("Proxy server starting on 127.0.0.1:1944")
        print("Waiting for Fortnite requests...")
        print("Press Ctrl+C to stop the proxy")

        await master.run()
    except KeyboardInterrupt:
        print("Shutting down proxy...")
    except Exception as e:
        print(f"Proxy error: {e}")
        traceback.print_exc()
    finally:
        if 'master' in locals():
            master.shutdown()
        
        set_proxy_settings("", 0)


if __name__ == '__main__':
    asyncio.run(run_proxy())