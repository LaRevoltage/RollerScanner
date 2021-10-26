from concurrent.futures import ThreadPoolExecutor
import socket
import os
import subprocess
import sys
import modules.censys as censys
import modules.wafmeow as wafmeow
import psutil
import time
from colorama import Fore, Back, Style
choise = "0"
scheme=""
if("--help" in sys.argv):
    print("Usage: python3 rollerscan.py --target [target]")
    print("Additional flags:")
    print("--censys (-c) — scrap data from censys, fastet method to gain info")
    print("--port (-p) — specify port range for scan, by default 1-60 000")
    print("--nmapsv (-nsv) — get service version using nmap")
    print("--https — activate web mode, use if you are scanning an https website")
    print("--http — activate web mode, use if you are scanning an http website")
    exit()
if("--target" in sys.argv):
    indexoftarget = sys.argv.index("--target")
    target = sys.argv[indexoftarget + 1]
else:
    print("Target is not specified, see --help")
    print(sys.argv)
    exit()
if("--port" in sys.argv):
    indexofport = sys.argv.index("--port")
    port = sys.argv[indexofport + 1]
    if("-" in port):
        port = port.split("-")
        end = int(port[1])
        start = int(port[0])
        ports = list(range(start, end))
    elif("," in port):
        ports = port.split(",")
        ports = list(map(int, ports))
elif("-p" in sys.argv):
    indexofport = sys.argv.index("-p")
    port = sys.argv[indexofport + 1]
    if("-" in port):
        port = port.split("-")
        end = int(port[1])
        start = int(port[0])
        ports = list(range(start, end))
    elif("," in port):
        ports = port.split(",")
        ports = list(map(int, ports))
else:
    ports=list(range(1, 65000))
if("--nmapsv" in sys.argv):
    choise = "1"
elif("-nsv" in sys.argv):
    choise = "1"
if("--censys" in sys.argv):
    choise = "2"
if("-c" in sys.argv):
    choise = "2"
if("--http" in sys.argv):
    scheme = "http://"
elif("--https" in sys.argv):
    scheme = "https://"
response = os.system("ping -c 1 " + target)
processes = []
nmapdone = {}
if (response == 0):
    print(
        "[",
        Fore.LIGHTCYAN_EX +
        "^" +
        Style.RESET_ALL,
        "]",
        Fore.YELLOW +
        target +
        Style.RESET_ALL,
        Fore.GREEN +
        "is UP" +
        Style.RESET_ALL)
if (response != 0):
    print(
        "[",
        Fore.LIGHTCYAN_EX +
        "^" +
        Style.RESET_ALL,
        "]",
        Fore.LIGHTYELLOW_EX +
        target +
        Style.RESET_ALL,
        Fore.RED +
        "is DOWN" +
        Style.RESET_ALL)
    docontinue = input(
        "Target is marked as DOWN, continue? Y/N: ")
    if(docontinue == "Y" or docontinue == "y"):
        pass
    else:
        print(Fore.RED + "Shutting down")
        exit()
n = int(
    input(
        "[" +
        Fore.LIGHTCYAN_EX +
        " ? " +
        Style.RESET_ALL +
        "]" +
        Fore.BLUE +
        " How many threads you need?: " +
        Style.RESET_ALL))
print("[", Fore.LIGHTCYAN_EX + "&" + Style.RESET_ALL, "]",
      Fore.BLUE + "Starting Scan!" + Style.RESET_ALL)
start_time = time.time()


def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        con = s.connect((target, port))
        print(
            '[',
            Fore.LIGHTCYAN_EX +
            '*' +
            Style.RESET_ALL,
            ']',
            Fore.YELLOW +
            f'''Port: {port}''' +
            Style.RESET_ALL,
            Fore.GREEN +
            "is opened." +
            Style.RESET_ALL)
        if choise == "1":
            process = subprocess.Popen(
                f'''nmap -sV {target} -p {port} -Pn''', shell=True)
            processes.append(process.pid)
        con.close()
    except Exception as e:
        pass


with ThreadPoolExecutor(max_workers=n) as pool:
    pool.map(portscan, ports)
print(Fore.BLUE + "Scan of ports Ended in:" + Style.RESET_ALL,
      Fore.GREEN + str(round(time.time() - start_time)) + Style.RESET_ALL, "s")
if(choise == "2"):
    adresses = censys.SearchByDomain(target)
    for el in adresses:
        print(Fore.YELLOW + str(adresses.index(el)) + Style.RESET_ALL +
              ": " + Fore.GREEN + el + Style.RESET_ALL)
    addrint = int(
        input(
            Fore.BLUE +
            "Censys got those hosts, which would you like to scrap:? " +
            Style.RESET_ALL))
    target = adresses[addrint]
    censys.SearchByIp(target)
if(scheme=="https://" or scheme=="http://"):
    wafmeow.wafsearch(target,scheme)
def checkprocess():
    for proc in processes:
        if psutil.pid_exists(proc):
            nmapdone[proc] = 'False'
        else:
            nmapdone[proc] = 'True'


if (choise == "1"):
    checkprocess()
    while 'False' in nmapdone.values():
        checkprocess()
