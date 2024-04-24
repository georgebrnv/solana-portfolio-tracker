from django.db import models

class SolanaWallet(models.Model):
    solana_wallet_address = models.CharField(max_length=44)

