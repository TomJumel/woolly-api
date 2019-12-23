# Generated by Django 2.2.3 on 2019-08-05 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_auto_20190805_2345'),
        ('authentication', '0002_auto_20190312_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='associations',
            field=models.ManyToManyField(through='sales.AssociationMember', to='sales.Association'),
        ),
    ]