# Generated by Django 2.1 on 2019-04-02 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_questions_edit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='created',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='edit',
        ),
    ]
