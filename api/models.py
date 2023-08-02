from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum



# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    # access_token = models.CharField(max_length=255, blank=True, null=True)
    # refresh_token = models.CharField(max_length=255, blank=True, null=True)
    # phone_number = models.IntegerField()
    phone_number = models.CharField(max_length=20,blank=True,null=True) 

    groups = None
    user_permissions = None
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return f"{self.user.username}:{self.amount}"

        # oh we dont need to migrate for str name





from decimal import Decimal
from django.utils import timezone

class Expenditure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expenditure_type = models.CharField(max_length=30,default='Default')
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(blank=True, null=True)
    # weekly_period = models.PositiveIntegerField(blank=True, null=True)
    # monthly_period = models.PositiveIntegerField(blank=True, null=True)
    # quarterly_period = models.PositiveIntegerField(blank=True, null=True)
    # yearly_period = models.PositiveIntegerField(blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     self.user.balance.amount -= self.amount
    #     self.user.balance.save()
    
    
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.created_at:  # Check if created_at is not provided by the user
            self.created_at = timezone.now()   # Set it to the current date and time

        balance = Balance.objects.get(user=self.user)
        balance.amount -= Decimal(self.amount)
        balance.save()
        super().save(*args, **kwargs)
    
    def formatted_created_at(self):
        return self.created_at.isoformat() + 'Z'

    
    # def update_period_fields(self):
    #     # Calculate the periods based on created_at field
    #     self.weekly_period = self.created_at.isocalendar()[1]  # ISO week number
    #     self.monthly_period = self.created_at.month
    #     self.quarterly_period = (self.created_at.month - 1) // 3 + 1
    #     self.yearly_period = self.created_at.year


    def __str__(self):
        return f"Expenditure of {self.amount} by {self.user.username} on {self.expenditure_type}"

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income_type = models.CharField(max_length=30,default='Salary')
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     self.user.balance.amount -= self.amount
    #     self.user.balance.save()
    
    
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if not self.created_at:  # Check if created_at is not provided by the user
            self.created_at = timezone.now()   # Set it to the current date and time
            #keep this at first not at last after super save no save 
    
        balance = Balance.objects.get(user=self.user)
        balance.amount += Decimal(self.amount)
        balance.save()
        super().save(*args, **kwargs)
    
      
    def formatted_created_at(self):
        return self.created_at.isoformat() + 'Z'
    
    def __str__(self):
        return f"Income of {self.amount} by {self.user.username} on {self.income_type}"

class Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    debt_type = models.CharField(max_length=30,default='Deu_payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     self.user.balance.amount -= self.amount
    #     self.user.balance.save()
    
    
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        # balance = Balance.objects.get(user=self.user)
        # balance.amount += Decimal(self.amount)
        # balance.save()
    
        if not self.created_at:  # Check if created_at is not provided by the user
            self.created_at = timezone.now()   # Set it to the current date and time
        super().save(*args, **kwargs)
    
      
    def formatted_created_at(self):
        return self.created_at.isoformat() + 'Z'


    def __str__(self):
        return f"Debt of {self.amount} by {self.user.username} on {self.debt_type}"

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions',default=None)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions',default=None)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # balance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    transaction_count =  models.DecimalField(max_digits=3, decimal_places=0,default=10) 
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.sender} to {self.receiver}"


class Portfolio_History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()  # This is updated based on buy/sell actions.
    stock_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_sold = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return f"Stock {self.user} and {self.quantity} and {self.quantity} {self.stock_symbol} stocks sold:{self.stock_sold}"



class Portfolio(models.Model):
    TRADE_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    portfolio_history = models.ForeignKey(Portfolio_History,on_delete=models.CASCADE,default=None)
    quantity = models.PositiveIntegerField()
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES,default=None)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock {self.trade_type} by {self.user.username}: {self.stock_symbol} No.{self.quantity}"



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    alert_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Alert for {self.user.username}: {self.stock_symbol} at {self.alert_price}"
