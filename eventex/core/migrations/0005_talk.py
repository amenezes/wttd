# Generated by Django 2.2.2 on 2019-07-09 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190709_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='título')),
                ('start', models.TimeField(verbose_name='início')),
                ('description', models.TextField(verbose_name='descrição')),
                ('speakers', models.ManyToManyField(to='core.Speaker')),
            ],
        ),
    ]