# Generated by Django 5.1.2 on 2024-10-27 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_alter_transaction_entrytime_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='entryTime',
            new_name='transactionTimestamp',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='exitTime',
        ),
    ]