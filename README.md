# Cryptocurrency egalitarianism: A quantitative approach

In this paper, we define the economic notion of cryptocurrency
"egalitarianism". We provide measurements of the egalitarianism of various
proof-of-work-based cryptocurrencies, including BTC, ETH and XMR. We find that
cryptocurrencies which were designed to be more egalitarian through memory
hardness indeed achieve this and quantify how successful each one is. We
measure the egalitarianism of two proof-of-stake-based cryptocurrencies, DCR
and ADA. Perhaps contrary to folklore belief, we find that proof-of-stake is
perfectly egalitarian in our model.

## Simulation

### Installation

1. Install [pipenv](https://github.com/pypa/pipenv).
2. `cd simulation && pipenv install`

### Usage

```
usage: egalitarianism.py [-h] [-c {btc,eth,xmr}] [-s {tech,electricity,dp}] -d
                         DIFFICULTY -b COINBASE -k KWH -r RATE -p CAPITAL
                         [-t TIME] -f FILE [--version]

Cryptocurrency egalitarianism: A quantitative approach

optional arguments:
  -h, --help            show this help message and exit
  -c {btc,eth,xmr}, --currency {btc,eth,xmr}
                        Currency (default: btc)
  -s {tech,electricity,dp}, --strategy {tech,electricity,dp}
                        Strategy of invenstment (default: tech)
  -d DIFFICULTY, --difficulty DIFFICULTY
                        Block difficulty (required)
  -b COINBASE, --coinbase COINBASE
                        Coinbase (required)
  -k KWH, --kwh KWH     Price per kilowatt per hour (required)
  -r RATE, --rate RATE  Currency price in fiat (required)
  -p CAPITAL, --capital CAPITAL
                        Capital of invenstment (required)
  -t TIME, --time TIME  Total time of operation in months (default:
                        6)
  -f FILE, --file FILE  The path of the file that contains the specs of each
                        hardware (required). Each hardware should contain the
                        following fields: product, hash / s, watt, price
  --version             show program's version number and exit
```

### Examples

#### BTC

`pipenv run python egalitarianism.py -f ./data/btc.csv -d 5106422924659.82 -b 12.5 -k 0.11 -r 4074.25 -p 10000`

#### ETH

`pipenv run python egalitarianism.py -f ./data/eth.csv -c eth -d 2529724525783320 -b 3 -k 0.11 -r 126.12 -p 10000`

#### XMR

`pipenv run python egalitarianism.py -f ./data/xmr.csv -c xmr -d 44453209154 -b 3.37 -k 0.11 -r 47.27 -p 10000`

#### LTC

`pipenv run python egalitarianism.py -f ./data/ltc.csv -c ltc -d 44453209154 -b 25 -k 0.11 -r 32.10 -p 10000`

#### DCR

`pipenv run python egalitarianism.py -f ./data/dcr.csv -c dcr -d 13034411457.7978 -b 11.38 -k 0.11 -r 16.62 -p 10000`

### Docker

#### Build

`docker build -t egalitarianism .`

#### Run
`docker run -it egalitarianism`
