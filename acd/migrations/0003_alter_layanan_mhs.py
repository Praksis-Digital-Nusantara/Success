# Generated by Django 4.2 on 2025-05-18 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acd', '0002_alter_layanan_mhs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layanan',
            name='mhs',
            field=models.ForeignKey(default='00', on_delete=django.db.models.deletion.CASCADE, related_name='layanan_mhs', to='acd.usermhs'),
            preserve_default=False,
        ),
    ]
