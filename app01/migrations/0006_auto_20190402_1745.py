# Generated by Django 2.1 on 2019-04-02 17:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_auto_20190402_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questions',
            name='edit',
            field=models.DateField(auto_now=True),
        ),
    ]
