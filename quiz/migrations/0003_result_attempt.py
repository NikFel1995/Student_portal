# Generated by Django 4.0.1 on 2022-01-08 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_alter_quiz_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='attempt',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Попытка'),
        ),
    ]