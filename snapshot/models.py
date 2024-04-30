from django.db import models

from authentication.models import UserAuth

class WalletSnapshot(models.Model):
    timestamp_datetime = models.DateTimeField(auto_now_add=True)
    wallet_balance = models.FloatField()
    solana_wallet_balance = models.FloatField()
    user = models.ForeignKey(to=UserAuth, on_delete=models.CASCADE)

    class Meta:
        # The order of fields in the db when obtaining lists of objects.
        ordering = ['user', 'timestamp_datetime', 'wallet_balance', 'solana_wallet_balance']

    def __str__(self):
        return f"""
        USERNAME: {self.user}, 
        SNAPSHOT_DATE: {self.timestamp_datetime}, 
        WALLET_BALANCE: {self.wallet_balance}, 
        SOLANA BALANCE (in USDC): {self.solana_wallet_balance}.
        """