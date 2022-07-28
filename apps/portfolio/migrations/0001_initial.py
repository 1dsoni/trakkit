# Generated by Django 4.0.6 on 2022-07-28 20:08

import commons.db.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_id', models.CharField(default=commons.db.models.random_ref_id, max_length=64, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.IntegerField(default=0)),
                ('user_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'portfolio',
                'ordering': ('-id',),
                'unique_together': {('user_id', 'name', 'is_deleted')},
            },
        ),
        migrations.CreateModel(
            name='PortfolioSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_id', models.CharField(default=commons.db.models.random_ref_id, max_length=64, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.IntegerField(default=0)),
                ('user_id', models.CharField(max_length=255)),
                ('ticker', models.CharField(max_length=255)),
                ('average_amount', models.DecimalField(decimal_places=2, max_digits=65, null=True)),
                ('volume', models.PositiveIntegerField(null=True)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='summary', to='portfolio.portfolio')),
            ],
            options={
                'db_table': 'portfolio_summary',
                'ordering': ('-id',),
                'unique_together': {('user_id', 'portfolio_id', 'ticker', 'is_deleted')},
            },
        ),
    ]
