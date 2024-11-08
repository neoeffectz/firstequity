# Generated by Django 4.2.16 on 2024-10-21 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rockwellbank', '0022_alter_portfolio_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='amount_sign',
            field=models.CharField(blank=True, choices=[('$', 'Dollar'), ('£', 'Pound'), ('€', 'Euro'), ('₩', 'Korean Won')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='transactions',
            name='amount_sign',
            field=models.CharField(blank=True, choices=[('$', 'Dollar'), ('£', 'Pound'), ('€', 'Euro'), ('₩', 'Korean Won')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='transactions',
            name='purpose_of_the_transfer',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
