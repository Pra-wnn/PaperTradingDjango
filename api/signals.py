from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,Balance,Expenditure, Transaction,Portfolio,Income
from decimal import Decimal

# @receiver(post_save, sender=Expenditure)
# def update_balance(sender, instance, created, **kwargs):
#     if created:
#         balance = instance.balance
#         balance.amount -= instance.amount
#         balance.save()
#         Transaction.objects.create(balance=balance, amount=instance.amount)



@receiver(post_save, sender=User)
def create_related_instances(sender, instance, created, **kwargs):
    if created:
        balance=Balance.objects.create(user=instance, amount=0.0)
        Expenditure.objects.create(user=instance,  amount=0.0)
        Income.objects.create(user=instance,  amount=0.0)
        # Transaction.objects.create(user=instance, balance=instance.balance, amount=0.0)



@receiver(post_save, sender=Transaction)
def  update_balances(sender, instance, created, **kwargs):
    if created:
        sender_balance = Balance.objects.get(user=instance.sender)
        receiver_balance = Balance.objects.get(user=instance.receiver)

        

        sender_balance.amount -= instance.amount
        sender_balance.save()

        receiver_balance.amount += instance.amount
        receiver_balance.save()
# Have to initialise the account foreign key data such as balance,Expenditure,Transaction to 0

@receiver(post_save, sender=Portfolio)
def deduct_balance(sender, instance, created, **kwargs):
    if created:
        # Get the user from the portfolio instance
        user = instance.user

        # Deduct the buy price from the user's balance
        user.balance.amount -= Decimal(instance.buy_price)
        user.balance.save()