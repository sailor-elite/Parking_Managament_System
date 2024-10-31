# Generated by Django 5.1.2 on 2024-10-29 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0003_rename_parkingname_parking_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parking',
            name='blueZoneSpaces',
        ),
        migrations.RemoveField(
            model_name='parking',
            name='greenZoneSpaces',
        ),
        migrations.RemoveField(
            model_name='parking',
            name='redZoneSpaces',
        ),
        migrations.AddField(
            model_name='parking',
            name='capacity',
            field=models.IntegerField(default=66),
        ),
        migrations.AddField(
            model_name='parking',
            name='zone',
            field=models.CharField(choices=[('greenZone', 'Green Zone'), ('blueZone', 'Blue Zone'), ('redZone', 'Red Zone')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
