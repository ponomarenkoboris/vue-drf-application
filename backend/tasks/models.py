from django.db import models

class Room(models.Model):
    room_name = models.CharField(max_length=255)
    room_description = models.TextField(blank=True)
    owner_username = models.CharField(max_length=255)
    members = models.TextField()

    def __str__(self):
        return self.room_name

class TaskGroup(models.Model):
    room = models.ForeignKey(Room, related_name='task_groups', null=True, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=255, default='Untitled')
    group_description = models.TextField()
    date_craeted = models.DateTimeField(auto_now=True, db_index=True)

class Task(models.Model):
    task_group = models.ForeignKey(TaskGroup, related_name='tasks', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True, db_index=True)