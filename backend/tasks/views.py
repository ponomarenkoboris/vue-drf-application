from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task, TaskGroup, Room
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from . import serializers

class RoomMembersView(APIView):
    """
    View for room members logic

    f: put - Append member to the room (only if user is room owner)
    f: delete - Remove member form th room (only if user is room ownwer)
    """
    def put(self, request):
        """ Append member to the room """
        user = self.request.user
        room_id = request.data.get('roomId', None)
        member_username = request.data.get('memberUserName', None)

        if member_username is None:
            return Response(data={'error': 'Invalid member username'}, status=status.HTTP_400_BAD_REQUEST)
        
        if room_id is None:
            return Response(data={'error': 'Invalid room id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.filter(id=room_id, owner_username=str(user)).first()

            if room is None:
                return Response(data={'error': 'Cannot find room'}, status=status.HTTP_400_BAD_REQUEST)
            
            members_list = serializers.RoomSerializer(room).data['members'].split(',')
                    
            for member in members_list:
                if member == member_username:
                    return Response(data={'error': 'User already in this group'}, status=status.HTTP_409_CONFLICT)
            
            members_list.append(member_username)

            Room.objects.filter(id=room_id, owner_username=str(user)).update(members=",".join(members_list))

            return Response(data={'success': 'User has been added to room members list'}, status=status.HTTP_200_OK)

        except:
            return Response(data={'error': 'Something went wrong while trying to append user to the room'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """ Remove member from group """
        user = self.request.user
        room_id = request.data.get('roomId', None)
        member_username = request.data.get('memberUserName', None)

        if member_username is None:
            return Response(data={'error': 'Invalid member username'}, status=status.HTTP_400_BAD_REQUEST)
        
        if room_id is None:
            return Response(data={'error': 'Invalid room id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.filter(id=room_id, owner_username=str(user)).first()

            if room is None:
                return Response(data={'error': 'Cannot find room'}, status=status.HTTP_400_BAD_REQUEST)
            
            members_list = serializers.RoomSerializer(room).data['members'].split(',')

            members_list.remove(member_username)
            
            Room.objects.filter(id=room_id, owner_username=str(user)).update(members=','.join(members_list))

            return Response(data={'success': 'User has been removed from room members'}, status=status.HTTP_200_OK)

        except:
            return Response(data={'error': 'Something went worng while tyring to remove user from thr room.'})

@method_decorator(csrf_protect, name='get')
class OneRoomView(APIView):
    """ Get one room """
    def get(self, request, room_name):
        user = self.request.user
        
        room_name = room_name.replace('&', ' ')

        if room_name is None:
            return Response(data={'error': 'Room name cannot be an empty value'}, status=status.HTTP_400_BAD_REQUEST)

        room = Room.objects.get(room_name=room_name)
        room = serializers.RoomSerializer(room)

        room_members = room.data.get('members').split(',')

        for member in room_members:
            if member == str(user):
                return Response(data={'success': 'Room exist', 'room': room.data})

        return Response(data={'error': 'Cannot find room'})


@method_decorator(csrf_protect, name='dispatch')
class RoomView(APIView):
    """
    View for rooms logic

    f: post - Create new room
    f: get - Get rooms list for current user
    f: delete - Delete room (only if user is room owner)
    f: put - Append user to the room (only if user is room owner) 

    """
    def post(self, request):
        """ Create room """
        user = self.request.user

        room_name = request.data.get('roomName', None)
        room_description = request.data.get('roomDescription', None)

        try:
            if room_name is None:
                return Response(data={'error': 'Group name cannot be empty value'})
            
            if room_description is None:
                return Response(data={'error': 'Group description cannot be empty value'})

            room = Room.objects.create(
                room_name=room_name, 
                room_description=room_description, 
                owner_username=str(user), 
                members=str(user)
            )
            room.save()

            room = serializers.RoomSerializer(room)
            print(room.data)

            return Response(data={'success': 'Room created', 'room': room.data})

        except:
            return Response(data={'error': 'Something went worng while trying to create room'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """ Get rooms names list """
        user = self.request.user

        try:
            rooms = Room.objects.filter(members__contains=str(user))
            rooms = serializers.RoomSerializer(rooms, many=True)

            rooms_list = []

            for room in rooms.data:
                members = room.get('members').split(',')

                for member in members:
                    if member == str(user):
                        rooms_list.append(room.get('room_name'))
            
            if len(rooms_list) > 0:
                return Response(data={'success': 'Rooms found', 'rooms': rooms_list}, status=status.HTTP_200_OK)
                
            else:
                return Response(data={'success': 'User is not registered in any rooms'}, status=status.HTTP_200_OK)

        except:
            return Response(data={'error': 'Something went wrong while trying to get rooms'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """ Delete room """

        user = self.request.user

        room_id = request.data.get('roomId', None)

        if room_id is None:
            return Response(data={'error': 'Cannot delete room with id none'})

        try:
            room = Room.objects.filter(id=room_id, owner_username=str(user))

            if room is None:
                return Response(data={'error': 'Cannot find room with this room id and owner username'})

            room.delete()

            return Response(data={'success': 'Room was successfully deleted'}, status=status.HTTP_200_OK)
        except: 
            return Response(data={'error': 'Somethong went wrong while trying to delete room'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class TaskGroupsView(APIView):
    """
    View for task groups logic

    f: post - Create new task group in room (only if user is room owner)
    f: delete - Delete task group (only if user is room owner)

    """

    def post(self, request):
        """ Create Task Group """

        user = self.request.user
        room_id = request.data.get('roomId', None)
        group_name = request.data.get('groupName', None)
        group_description = request.data.get('groupDescription', None)

        if group_name is None or group_description is None or room_id is None:
            return Response(data={'error': 'Invalid input value'}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            room = Room.objects.get(id=room_id, owner_username=str(user))

            if room is None:
                return Response(data={'error': 'Cannot find room'}, status=status.HTTP_404_NOT_FOUND)

            task_group = TaskGroup.objects.create(
                room=room,
                group_name=group_name, 
                group_description=group_description
            )
            task_group.save()

            task_group = serializers.TaskGroupSerializer(task_group)

            return Response(data={'success': 'Task group was successfully created', 'taskGroup': task_group.data}, status=status.HTTP_201_CREATED)

        except:
            return Response(data={'error': 'Something went wrong while trying to create new task group'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """ Delete task group """

        user = self.request.user
        room_id = request.data.get('roomId', None)
        task_group_id = request.data.get('taskGroupId', None)

        if room_id is None:
            return Response(data={'error': 'Room id cannot be empty value'}, status=status.HTTP_400_BAD_REQUEST)
        
        if task_group_id is None:
            return Response(data={'error': 'Task group id cannot be empty value'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(id=room_id, owner_username=str(user))

            if room is None:
                return Response(data={'error': 'Cannot find room'})
            
            task_group = TaskGroup.objects.filter(room=room, id=task_group_id)
            task_group.delete()

            return Response(data={'success': 'Task group was deleted successfully'}, status=status.HTTP_200_OK)
        
        except:
            return Response(data={'error': 'Something went wrong while trying to delete task group'}, status=status.HTTP_400_BAD_REQUEST)
        
@method_decorator(csrf_protect, name='dispatch')
class TaskView(APIView):
    """
    View for task logic

    f: post - Create new task in task group (only if user is room owner)
    f: delete - Delete task in task group (only if user is room owner)
    f: put - Change task status (for all users in room)
    """
    def post(self, request):
        user = self.request.user
        room_id = request.data.get('roomId', None)
        task_group_id = request.data.get('taskGroupId', None)
        title = request.data.get('taskTitle', None)
        description = request.data.get('taskDescription', None)

        if task_group_id is None or title is None or description is None or room_id is None:
            return Response(data={'error': 'Invalid task data'})
        
        try:            
            room = Room.objects.get(id=room_id, owner_username=str(user))

            if room is None: 
                return Response(data={'error': 'Cannot find room'}, status=status.HTTP_400_BAD_REQUEST)

            task_group = TaskGroup.objects.get(id=task_group_id, room=room)

            if task_group is None:
                return Response(data={'error': 'Cannot find task group'}, status=status.HTTP_400_BAD_REQUEST)

            task = Task.objects.create(task_group=task_group, title=title, description=description)
            task.save()

            task = serializers.TaskSerializer(task)

            return Response(data={'success': 'Task was successfully created', 'task': task.data}, status=status.HTTP_201_CREATED)

        except:
            return Response(data={'error': 'Something went worng while trying to create task'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        """ Remove task """
        user = self.request.user
        room_id = request.data.get('roomId', None)
        task_group_id = request.data.get('taskGroupId', None)
        task_id = request.data.get('taskId', None)

        if room_id is None or task_group_id is None or task_id is None:
            return Response(data={'error': 'Invalid task data'})
        
        try:
            room = Room.objects.get(id=room_id, owner_username=str(user))

            if room is None:
                return Response(data={'error': 'Cannot find room'}, status=status.HTTP_400_BAD_REQUEST)
            
            task_group = TaskGroup.objects.get(room=room, id=task_group_id)

            if task_group is None:
                return Response(data={'error': 'Cannot find task group'}, status=status.HTTP_400_BAD_REQUEST)

            task = Task.objects.filter(task_group=task_group, id=task_id)

            if task is None:
                return Response(data={'error': 'Cannot find task'}, status=status.HTTP_400_BAD_REQUEST)

            task.delete()

            return Response(data={'success': 'Task was successfully deleted'})

        except:
            return Response(data={'error': 'Something went worng while trying to delete task'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """ Change task status """
        user = self.request.user
        room_id = request.data.get('roomId', None)
        task_group_id = request.data.get('taskGroupId', None)
        task_id = request.data.get('taskId', None)
        task_status = request.data.get('taskStatus', None)

        if room_id is None or task_group_id is None or task_id is None or task_status is None:
            return Response(data={'error': 'Invalid task data'})

        try:            
            room = Room.objects.filter(id=room_id, members__contains=str(user)).first()
            
            if room is None:
                return Response(data={'error': 'Cannot find room'}, status=status.HTTP_400_BAD_REQUEST)
            
            task_group = TaskGroup.objects.get(room=room, id=task_group_id)
            
            if task_group is None:
                return Response(data={'error': 'Cannot find task group'}, status=status.HTTP_400_BAD_REQUEST)

            task = Task.objects.filter(task_group=task_group, id=task_id)
            
            if task is None:
                return Response(data={'error': 'Cannot find task'}, status=status.HTTP_400_BAD_REQUEST)
            
            task.update(completed=task_status)
            
            return Response(data={'success': 'Task status was successfully changed'}, status=status.HTTP_200_OK)

        except:
            return Response(data={'error': 'Something went worng while trying to change task status'}, status=status.HTTP_400_BAD_REQUEST)