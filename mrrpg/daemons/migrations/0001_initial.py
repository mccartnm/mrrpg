# Generated by Django 3.0.3 on 2020-02-19 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('campaign', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chassis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Daemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('health', models.IntegerField()),
                ('fuel', models.IntegerField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.Campaign')),
                ('chassis', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='daemons.Chassis')),
            ],
        ),
        migrations.CreateModel(
            name='Hardpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HardpointType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('required_energy', models.IntegerField()),
                ('_stats', models.TextField()),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='daemons.HardpointType')),
            ],
        ),
        migrations.CreateModel(
            name='Mount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operational', models.BooleanField(default=True)),
                ('_stats', models.TextField()),
                ('daemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daemons.Daemon')),
                ('hardpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daemons.Hardpoint')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='daemons.Item')),
            ],
        ),
        migrations.CreateModel(
            name='HardpointConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chassis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections', to='daemons.Chassis')),
                ('hardpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections', to='daemons.Hardpoint')),
                ('supports', models.ManyToManyField(to='daemons.HardpointType')),
            ],
        ),
        migrations.AddField(
            model_name='daemon',
            name='mounts',
            field=models.ManyToManyField(through='daemons.Mount', to='daemons.Item'),
        ),
        migrations.AddField(
            model_name='daemon',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='daemons', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chassis',
            name='hardpoints',
            field=models.ManyToManyField(through='daemons.HardpointConnection', to='daemons.Hardpoint'),
        ),
    ]
