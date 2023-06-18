from web3 import Web3
import os
from dotenv import load_dotenv
import json

with open('ABI_ERC20.json', 'r') as abi_file:
    abi_erc20 = json.load(abi_file)

with open('ABI_ERC721.json', 'r') as abi_file:
    abi_erc721 = json.load(abi_file)

load_dotenv()
data= os.getenv('provider')
web3 = Web3(Web3.HTTPProvider(data))
if web3.is_connected():
    print("Connecté à Ethereum")

latest_block_number = web3.eth.block_number

def nb_block():
    global latest_block_number
    block_number = web3.eth.block_number
    if block_number != latest_block_number:
        latest_block_number = block_number
        block = web3.eth.get_block(latest_block_number, full_transactions=True)
        print("Nouveau bloc", ":", latest_block_number)
        transactions = block['transactions']
        return transactions

def is_erc20(contract_address):
    erc20_contract = web3.eth.contract(address=contract_address, abi=abi_erc20)
    try:        
        name = erc20_contract.functions.name().call()
        symbol = erc20_contract.functions.symbol().call()
        totalsupply = erc20_contract.functions.totalSupply().call()
        decimals = erc20_contract.functions.decimals().call()
        reel_supply = totalsupply/ 10 ** decimals
        print()
        print(
            f"{contract_address} - Ce contract est ERC20\n"
            f"Nom du contract: {name}\n"
            f"Symbole: {symbol}\n"
            f"Supply: {totalsupply}\n"
            f"Reel supply : {reel_supply}\n"
            )
        return True
    except:
        return False

def is_erc721(contract_address):
    erc721_contract = web3.eth.contract(address=contract_address, abi=abi_erc721)
    try:
        erc721_contract.functions.supportsInterface(
            web3.keccak(text="supportsInterface(bytes4)").hex()[:10]  # Interface ERC721
        ).call()
        return True
    except:
        return False

def main():
    transactions = nb_block()
    if transactions is not None:
        for tx in transactions:
            to_address = tx['to']
            if to_address is None or to_address == "0x0":
                info_transac = web3.eth.get_transaction_receipt(tx.hash.hex())
                contract_address = info_transac['contractAddress']
                if is_erc20(contract_address):
                    detectorhoneypot(contract_address)
                elif is_erc721(contract_address):
                    print(f"{contract_address} - Ce contrat est un ERC721")

while __name__ == '__main__':
    main()

 
