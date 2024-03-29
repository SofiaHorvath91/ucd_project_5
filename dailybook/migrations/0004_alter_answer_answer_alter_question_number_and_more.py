# Generated by Django 4.0.2 on 2022-06-11 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dailybook', '0003_result_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.TextField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='number',
            field=models.IntegerField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='point',
            field=models.IntegerField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='result',
            field=models.TextField(blank=True, max_length=354, null=True),
        ),
    ]
