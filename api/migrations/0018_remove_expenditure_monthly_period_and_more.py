# Generated by Django 4.2.1 on 2023-07-03 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_portfolio_history_stock_sold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expenditure',
            name='monthly_period',
        ),
        migrations.RemoveField(
            model_name='expenditure',
            name='quarterly_period',
        ),
        migrations.RemoveField(
            model_name='expenditure',
            name='weekly_period',
        ),
        migrations.RemoveField(
            model_name='expenditure',
            name='yearly_period',
        ),
    ]
