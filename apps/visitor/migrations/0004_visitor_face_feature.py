# Generated by Django 5.1.3 on 2024-11-13 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0003_visitorfacefeatures'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='face_feature',
            field=models.BinaryField(null=True),
        ),
    ]