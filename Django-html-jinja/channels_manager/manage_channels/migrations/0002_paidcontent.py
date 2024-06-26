# Generated by Django 4.2.11 on 2024-04-16 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_channels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaidContent',
            fields=[
                ('paid_content_id', models.AutoField(primary_key=True, serialize=False)),
                ('content_name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('content_HTML', models.TextField()),
            ],
            options={
                'db_table': 'paid_content',
            },
        ),
    ]
