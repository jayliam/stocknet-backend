# Generated by Django 2.2 on 2020-04-07 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0016_stocktrack'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocktrack',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stocktracklist', to=settings.AUTH_USER_MODEL),
        ),
    ]
