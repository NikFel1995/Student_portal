# Generated by Django 4.0.1 on 2022-01-05 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0004_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='group',
            field=models.ManyToManyField(related_name='courses_joined', to='classroom.Group', verbose_name='Группа'),
        ),
    ]
