# Generated by Django 3.1.7 on 2021-09-04 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phobook', '0005_auto_20210904_1139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['organization'], 'verbose_name': 'Сотрудник', 'verbose_name_plural': 'Сотрудники'},
        ),
    ]