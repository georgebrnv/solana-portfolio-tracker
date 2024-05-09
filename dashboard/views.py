from django.shortcuts import render, redirect
from django.db import connection
from django.db.utils import OperationalError
from datetime import datetime, timezone
from django.contrib import messages

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
    user = request.user
    if user.solana_wallet is None:
        messages.error(request, 'You need to connect your wallet first to see Portfolio page.')
        return redirect('profile')
    # Fungible tokens data request
    wallet_data = fungible_token_balance(request)
    # Solana Balances in USDC
    total_solana_price = round(wallet_data[0], 2)
    # Fungible tokens balance in USDC
    fungible_account_balance = wallet_data[1]
    # Nfts list
    nfts_list = nft_assets(request)[0]
    # NFTs account balance
    total_nfts_value = wallet_data[6]
    # Biggest fungible token position
    biggest_position_token_name = wallet_data[2]
    biggest_position_token_balance = round(wallet_data[3], 2)
    biggest_position_balance_percentage = round(wallet_data[4], 2)
    sorted_wallet_tokens = wallet_data[5]

    # Wallet Snapshots Data
    wallet_snapshots_data = balance_chart(request)

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
        'wallet_snapshots_data': wallet_snapshots_data,
        'fungible_account_balance': fungible_account_balance,
        'nft_account_balance': total_nfts_value,
    })

def balance_chart(request):
    user = request.user

    wallet_balance_data_query = f"""
    SELECT
        timestamp_datetime AS timestamp_datetime,
        wallet_balance AS wallet_balance,
        solana_wallet_balance AS solana_wallet_balance
    FROM snapshot_walletsnapshot
    WHERE user_id = {user.id}
    """

    wallet_balance_data = execute_sql_query(wallet_balance_data_query)

    user_snapshot_data = {
        "day_1": [],
        "week_1": [],
        "month_1": [],
        "month_3": [],
        "month_6": [],
        "year_1": []
    }

    last_day_snapshot_date = None
    last_week_snapshot_date = None
    last_month_snapshot_date = None
    last_half_year_snapshot_date = None
    last_year_snapshot_date = None

    for row in wallet_balance_data:
        timestamp_datetime = row['timestamp_datetime']
        wallet_balance = row['wallet_balance']
        solana_wallet_balance = row['solana_wallet_balance']

        daily_snapshot = {"timestamp_datetime": timestamp_datetime.strftime("%m/%d/%Y %H:%M"), "wallet_balance": wallet_balance, "solana_wallet_balance": solana_wallet_balance}
        snapshot = {"day": timestamp_datetime.strftime("%m/%d/%Y"), "wallet_balance": wallet_balance, "solana_wallet_balance": solana_wallet_balance}

        days_diff = (datetime.now(timezone.utc) - timestamp_datetime).days

        if days_diff == 0:
            user_snapshot_data['day_1'].append(daily_snapshot)
        if timestamp_datetime.date() != last_day_snapshot_date and days_diff <= 7:
            user_snapshot_data['week_1'].append(snapshot)
            last_day_snapshot_date = timestamp_datetime.date()
        if timestamp_datetime.date() != last_week_snapshot_date and days_diff <= 30:
            user_snapshot_data['month_1'].append(snapshot)
            last_week_snapshot_date = timestamp_datetime.date()
        if timestamp_datetime.date() != last_month_snapshot_date and days_diff <= 90:
            user_snapshot_data['month_3'].append(snapshot)
            last_month_snapshot_date = timestamp_datetime.date()
        if timestamp_datetime.date() != last_half_year_snapshot_date and days_diff <= 180:
            user_snapshot_data['month_6'].append(snapshot)
            last_half_year_snapshot_date = timestamp_datetime.date()
        if timestamp_datetime.date() != last_year_snapshot_date and days_diff <= 365:
            user_snapshot_data['year_1'].append(snapshot)
            last_year_snapshot_date = timestamp_datetime.date()

    return user_snapshot_data

def execute_sql_query(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            # Store column names (col[0]) in the 'columns' variable
            columns = [col[0] for col in cursor.description]
            # Fetch all the rows from executed query
            rows = cursor.fetchall()

            # List comprehension iterates through each row and creates a list of
            # dictionaries and pair column name with the corresponding value (key: value)
            return [dict(zip(columns, row)) for row in rows]
    except OperationalError as e:
        print(f"Database Error: {e}")
        return []