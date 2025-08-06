import random
from datetime import datetime, timedelta
import argparse

methods = ['GET', 'POST', 'PUT', 'DELETE']
paths = [
    '/api/v1/resource', '/index.html', '/login.php',
    '/dashboard', '/products', '/search?q=test', '/logout'
]
status_codes = [200, 201, 204, 301, 400, 403, 404, 500]
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'curl/7.64.1',
    'PostmanRuntime/7.26.8',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'Googlebot/2.1 (+http://www.google.com/bot.html)',
    'Mozilla/5.0 (Linux; Android 10)'
]
referers = [
    '-', 'https://google.com', 'https://example.com', 
    'https://facebook.com', 'https://linkedin.com', '-'
]

# Argument parser
parser = argparse.ArgumentParser(description='Generate random NGINX-style access logs.')
parser.add_argument('-l', '--len_logs', type=int, default=100, help='Number of log entries to generate (default: 100)')
args = parser.parse_args()
len_logs = args.len_logs

def generate_log_entry(base_time):
    ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
    method = random.choice(methods)
    path = random.choice(paths)
    status = random.choice(status_codes)
    size = random.randint(100, 5000)
    referer = random.choice(referers)
    agent = random.choice(user_agents)

    log_time = base_time.strftime('%d/%b/%Y:%H:%M:%S +0000')
    request_line = f'"{method} {path} HTTP/1.1"'
    log_entry = f'{ip} - - [{log_time}] {request_line} {status} {size} "{referer}" "{agent}"'
    return log_entry

def main():
    base_time = datetime.now() - timedelta(minutes=len_logs)  # Start time
    logs = []

    for _ in range(len_logs):
        # Increment time slightly for each log (1-10s)
        delta = timedelta(seconds=random.randint(1, 10))
        base_time += delta
        logs.append(generate_log_entry(base_time))

    # Write logs sorted by timestamp
    with open('logs.txt', 'w') as f:
        for log in logs:
            f.write(log + '\n')

if __name__ == '__main__':
    main()
