# Generated by Django 3.1.7 on 2021-09-05 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phobook', '0010_auto_20210905_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='organization',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='organizations_of_employees', to='phobook.organization', verbose_name='Организация'),
        ),
    ]