# Generated by Django 4.0.2 on 2022-06-11 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dailybook', '0005_alter_question_number_alter_result_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.TextField(blank=True, max_length=354, null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(max_length=254),
        ),
    ]
