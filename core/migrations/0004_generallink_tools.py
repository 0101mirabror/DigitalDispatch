# Generated by Django 4.0.4 on 2022-05-08 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_section_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='generallink',
            name='tools',
            field=models.ManyToManyField(blank=True, null=True, to='core.generallink'),
        ),
    ]