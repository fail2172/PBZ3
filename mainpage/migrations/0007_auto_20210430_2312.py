# Generated by Django 3.1.7 on 2021-04-30 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0006_auto_20210425_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subconcept1',
            name='sub_concepts2',
        ),
        migrations.DeleteModel(
            name='SubConcept2',
        ),
    ]
