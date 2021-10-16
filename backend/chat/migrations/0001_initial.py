# Generated by Django 3.2.7 on 2021-10-11 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('message_send_date', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chatroom')),
            ],
        ),
    ]
