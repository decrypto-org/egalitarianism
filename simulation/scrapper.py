import time
import json
import numpy as np
from collections import namedtuple
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, NavigableString


Machine = namedtuple('Machine', ['hash', 'watt'])


def parseMoneroBencharks(gpu_card, machines):
    url = 'https://monerobenchmarks.info/t/sp_sAMDNVIDIAG.php?draw=7&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=6&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=7&order[0][dir]=desc&order[1][column]=6&order[1][dir]=desc&start=0&length=100&search[value]=CN-V8&search[regex]=false&_=1548693382189'

    # url = 'https://monerobenchmarks.info/t/sp_cpuAMDINTEL.php?draw=2&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=6&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=7&order[0][dir]=desc&order[1][column]=6&order[1][dir]=desc&start=0&length=100&search[value]=CN-V8&search[regex]=false&_=1548772178903'

    # url = 'https://monerobenchmarks.info/t/sp_cpuINTEL.php?draw=2&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=6&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&order[0][column]=7&order[0][dir]=desc&order[1][column]=6&order[1][dir]=desc&start=0&length=100&search[value]=CN-V8&search[regex]=false&_=1548783474669'

    req = Request(url)

    with urlopen(req) as webpage:
        res = webpage.read().decode('utf-8')

    data = json.loads(res)['data']

    for m in data:
        if any(g in m[0] for g in gpu_card):
            print(m[0])
            hash = float(m[2].strip())
            watt = float(m[3].replace('W', '').strip()) if m[3] != 'N/A' else 0
            machines.append(Machine(hash, watt))


def parseGPUStats(currency, gpu_card, machines):
    currencies = {
        'eth': 'https://gpustats.com/ajax/hashrate/760029f231f37c26b705e990e9413c93?_=1548683165971',
        'xmr': 'https://gpustats.com/ajax/hashrate/a12aea5539be6e2c6b5ee5e03a938bad?_=1548694246365'
    }

    req = Request(
        currencies[currency],
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://gpustats.com/coin/ETH',
            'X-Requested-With': 'XMLHttpRequest',
            'DTN': '1'
        }
    )

    with urlopen(req) as webpage:
        res = webpage.read().decode('utf-8')

    data = json.loads(res)['data']
    for m in data:
        model = BeautifulSoup(m[1], features='html.parser').get_text()
        if any(g in model for g in gpu_card):
            print(model)
            hash = float(m[2].replace('H/s', '').replace('k', '').strip())
            machines.append(Machine(hash, 0))


def parseEthMonitoring(gpu_card, algo, machines):

    for i in range(1, 3):
        url = 'https://www.ethmonitoring.com/benchmark/{0}?algo={1}&page={2}&sort=-power'.format(gpu_card, algo, i)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        with urlopen(req) as webpage:
            soup = BeautifulSoup(webpage, features='html.parser')

        records = soup.find(id='w1').table.tbody

        for row in records:
            if isinstance(row, NavigableString):
                continue
            cells = row.find_all('td')
            hash = float(cells[1].get_text().replace('Mh/s', '').strip())
            watt = float(cells[5].get_text().replace('W', '').strip())
            machines.append(Machine(hash, watt))

        time.sleep(1)


def main():
    machines = []
    gpu_card = ['GTX 570']
    algo = 'cnv8'

    parseEthMonitoring(gpu_card[0], algo, machines)
    parseGPUStats('xmr', gpu_card, machines)
    parseMoneroBencharks(gpu_card, machines)

    hash_median = np.median([m.hash for m in machines])
    watt_median = np.median([m.watt for m in machines])
    print(hash_median, watt_median)


if __name__ == '__main__':
    main()
