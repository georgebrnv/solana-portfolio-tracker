import requests

from solana_portfolio_tracker.settings import HELIUS_KEY_ID, SimpleHash_API_KEY

# Helius Credentials
HELIUS_URL = f'https://mainnet.helius-rpc.com/?api-key={HELIUS_KEY_ID}'
helius_headers = {
        'Content-Type': 'application/json',
    }

# SimpleHash credentials
simplehash_headers = {
    "accept": "application/json",
    "X-API-KEY": SimpleHash_API_KEY,
}

def snapshot(user):
    wallet_balances = fungible_token_balance(user) # Returns (account_balance, solana_wallet_balance)
    fungible_wallet_balance = wallet_balances[0] # account_balance
    solana_wallet_balance = wallet_balances[1] # solana_wallet_balance

    # NFTs wallet balance
    wallet_nfts_value = nfts_value(user)

    # Total wallet balance (fungible + nfts)
    total_wallet_balance = fungible_wallet_balance + wallet_nfts_value

    return total_wallet_balance, solana_wallet_balance

def nfts_value(user):
    # Request params (GET request)
    request_objects_limit = 25
    order_by = 'floor_price__desc'
    chains = 'solana'

    simplehash_url = f"https://api.simplehash.com/api/v0/nfts/owners_v2?chains={chains}&order_by={order_by}&limit={request_objects_limit}"

    body = {
        'wallet_addresses': [user.solana_wallet.solana_wallet_address]
    }

    response = requests.post(url=simplehash_url, headers=simplehash_headers, json=body)
    nfts_data = response.json()['nfts']

    # Total NFTs value in USDC
    total_nfts_value = 0

    for nft in nfts_data:
        for marketplace in nft['collection']['floor_prices']:
            if marketplace['marketplace_name'] == 'Tensor':
                nft_price_usdc = marketplace['value_usd_cents'] / 100
                total_nfts_value += nft_price_usdc
    return total_nfts_value


# Get total account balance in SOL and USD
def fungible_token_balance(user):

    body = {
        'jsonrpc': '2.0',
        'id': 'my-id',
        'method': 'searchAssets',
        'params': {
            'ownerAddress': user.solana_wallet.solana_wallet_address,
            'page': 1,
            'limit': 200,
            'tokenType': 'fungible',
            'displayOptions': {
                'showUnverifiedCollections': False,
                'showCollectionMetadata': False,
                'showGrandTotal': True,
                'showNativeBalance': True,
                'showInscription': True,
                'showZeroBalance': False,
                'showRawData': False,
            },
        },
    }

    response = requests.post(url=HELIUS_URL, headers=helius_headers, json=body)
    token_balance_data = response.json()['result']

    # Total wallet balance (excluding SOL)
    token_sum_price = 0

    # SOL balance in USD
    solana_wallet_balance = round(token_balance_data['nativeBalance']['total_price'], 2)

    for token in token_balance_data['items']:

        try:
            token_info = token['token_info']
            # Total token price in USD
            token_total_price = token_info['price_info']['total_price']
            # Total wallet balance (excluding SOL)
            token_sum_price += token_total_price
        except KeyError:
            continue



    # Total Wallet Balance in USDC
    account_balance = round(solana_wallet_balance + token_sum_price, 2)

    return account_balance, solana_wallet_balance