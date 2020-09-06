# IBClient

IBClient is an extension of IbPy. It provides higher layer abstraction APIs to 
interact with Interactive Brokers TWS. With these APIs, users could access 
market data, fundamental data, place order and review account using python 
script instead of TWS GUI.

## Dependencies

- python 2.7 or python >= 3.5 
- [IbPy](https://github.com/blampe/IbPy "IbPy")
- [pandas](http://pandas.pydata.org/ "pandas")


## Installation

- Install from source

1. download the source code or clone git repo: `git clone https://github.com/chrjxj/ibclient.git`
2. run `python setup.py install`

## Test

1. change directory to `tests` folder, create a config file `test-acc.yaml`, e.g.
 
```
host: localhost
port: 7497
client_id: 666

account: FILL-YOUR-IB-ACCOUNT
starting_cash: 100000

stock:
  symbol: 1810
  security_type: STK
  currency: HKD
  exchange: SEHK
  sid: 123
  price_unit: 0.05

future:
  symbol: XINA50
  exchange: SGX
  expiry: 20200528
  tradingClass: CN
``` 
 
2. run `python -m unittest xxx_test.py`
