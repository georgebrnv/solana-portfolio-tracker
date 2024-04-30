from django.db import models

from authentication.models import UserAuth

class WalletSnapshot(models.Model):
    timestamp_datetime = models.DateTimeField(auto_now_add=True)
    wallet_balance = models.FloatField()
    solana_wallet_balance = models.FloatField()
    user = models.ForeignKey(to=UserAuth, on_delete=models.CASCADE)
