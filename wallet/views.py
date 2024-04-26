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
                elif len(nft_name) > 17:
                    nft_name = nft_name[:17] + '...'
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
    # Total wallet balance (excluding SOL)
    token_sum_price = 0
    # Biggest position
    biggest_position_token_name = ''
    biggest_position_token_balance = 0
    # SOL balance in USD
    total_solana_price = token_balance_data['nativeBalance']['total_price']
    # SOL price
    solana_price = token_balance_data['nativeBalance']['price_per_sol']

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
        # Total wallet balance (excluding SOL)
        token_sum_price += token_total_price

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
    account_balance = total_solana_price + token_sum_price
    # Biggest position percentage
    biggest_position_balance_percentage = biggest_position_token_balance / account_balance * 100

    return [total_solana_price, account_balance, biggest_position_token_name, biggest_position_token_balance, biggest_position_balance_percentage, sorted_wallet_tokens]
