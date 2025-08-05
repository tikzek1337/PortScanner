import socket
import threading
import time
import sys
import os
from datetime import datetime

class PortScanner:
    def __init__(self):
        self.open_ports = []
        self.closed_ports = []
        self.threads = []
        self.lock = threading.Lock()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_logo(self):
        logo = """
         _   _ _             _    
        | |_(_) | __ _______| | __
        | __| | |/ /|_  / _ \ |/ /
        | |_| |   <  / /  __/   < 
         \__|_|_|\_\/___\___|_|\_/
                           
        
        ========================================
                  PORT SCANNER by tikzek
        ========================================
        """
        print(logo)
    
    def scan_port(self, host, port, timeout=1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            with self.lock:
                if result == 0:
                    self.open_ports.append(port)
                    service = self.get_service_name(port)
                    print(f"[+] Порт {port} ОТКРЫТ - {service}")
                else:
                    self.closed_ports.append(port)
                    
        except socket.gaierror:
            pass
        except Exception:
            pass
    
    def get_service_name(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
            995: "POP3S", 587: "SMTP", 465: "SMTPS", 3389: "RDP", 5432: "PostgreSQL",
            3306: "MySQL", 1433: "MSSQL", 6379: "Redis", 27017: "MongoDB",
            8080: "HTTP-Proxy", 8443: "HTTPS-Alt", 9000: "SonarQube"
        }
        return services.get(port, "Unknown")
    
    def scan_range(self, host, start_port, end_port, thread_count=100):
        self.clear_screen()
        self.show_logo()
        
        print(f"\nСканирование {host} портов {start_port}-{end_port}")
        print(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        start_time = time.time()
        
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(host, port))
            self.threads.append(thread)
            thread.start()
            
            if len(self.threads) >= thread_count:
                for t in self.threads:
                    t.join()
                self.threads = []
        
        for thread in self.threads:
            thread.join()
        
        end_time = time.time()
        self.show_results(host, end_time - start_time)
    
    def scan_common_ports(self, host):
        self.clear_screen()
        self.show_logo()
        
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080]
        
        print(f"\nСканирование популярных портов на {host}")
        print(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        start_time = time.time()
        
        for port in common_ports:
            thread = threading.Thread(target=self.scan_port, args=(host, port))
            thread.start()
            self.threads.append(thread)
        
        for thread in self.threads:
            thread.join()
        
        end_time = time.time()
        self.show_results(host, end_time - start_time)
    
    def show_results(self, host, scan_time):
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ")
        print("=" * 50)
        print(f"Хост: {host}")
        print(f"Время сканирования: {scan_time:.2f} секунд")
        print(f"Открытых портов: {len(self.open_ports)}")
        print(f"Закрытых портов: {len(self.closed_ports)}")
        
        if self.open_ports:
            print("\nОТКРЫТЫЕ ПОРТЫ:")
            print("-" * 30)
            for port in sorted(self.open_ports):
                service = self.get_service_name(port)
                print(f"  {port:5d} - {service}")
        else:
            print("\nОткрытые порты не найдены")
        
        print("=" * 50)

def main():
    scanner = PortScanner()
    scanner.show_logo()
    
    while True:
        print("\n1. Сканировать диапазон портов")
        print("2. Сканировать популярные порты")
        print("3. Выход")
        
        choice = input("\nВыберите опцию: ").strip()
        
        if choice == "1":
            host = input("Введите IP или домен: ").strip()
            try:
                start_port = int(input("Начальный порт: "))
                end_port = int(input("Конечный порт: "))
                if start_port > end_port or start_port < 1 or end_port > 65535:
                    print("Неверный диапазон портов!")
                    continue
                scanner = PortScanner()
                scanner.scan_range(host, start_port, end_port)
            except ValueError:
                print("Введите корректные числа!")
                
        elif choice == "2":
            host = input("Введите IP или домен: ").strip()
            scanner = PortScanner()
            scanner.scan_common_ports(host)
            
        elif choice == "3":
            print("Выход...")
            break
            
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()