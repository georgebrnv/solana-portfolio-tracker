from django.shortcuts import redirect
from django.contrib import messages

import requests

from solana_portfolio_tracker.settings import HELIUS_KEY_ID, SimpleHash_API_KEY

from .models import SolanaWallet

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


def add_wallet(request):
    if request.method == 'POST':

        user = request.user
        wallet = request.POST['solana_wallet']

        if user.solana_wallet is not None:
            messages.error(request, 'You have already added Solana Wallet Address. Change it in your Profile Settings instead.')
            return redirect('profile')

        solana_wallet = SolanaWallet.objects.create(solana_wallet_address=wallet)
        user.solana_wallet = solana_wallet
        user.save()

        # Flash success message
        messages.success(request, 'Your Wallet has been successfully added.')

        return redirect('profile')



def nft_assets(request):
    user = request.user

    # Request params (GET request)
    request_objects_limit = 15
    order_by = 'floor_price__desc'
    chains = 'solana'

    simplehash_url = f"https://api.simplehash.com/api/v0/nfts/owners_v2?chains={chains}&order_by={order_by}&limit={request_objects_limit}"

    body = {
        'wallet_addresses': [user.solana_wallet.solana_wallet_address]
    }

    response = requests.post(url=simplehash_url, headers=simplehash_headers, json=body)
    nfts_data = response.json()['nfts']

    nfts_list = []

    # Total NFTs value in USDC
    total_nfts_value = 0

    for nft in nfts_data:

        try:
            nft_image_uri = nft['image_url']
            nft_name = nft['name']
            if len(nft_name) > 17:
                nft_name = nft_name[:17] + '...'
            nft_price_sol = 0
            nft_price_usdc = 0
            for marketplace in nft['collection']['floor_prices']:
                if marketplace['marketplace_name'] == 'Tensor':
                    nft_price_sol = round(marketplace['value'] / 1000000000, 2)
                    nft_price_usdc = marketplace['value_usd_cents'] / 100
            sol_currency = {'name': "SOL", 'price': nft_price_sol}
            usdc_currency = {'name': '$', 'price': nft_price_usdc}
            nfts_list.append(
                {'imgUrl': nft_image_uri, 'title': nft_name, 'sol_currency': sol_currency, 'usdc_currency': usdc_currency})
            total_nfts_value += nft_price_usdc
        except KeyError:
            continue

    return nfts_list, total_nfts_value


# Get total account balance in SOL and USD
def fungible_token_balance(request):
    user = request.user

    body = {
        'jsonrpc': '2.0',
        'id': 'my-id',
        'method': 'searchAssets',
        'params': {
            'ownerAddress': user.solana_wallet.solana_wallet_address,
            'page': 1,
            'limit': 1000,
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

    # Tokens Info Dict
    wallet_tokens = {}
    # Total wallet balance (excluding SOL)
    token_sum_price = fungible_tokens_total_balance(token_balance_data)
    # Biggest position
    biggest_position_token_name = ''
    biggest_position_token_balance = 0
    # SOL balance in USD
    total_solana_price = token_balance_data['nativeBalance']['total_price']
    # SOL price
    solana_price = token_balance_data['nativeBalance']['price_per_sol']
    # NFTs account balance
    total_nfts_value = nft_assets(request)[1]

    for token in token_balance_data['items']:
        token_info = token['token_info']

        try:
            token_symbol = token_info['symbol']
        except KeyError:
            continue

        # Total token price in USD
        token_total_price = token_info['price_info']['total_price']

        if token_total_price > biggest_position_token_balance:
            biggest_position_token_balance = token_total_price
            biggest_position_token_name = token_symbol

        # Amount of token in the wallet
        token_amount = token_info['price_info']['total_price'] / token_info['price_info']['price_per_token']


        wallet_tokens[token_symbol] = {
            'amount': round(token_amount, 4),
            'total_price': round(token_total_price, 2),
            'token_balance_percentage': round(token_total_price / (total_solana_price + token_sum_price) * 100, 2),
        }

    # Add Solana to wallet tokens dict
    wallet_tokens['SOL'] = {
        'amount': round(total_solana_price / solana_price, 4),
        'total_price': round(total_solana_price, 2),
        'token_balance_percentage': round(total_solana_price / (total_solana_price + token_sum_price) * 100, 2),
    }

    # Sort the dict according to the total_price in descending order
    sorted_wallet_tokens = sorted(wallet_tokens.items(), key=lambda x: x[1]['total_price'], reverse=True)

    # Account Balance in USD
    fungible_account_balance = total_solana_price + token_sum_price
    # Biggest position percentage
    biggest_position_balance_percentage = biggest_position_token_balance / (fungible_account_balance + total_nfts_value) * 100

    return [total_solana_price, fungible_account_balance, biggest_position_token_name, biggest_position_token_balance, biggest_position_balance_percentage, sorted_wallet_tokens, total_nfts_value]

def fungible_tokens_total_balance(data):
    total_wallet_balance = 0
    for token in data['items']:
         try:
             token_total_price = token['token_info']['price_info']['total_price']
             total_wallet_balance += token_total_price
         except KeyError:
             continue
    return total_wallet_balance
