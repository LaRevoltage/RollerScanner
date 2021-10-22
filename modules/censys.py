import requests
import re
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
def SearchByIp(target):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers',
    }
    i=0
    response = requests.get(f'''https://search.censys.io/hosts/{target}''', headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="content")
    ports = results.find_all("div", class_="protocol-details")
    for port in ports:
        soup = BeautifulSoup(str(port), features="lxml")
        results = soup.h2
        results = str(results.text)
        results = results.replace(" ", "")
        results = results.split('\n')
        print('[', Fore.LIGHTCYAN_EX+'*'+Style.RESET_ALL,']',Fore.YELLOW+"Protocol:",results[1].split("/")[1]+Style.RESET_ALL,Fore.GREEN+"is on port:"+Style.RESET_ALL,Fore.YELLOW+results[1].split("/")[0]+Style.RESET_ALL)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="content")
    try:
        dl_data = results.find('dt', string='OS').find_next_siblings('dd')
        print('[', Fore.LIGHTCYAN_EX+'*'+Style.RESET_ALL,']', Fore.YELLOW+"OS:"+Style.RESET_ALL,Fore.GREEN+dl_data[0].string.replace("\n", "")+Style.RESET_ALL)
    except:
        print('[', Fore.LIGHTCYAN_EX+'!'+Style.RESET_ALL,']',Fore.RED+"OS Can't be specified!"+Style.RESET_ALL)
    try:
        dl_data = results.find('dt', string='Network').find_next_siblings('dd')
        print('[', Fore.LIGHTCYAN_EX+'*'+Style.RESET_ALL,']', Fore.YELLOW+"Network:"+Style.RESET_ALL,Fore.GREEN+dl_data[0].text.replace(" ", "").replace("\n", "")+Style.RESET_ALL)
    except:
        print('[', Fore.LIGHTCYAN_EX+'!'+Style.RESET_ALL,']',Fore.RED+"Network Can't be specified!"+Style.RESET_ALL)
    try:
        dl_data = results.find('dt', string='Routing').find_next_siblings('dd')
        print('[', Fore.LIGHTCYAN_EX+'*'+Style.RESET_ALL,']', Fore.YELLOW+"Routing:"+Style.RESET_ALL,Fore.GREEN+dl_data[0].text.replace(" ", "").replace("\n", "")+Style.RESET_ALL)
    except:
        print('[', Fore.LIGHTCYAN_EX+'!'+Style.RESET_ALL,']',Fore.RED+"Routing Can't be specified!"+Style.RESET_ALL)
    try:
        ports=results.find_all("div", class_="protocol-details")
        for portservice in ports:
            portlist=(portservice.find_next_siblings("div", class_="host-section"))
            port=re.sub('\n\n', '\n', portlist[0].text)
            port=re.sub(' +', ' ', port)
            port=port.split("\n")
            print(Fore.BLUE+portservice.text.split("\n")[2].replace(" ", "")+":"+Style.RESET_ALL)
            for el in port:
                if el!='' and el!=' ' and "\r" not in el and "\n" not in el:
                    if(el.startswith(" ")==True):
                        print(Fore.GREEN+el.replace(" ", "-", 1)+Style.RESET_ALL)
                    if(el.startswith(" ")==False):
                        print(Fore.YELLOW+el+":"+Style.RESET_ALL)
                elif(el!=' '):
                    print(Fore.GREEN+el+Style.RESET_ALL)
    except Exception as e:
        print(e)
def SearchByDomain(target):
    addr=[]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://search.censys.io/search?resource=hosts&q=artscp.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'max-age=0',
    }
    params = (
        ('resource', 'hosts'),
        ('q', " services.tls.certificates.leaf_data.names: "+target),
    )
    response = requests.get('https://search.censys.io/_search', headers=headers, params=params)

    soup = BeautifulSoup(response.text, "html.parser")
    results=soup.find_all("div", {"class": "SearchResult result"})
    soup = BeautifulSoup(str(results), features="lxml")
    for result in soup.find_all('a', href=True):
        preresult=str(result.text).replace("\n", "")
        preresult=preresult.replace(" ", "")
        resultis=(preresult.split("\n"))
        if(any(c.isalpha() for c in resultis[0])==False):
            addr.append(resultis[0])
    return(addr)
if __name__ == '__main__':
    searchbyip(target)
    searchbydomain(target)