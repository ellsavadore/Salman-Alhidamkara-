# Network Scanner - Untuk tujuan edukasi dan administrasi jaringan
# Author: Salman Alhidamkara

import socket
import subprocess
import sys
import datetime
from threading import Thread

class NetworkScanner:
    def __init__(self, network_prefix):
        self.network_prefix = network_prefix
        self.active_hosts = []
        self.scan_date = datetime.datetime.now()
        
    def display_banner(self):
        print("=" * 50)
        print("   Network Scanner Tool")
        print("   Author: Salman Alhidamkara")
        print("=" * 50)
        
    def ping_host(self, ip):
        """Ping host untuk cek apakah aktif"""
        param = '-n' if sys.platform.lower().startswith('win') else '-c'
        command = ['ping', param, '1', ip]
        
        try:
            result = subprocess.run(command, capture_output=True, timeout=2)
            if result.returncode == 0:
                self.active_hosts.append(ip)
                print(f"[+] Host aktif: {ip}")
        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            pass
    
    def scan_network(self):
        """Scan semua host dalam jaringan"""
        print(f"\nScanning network: {self.network_prefix}.0/24")
        print(f"Waktu scan: {self.scan_date}")
        print("-" * 40)
        
        threads = []
        for i in range(1, 255):
            ip = f"{self.network_prefix}.{i}"
            thread = Thread(target=self.ping_host, args=(ip,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        return self.active_hosts
    
    def scan_ports(self, ip, ports=None):
        """Scan port pada IP tertentu"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 
                     993, 995, 1433, 3306, 3389, 5432, 5900, 8080, 8443]
        
        print(f"\nScanning ports on {ip}...")
        open_ports = []
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"  Port {port} : OPEN")
                sock.close()
            except:
                pass
        
        return open_ports
    
    def generate_report(self):
        """Generate laporan scan"""
        report = f"""
NETWORK SCAN REPORT
===================
Scan Date: {self.scan_date}
Network: {self.network_prefix}.0/24

ACTIVE HOSTS FOUND:
{len(self.active_hosts)} host(s) aktif

List active hosts:
"""
        for host in self.active_hosts:
            report += f"- {host}\n"
        
        report += "\n" + "=" * 40 + "\n"
        return report
    
    def save_report(self, filename="scan_report.txt"):
        """Simpan laporan ke file"""
        report = self.generate_report()
        with open(filename, 'w') as f:
            f.write(report)
        print(f"\nReport saved to {filename}")

def main():
    scanner = NetworkScanner("192.168.1")
    scanner.display_banner()
    
    print("\nPilihan:")
    print("1. Scan network (cari host aktif)")
    print("2. Scan port pada IP tertentu")
    print("3. Full scan (network + port pada host aktif)")
    
    choice = input("\nPilih menu (1/2/3): ")
    
    if choice == "1":
        scanner.scan_network()
        print(f"\nTotal host aktif: {len(scanner.active_hosts)}")
        scanner.save_report()
    
    elif choice == "2":
        ip = input("Masukkan IP target: ")
        ports = scanner.scan_ports(ip)
        print(f"\nOpen ports pada {ip}: {ports}")
    
    elif choice == "3":
        print("\n=== FULL SCAN ===")
        scanner.scan_network()
        for host in scanner.active_hosts:
            print(f"\nScanning ports on {host}...")
            scanner.scan_ports(host)
        scanner.save_report("full_scan_report.txt")
    
    else:
        print("Pilihan tidak valid")

if __name__ == "__main__":
    main()
