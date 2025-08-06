import random
from datetime import datetime, timedelta
import argparse
from faker import Faker

fake = Faker()

# Argument parser
parser = argparse.ArgumentParser(description='Generate random NGINX-style access logs.')
parser.add_argument('-l', '--len_logs', type=int, default=100, help='Number of log entries to generate (default: 100)')
parser.add_argument('-s', '--status_codes', type=list, nargs='*', default=[200, 201, 204, 301, 400, 403, 404, 500], help='List of status codes to use (default: [200, 201, 204, 301, 400, 403, 404, 500])')
parser.add_argument('-r', '--referers', type=list, nargs='*', default=['-', 'https://google.com', 'https://example.com', 'https://facebook.com', 'https://linkedin.com'], help='List of referers to use (default: ["-", "https://google.com", "https://example.com", "https://facebook.com", "https://linkedin.com"])')
args = parser.parse_args()
len_logs = args.len_logs

methods = ['GET', 'POST', 'PUT', 'DELETE']
paths = [fake.uri_path() for _ in range(10)]
status_codes = args.status_codes
user_agents = [fake.user_agent() for _ in range(10)]
referers = args.referers

def generate_log_entry(base_time):
    ip = fake.ipv4()
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
