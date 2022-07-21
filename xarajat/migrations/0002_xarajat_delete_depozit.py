# Generated by Django 4.0.6 on 2022-07-17 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xarajat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Xarajat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.PositiveBigIntegerField()),
                ('comment', models.CharField(max_length=64)),
                ('price', models.PositiveIntegerField(default=0, verbose_name='summa (UZS)')),
            ],
        ),
        migrations.DeleteModel(
            name='Depozit',
        ),
    ]
