import json
import time
from datasketch import HyperLogLog

def load_data(file_path):
    """
    Load data from the log file.
    Ignores invalid JSON lines and extracts IP addresses.
    """
    ips = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                
                data = json.loads(line.strip())
                
                ip = data.get("remote_addr")
                if ip:
                    ips.append(ip)
            except json.JSONDecodeError:
                
                pass
    return ips

def exact_count(ips):
    """
    Count exact unique IPs using a standard Python set.
    """
    return len(set(ips))

def approximate_count(ips):
    """
    Count approximate unique IPs using HyperLogLog.
    """
    
    hll = HyperLogLog(p=14)
    for ip in ips:
        
        hll.update(ip.encode('utf-8'))
    return hll.count()

def main():
    file_path = "lms-stage-access.log"
    
    
    ips = load_data(file_path)
    
    
    start_exact = time.time()
    exact_res = exact_count(ips)
    time_exact = time.time() - start_exact
    
    
    start_approx = time.time()
    approx_res = approximate_count(ips)
    time_approx = time.time() - start_approx
    
    
    print("Результати порівняння:")
    print(f"{'':<25}{'Точний підрахунок':>20}{'HyperLogLog':>15}")
    print(f"{'Унікальні елементи':<25}{float(exact_res):>20.1f}{float(approx_res):>15.1f}")
    print(f"{'Час виконання (сек.)':<25}{time_exact:>20.5f}{time_approx:>15.5f}")

if __name__ == "__main__":
    main()