# Generated by Django 4.2.4 on 2023-09-04 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonDRF", "0009_menuitem_inventory"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="slug",
        ),
    ]
