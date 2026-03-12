# crt digger 
**A fast, multi-threaded OSINT tool for Horizontal & Vertical Recon via crt.sh.**

Developed by: **rv_u**

## Features
- **Auto-Mode:** Defaults to Horizontal Recon (Root Domains) if no flags provided.
- **Smart Recon:** Choose between Horizontal (`-H`) and Vertical (`-V`).
- **Live Probing:** Built-in multithreaded HTTP/HTTPS prober (`-p`).
- **Resilience:** Automatic retry logic (3 attempts) to bypass `crt.sh` 503 errors.
- **Clean Output:** Auto-cleans wildcards and junk data for ready-to-scan targets.

## Installation
```bash
git clone https://github.com/RaV-u/crt-digger.git
cd crt-digger
pip3 install -r requirements.txt --break-system
```

## Usage
1. Fast Horizontal Recon (Default)
```
python3 crtdigger.py "Organization Name"
```
3. Vertical Recon with Live Probing (20 Threads)
```
python3 crtdigger.py "Organization Name" -V -p -t 20
```
4. Bulk Scanning from File
```
python3 crtdigger.py orgs_list.txt -H -o results.txt
```
