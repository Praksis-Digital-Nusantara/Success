# Generated by Django 4.2 on 2025-05-18 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acd', '0005_alter_layanan_mhs_alter_layanan_mhs2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layanan',
            name='mhs2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='layanan_mhs', to='acd.usermhs'),
        ),
    ]
