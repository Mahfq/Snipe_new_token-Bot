from web3 import Web3
import json

# add your blockchain connection information
Provider_url = 'ADDYOURINFURAURL'
web3 = Web3(Web3.HTTPProvider(Provider_url))

if web3.is_connected():
    print("Connecté à Ethereum")

#Smart contract ERC20 ABI  
abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')

latest_block_number = web3.eth.block_number

def main():
    #Find new block
    global latest_block_number 
    block_number = web3.eth.block_number  
    if block_number != latest_block_number: 
        latest_block_number = block_number
        #Find transactions in this block
        block = web3.eth.get_block(latest_block_number, full_transactions=True)
        transactions = block['transactions']
        print("Nombre de transactions dans le bloc" ,latest_block_number,":", len(transactions))
        #Process transaction data
        for tx in transactions:
            to_address = tx['to']
            #It's smart contract
            if to_address is None or to_address == "0x0":
                info_transac = web3.eth.get_transaction_receipt(tx.hash.hex())
                address = info_transac['contractAddress']
                contract = web3.eth.contract(address=address, abi=abi)
                try:
                    name = contract.functions.name().call()
                    symbol = contract.functions.symbol().call()
                    total_supply = contract.functions.totalSupply().call()
                    is_erc20 = True
                except:
                    is_erc20 = False

                if is_erc20:
                    print()
                    print(address,"Ce contrat est ERC20")
                    print('Nom du contrat: ', name)
                    print('Symbole: ', symbol)
                    print('Total Supply: ', total_supply)
                    print()
                else:
                    print()
                    print(address,"Ce contrat n'est pas un ERC20")
                    print()

while __name__ == '__main__':
    main()



 
