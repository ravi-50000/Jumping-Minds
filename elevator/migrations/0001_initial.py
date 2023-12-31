# Generated by Django 2.1 on 2023-07-27 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('is_elevator_working', models.BooleanField(default=True)),
                ('current_floor', models.IntegerField(default=1)),
                ('is_door_opened', models.BooleanField(default=False)),
                ('is_door_closed', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('source_floor', models.IntegerField(blank=True, null=True)),
                ('destination_floor', models.IntegerField(blank=True, null=True)),
                ('is_elevator_moving_up', models.BooleanField()),
                ('elevator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='elevator.Elevator')),
            ],
        ),
    ]
