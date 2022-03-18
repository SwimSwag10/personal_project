import config
from web3 import Web3 

web3 = Web3(Web3.HTTPProvider(config.INFURA_URL))

balance = web3.eth.get_balance('0x73F7b23Ee66B432CaebcF4A9Dd3836ba4DCDe87f')

print(web3.fromWei(balance, "ether"))