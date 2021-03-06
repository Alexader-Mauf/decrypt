# Generated by Django 3.1.6 on 2021-03-01 12:18

import core.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('name', models.CharField(default=None, max_length=255)),
                ('iban', models.CharField(default=core.models.BankAccount._generate_iban, max_length=255, primary_key=True, serialize=False, unique=True, verbose_name='IBAN')),
                ('balance', models.DecimalField(decimal_places=4, default=0.0, max_digits=22)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BankCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(default='None', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bank_customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bankkunde',
                'verbose_name_plural': 'Bankkunden',
            },
        ),
        migrations.CreateModel(
            name='BankTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_case', models.TextField(verbose_name='Verwendungszweck')),
                ('executionlog', models.TextField(default='erstellt')),
                ('execute_datetime', models.DateTimeField(default=datetime.datetime(2021, 3, 2, 12, 18, 20, 421971, tzinfo=utc))),
                ('is_open', models.BooleanField(default=True)),
                ('is_success', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=22)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_by', to='core.bankcustomer', verbose_name='Auftraggeber')),
                ('iban_from', models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, related_name='Überweisender', to='core.bankaccount', verbose_name='Überweisender')),
                ('iban_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Begünstigter', to='core.bankaccount', verbose_name='Begünstigter')),
            ],
        ),
        migrations.CreateModel(
            name='RepeatedTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(choices=[('weekly', 'Wöchentlich'), ('monthly', 'Monatlich'), ('yearly', 'Jährlich')], default='monthly', max_length=7)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('transaction_to_be_repeated', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='to_be_repeated', to='core.banktransfer', verbose_name='Dauerauftrag')),
            ],
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='account_owned_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_owned_by', to='core.bankcustomer', verbose_name='Inhaber'),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='administrated_by',
            field=models.ManyToManyField(default=None, related_name='administrating_accounts', to='core.BankCustomer'),
        ),
    ]
