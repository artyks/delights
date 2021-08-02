# Generated by Django 3.2.5 on 2021-07-28 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='purchase',
        ),
        migrations.AddField(
            model_name='purchase',
            name='menu_item',
            field=models.ManyToManyField(related_name='purchases', to='website_app.MenuItem'),
        ),
    ]
