from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

import requests

from solana_portfolio_tracker.settings import HELIUS_KEY_ID

from .models import SolanaWallet

URL = f'https://mainnet.helius-rpc.com/?api-key={HELIUS_KEY_ID}'
headers = {
        'Content-Type': 'application/json',
    }
UNVERIFIED_BLOCK_LIST = ['Amount', 'AMOUNT', 'Website', 'Verified', 'Time Left']

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



def verified_nfts(request):
    user = request.user

    body = {
        'jsonrpc': '2.0',
        'id': 'my-id',
        'method': 'searchAssets',
        'params': {
            'ownerAddress': user.solana_wallet.solana_wallet_address,
            'page': 1,
            'limit': 300,
            'creatorVerified': True,
            'options': {
                'showUnverifiedCollections': False,
                'showNativeBalance': True,
                'showInscription': False,
                'showZeroBalance': False,
            },
        },
    }

    response = requests.post(url=URL, headers=headers, json=body)
    nfts_data = response.json()['result']

    verified_nfts_list = []

    for nft in nfts_data['items']:
        spam_collection = False
        metadata = nft['content']['metadata']

        try:
            # Filter spam ntfs from received nfts data
            for attribute in metadata['attributes']:
                if attribute['trait_type'] in UNVERIFIED_BLOCK_LIST:
                    spam_collection = True
                    break
                else:
                    continue

            # Store verified nfts data in the list
            if not spam_collection:
                nft_image_uri = nft['content']['links']['image']
                nft_name = nft['content']['metadata']['name']
                if nft_name == '':
                    nft_name = 'Unknown Collection'
                currency1 = {'name': "SOL", 'price': 0.5}
                currency2 = {'name': '$', 'price': 100}

                verified_nfts_list.append(
                    {'imgUrl': nft_image_uri, 'title': nft_name, 'currency1': currency1, 'currency2': currency2})

        except KeyError:
            continue

    return verified_nfts_list


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

    response = requests.post(url=URL, headers=headers, json=body)
    token_balance_data = response.json()['result']

    # Tokens Info Dict
    wallet_tokens = {}
    # Total price of all tokens BESIDES SOL
    token_sum_price = 0

    for token in token_balance_data['items']:
        token_info = token['token_info']

        try:
            token_symbol = token_info['symbol']
        except KeyError:
            continue

        token_total_price = token_info['price_info']['total_price']
        token_amount = token_info['price_info']['total_price'] / token_info['price_info']['price_per_token']

        wallet_tokens[token_symbol] = {
            'amount': round(token_amount, 4),
            'total_price': round(token_total_price, 2),
        }

        token_sum_price += token_total_price

    # SOL balance in USD
    total_solana_price = token_balance_data['nativeBalance']['total_price']
    # Account Balance in USD
    account_balance = total_solana_price + token_sum_price

    return [total_solana_price, account_balance]
