# Generated by Django 3.2 on 2021-04-26 13:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('docfile', models.FileField(upload_to='documents/')),
            ],
        ),
    ]
