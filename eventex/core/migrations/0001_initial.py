# Generated by Django 3.0.6 on 2020-05-30 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='nome')),
                ('slug', models.SlugField()),
                ('photo', models.URLField(verbose_name='link da foto')),
                ('website', models.URLField(verbose_name='link do site')),
                ('description', models.TextField(verbose_name='descrição')),
            ],
        ),
    ]