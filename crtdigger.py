#!/usr/bin/env python3
import re
import sys
import os
import time
import argparse
import requests
import urllib3
import concurrent.futures
import tldextract
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

def banner():
    # تعديل البانر: crt digger بمسافة وحرف d صغير
    banner_text=r"""
           _         _ _
  ___ _ __| |_    __| (_) __ _  __ _  ___ _ __
 / __| '__| __|  / _` | |/ _` |/ _` |/ _ \ '__|
| (__| |  | |_  | (_| | | (_| | (_| |  __/ |
 \___|_|   \__|  \__,_|_|\__, |\__, |\___|_|
                         |___/ |___/
           By: rv_u
    """
    print(Fore.CYAN + banner_text)

def check_alive(domain, timeout=5):
    protocols = ['https://', 'http://']
    for proto in protocols:
        try:
            response = requests.get(f"{proto}{domain}", timeout=timeout, verify=False)
            return domain
        except requests.exceptions.RequestException:
            continue
    return None

def collect_from_crtsh(org, max_retries=3):
    print(Fore.YELLOW + f"[*] Fetching domains for [{org}] from crt.sh...")
    domains = set()
    org_encoded = org.replace(" ", "%20")
    url = f"https://crt.sh/?O=%25.{org_encoded}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for attempt in range(1, max_retries + 1):
        try:
            req = requests.get(url, headers=headers, timeout=30)
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, "html.parser")
                td = soup.find_all("td")
                for dom in td:
                    for text in dom.stripped_strings:
                        text = text.strip().lower()
                        text = re.sub(r'^\*\.', '', text)
                        if re.match(r'^([a-z0-9-]+\.)+[a-z]{2,}$', text):
                            domains.add(text)
                return domains
            elif req.status_code in [500, 502, 503, 504]:
                print(Fore.RED + f"[!] crt.sh returned {req.status_code}.")
                if attempt < max_retries:
                    print(Fore.YELLOW + f"[*] Retrying in 5s... ({attempt}/{max_retries})")
                    time.sleep(5)
            else:
                return set()
        except requests.exceptions.RequestException:
            if attempt < max_retries: time.sleep(5)
    return domains

def main():
    banner()

    # جعل argparse يقبل الأوامر بدون إلزامية الـ Modes
    parser = argparse.ArgumentParser(description="crt digger - By: rv_u", add_help=False)
    parser.add_argument('target', type=str, help='Org Name or File')

    # تحويل الـ Mode ليكون اختيارياً (Default is Horizontal)
    mode_group = parser.add_mutually_exclusive_group(required=False)
    mode_group.add_argument('-H', '--horizontal', action='store_true', help='Horizontal Recon (Default)')
    mode_group.add_argument('-V', '--vertical', action='store_true', help='Vertical Recon')

    parser.add_argument('-o', '--output', type=str, help='Output file')
    parser.add_argument('-p', '--probe', action='store_true', help='Live host probing')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Threads')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show help')

    args = parser.parse_args()

    # تحديد الـ Mode الافتراضي
    is_vertical = args.vertical
    is_horizontal = True if (args.horizontal or not args.vertical) else False

    orgs_to_check = []
    if os.path.isfile(args.target):
        with open(args.target, 'r') as f:
            orgs_to_check = [line.strip() for line in f if line.strip()]
    else:
        orgs_to_check.append(args.target)

    all_domains = set()
    for org in orgs_to_check:
        found_domains = collect_from_crtsh(org)
        all_domains.update(found_domains)

    if not all_domains:
        print(Fore.RED + "[-] No domains found.")
        sys.exit(0)

    # تنفيذ الفلترة بناءً على الـ Mode المختار أو الافتراضي
    if is_horizontal:
        print(Fore.YELLOW + "[*] Mode: Horizontal Recon (Default)")
        filtered_domains = set()
        for domain in all_domains:
            ext = tldextract.extract(domain)
            if ext.domain and ext.suffix:
                filtered_domains.add(f"{ext.domain}.{ext.suffix}")
        all_domains = filtered_domains
    else:
        print(Fore.YELLOW + "[*] Mode: Vertical Recon")

    print(Fore.GREEN + f"\n[+] Total unique domains: {len(all_domains)}")

    final_domains = set()
    if args.probe:
        print(Fore.YELLOW + f"[*] Probing {len(all_domains)} domains...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
            future_to_domain = {executor.submit(check_alive, domain): domain for domain in all_domains}
            for future in concurrent.futures.as_completed(future_to_domain):
                res = future.result()
                if res:
                    print(Fore.GREEN + f"[LIVE] {res}")
                    final_domains.add(res)
    else:
        final_domains = all_domains
        for d in final_domains: print(Fore.WHITE + f"[+] {d}")

    # التسمية التلقائية للملف
    if args.output:
        out_file = args.output
    else:
        name = os.path.basename(args.target).replace(" ", "_").replace(".txt", "")
        m = "horizontal" if is_horizontal else "vertical"
        p = "_live.txt" if args.probe else "_all.txt"
        out_file = f"{name}_{m}{p}"

    with open(out_file, "w") as f:
        for d in sorted(final_domains): f.write(d + "\n")

    print(Fore.CYAN + f"\n[=] Saved to: {out_file}")
    print(Fore.WHITE + "Happy Hacking " + Fore.RED + ";)")

if __name__ == "__main__":
    main(
