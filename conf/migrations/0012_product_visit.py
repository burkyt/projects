# Generated by Django 4.2.6 on 2024-03-23 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0011_alter_task_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='visit',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]