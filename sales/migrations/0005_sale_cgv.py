# Generated by Django 2.1 on 2021-11-27 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_auto_20190312_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='cgv',
            field=models.CharField(default='https://assos.utc.fr/woolly/cgv.pdf', max_length=1000),
        ),
    ]