# Generated by Django 4.0.2 on 2022-06-11 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_alter_feedback_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
