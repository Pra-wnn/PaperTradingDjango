# Generated by Django 4.2.1 on 2023-06-21 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_expenditure_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_count',
            field=models.DecimalField(decimal_places=0, default=10, max_digits=3),
        ),
    ]
