from django.core.management.base import BaseCommand
from authentication.models import UserAuth
from snapshot.models import WalletSnapshot

from snapshot.views import snapshot

class Command(BaseCommand):
    help = "Creates wallet balance snapshot for all users"

    def handle(self, *args, **kwargs):
        users = UserAuth.objects.filter(solana_wallet__isnull=False)

        for user in users:
            wallet_balances = snapshot(user) # Return (account_balance, solana_wallet_balance)
            total_wallet_balance = wallet_balances[0] # account_balance
            solana_wallet_balance = wallet_balances[1] # solana_wallet_balance

            wallet_snapshot = WalletSnapshot.objects.create(
                wallet_balance=total_wallet_balance,
                solana_wallet_balance=solana_wallet_balance,
                user=user
            )

            wallet_snapshot.save()
            self.stdout.write(self.style.SUCCESS(f'Snapshot for {user.username} has been created.'))