      ____ ____ _____      ____  _                     
     / ___|  _ \_   _|    |  _ \(_) __ _  __ _  ___ _ __ 
    | |   | |_) || |      | | | | |/ _` |/ _` |/ _ \ '__|
    | |___|  _ < | |   _  | |_| | | (_| | (_| |  __/ |   
     \____|_| \_\|_|  (_) |____/|_|\__, |\__, |\___|_|   
    --------------------------------|___/ |___/----------
              DIG DEEPER INTO DOMAINS | By: rv_u
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
<img width="1688" height="1281" alt="1" src="https://github.com/user-attachments/assets/ea58c558-3255-4cb2-8b2b-8f60f2532e6f" />

-----------------------------------------------
2. Vertical Recon with Live Probing (20 Threads)
```
python3 crtdigger.py "Organization Name" -V -p -t 20
```
<img width="2234" height="1426" alt="2" src="https://github.com/user-attachments/assets/0dd10e2e-b2c7-413c-9022-6a99f3739f35" />

-----------------------------------------------
3. Bulk Scanning from File
```
python3 crtdigger.py orgs_list.txt -H -o results.txt
```

--> By: rv_u
------> Happy Hacking ;)
