from django.contrib import messages
from django.http import JsonResponse

import requests, json

from solana_portfolio_tracker.settings import HELIUS_KEY_ID, SimpleHash_API_KEY

from .models import SolanaWallet
from snapshot.models import WalletSnapshot
from snapshot.views import snapshot

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


def connect_wallet(request):
    user = request.user

    if request.method == 'POST':
        response = json.loads(request.body.decode('utf-8'))

        try:
            wallet = response['publicKey']

            if user.solana_wallet is not None:
                if user.solana_wallet.solana_wallet_address == wallet:
                    messages.success(request, f'Wallet ({wallet}) is connected.')
                    return JsonResponse({'message': 'Wallet is connected.'}, status=200)
                user.solana_wallet.solana_wallet_address = wallet
                user.solana_wallet.save()
                # Create first wallet balance snapshot
                first_snapshot(user)
                messages.success(request, f'New wallet ({wallet}) has been successfully added to your profile.')
                return JsonResponse({'message': 'Success'}, status=201)

            solana_wallet = SolanaWallet.objects.create(solana_wallet_address=wallet)
            user.solana_wallet = solana_wallet
            user.save()
            # Create first wallet balance snapshot
            first_snapshot(user)
            messages.success(request, f'Congratulations! Your wallet ({wallet}) has been added to your profile!')
            return JsonResponse({'message': 'Wallet has been added to account.'}, status=201)
        except KeyError:
            messages.error(request, 'Error occurred. Try connecting your wallet again.')
            return JsonResponse({'message': 'Failed to connect the wallet.'}, status=400)

    return JsonResponse({'message': 'Method not allowed.'}, status=405)

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
                nft_name = nft_name[:15] + '...'
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


def first_snapshot(user):
    if WalletSnapshot.objects.filter(user=user).count() == 0:
        wallet_balances = snapshot(user)  # Return (account_balance, solana_wallet_balance)
        total_wallet_balance = wallet_balances[0]  # account_balance
        solana_wallet_balance = wallet_balances[1]  # solana_wallet_balance

        wallet_snapshot = WalletSnapshot.objects.create(
            wallet_balance=total_wallet_balance,
            solana_wallet_balance=solana_wallet_balance,
            user=user
        )

        wallet_snapshot.save()