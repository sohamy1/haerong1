# Generated by Django 3.2.5 on 2021-08-02 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210802_1354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='qustion_key',
            new_name='question_key',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='qustion_value',
            new_name='question_value',
        ),
    ]
