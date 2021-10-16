from rest_framework import serializers
from .models import Room, Task, TaskGroup

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'date_created', 'completed']

    def update(self, instance, validated_data):
        return Task.objects.create(task_group=instance, **validated_data)


class TaskGroupSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = TaskGroup
        fields = ['id', 'group_name', 'group_description', 'tasks']

    def create(self, validated_data):
        tasks = validated_data.pop('tasks')
        room = validated_data.pop('room')
        task_group_instance = TaskGroup.objects.create(room=room, **validated_data)

        for task in tasks:
            Task.objects.create(tasks=task_group_instance, **task)

        return task_group_instance

class RoomSerializer(serializers.ModelSerializer):
    task_groups = TaskGroupSerializer(many=True)

    class Meta:
        model = Room
        fields = [
            'id', 
            'room_name', 
            'room_description',
            'owner_username', 
            'members',
            'task_groups'
        ]