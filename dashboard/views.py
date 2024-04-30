from django.shortcuts import render

from wallet.views import fungible_token_balance, nft_assets

FAQ = {
    "What is Solana?": "Solana is a high-performance blockchain platform designed for decentralized applications and crypto projects.",
    "How does Solana achieve high throughput?": "Solana achieves high throughput through its unique consensus mechanism called Proof of History (PoH), which timestamps transactions before they are included in a block.",
    "What are some key features of Solana?": "Key features of Solana include its high transaction throughput, low transaction fees, fast confirmation times, and scalability.",
    "What programming languages are supported for developing on Solana?": "Solana supports programming languages such as Rust and C, with plans to support more languages in the future.",
    "Is Solana secure?": "Yes, Solana is designed with security in mind and utilizes various cryptographic techniques to ensure the integrity and security of the network and its transactions.",
    "How can I get started with Solana development?": "To get started with Solana development, you can explore the official Solana documentation, join the Solana developer community, and experiment with building decentralized applications (dApps) on the platform."
}

def index(request):
    return render(request, 'dashboard/index.html', context={
        'faq_questions': FAQ,
    })


def portfolio(request):

    # Fungible tokens data request
    wallet_data = fungible_token_balance(request)
    # Solana Balances in USDC
    total_solana_price = round(wallet_data[0], 2)
    # Fungible tokens balance in USDC
    fungible_account_balance = wallet_data[1]
    # Nfts list
    nfts_list = nft_assets(request)[0]
    # NFTs account balance
    total_nfts_value = nft_assets(request)[1]
    # Biggest fungible token position
    biggest_position_token_name = wallet_data[2]
    biggest_position_token_balance = round(wallet_data[3], 2)
    biggest_position_balance_percentage = round(wallet_data[4], 2)
    sorted_wallet_tokens = wallet_data[5]

    # Total account balance (fungible + nfts)
    total_wallet_balance = round(fungible_account_balance +  total_nfts_value, 2)

    return render(request, 'dashboard/portfolio.html', context={
        'nfts_list': nfts_list[:15],
        'total_solana_price': total_solana_price,
        'total_wallet_balance': total_wallet_balance,
        'biggest_position_token_name': biggest_position_token_name,
        'biggest_position_token_balance': biggest_position_token_balance,
        'biggest_position_balance_percentage': biggest_position_balance_percentage,
        'sorted_wallet_tokens': sorted_wallet_tokens[:5],
    })
