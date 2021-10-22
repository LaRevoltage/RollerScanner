# RollerScanner
[![CodeFactor](https://www.codefactor.io/repository/github/majorraccoon/rollerscanner/badge)](https://www.codefactor.io/repository/github/majorraccoon/rollerscanner) ![](https://dcbadge.vercel.app/api/shield/439119266684600320)
RollerScanner — Fast Port Scanner Written On Python
# Installation
1. You should clone this repository using:
```
git clone https://github.com/MajorRaccoon/RollerScanner.git
```
2. Install requirements:
```
pip3 install -r requirements.txt
```
3. Run the script:
```
python3 rollerscanner.py --target...
```
After running, script will try to ping the target, it will also ask you for threads number, i recommend 5000, it works perfect for me.
# How to use:
Currently, there are only these flags available:
```
--target
```
```
--censys
```
```
--nmapsv
```
```
--port
```
It is only necessary to use ```--target```, to set up ip/domain for scanning.
Other flags can be ignored.

```--censys``` flag availables censys module, so scanner can get possible services and versions that are running on specific port

```--nmapsv``` runs ```nmap -sv``` on every opened port to get possible version, it will take longer yhan censys but it is more accurate.

```--port``` can help you to specify ports to scan.
# Performance:
On my system i am able to scan 65000 ports in 14-17 seconds.
Script uses multithreading, and sets up timeout.
# ToDo:
1. Virtual host scan
2. Vulnerability scan
3. Firewall check
