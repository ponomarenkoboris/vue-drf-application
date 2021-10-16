from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.contrib.auth.models import User
from . import serializers
from .models import UserProfile
from chat.models import Message
from tasks import models
from tasks import serializers as tasks_serializers

@method_decorator(ensure_csrf_cookie, name='get')
class GetCSRFTokenView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        return Response(data={'success': 'CSRF Cookie set'})

@method_decorator(ensure_csrf_cookie, name='post')
class RegistartionView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        data = request.data
        
        first_name = data.get('firstName', None)
        last_name = data.get('lastName', None)
        username = data.get('username', None)
        password = data.get('password', None)
        re_password = data.get('rePassword', None)

        try:
            if password == re_password:

                if User.objects.filter(username=username).exists():
                    return Response(data={'error': 'User already exists.'})
                
                elif first_name is None or last_name is None:
                    return Response(data={'error': 'User should have first name and last name'})
                
                else:
                    if len(password) < 6:
                        return Response(data={'error': 'Password must be at least 6 characters.'})
                    
                    else: 
                        user = User.objects.create_user(username=username, password=password)
                        user.save()
                        user = User.objects.get(id=user.id)

                        user_profile = UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name)
                        user_profile.save()


                        user = auth.authenticate(username=username, password=password)

                        if user is None:
                            return Response(data={'error': 'Authentication error'})
                        
                        auth.login(request, user)

                        serialized_user_profile = serializers.UserProfileSerializer(user_profile)

                        return Response(
                            data={'success': 'User created successfully', 'user': serialized_user_profile.data, 'username': str(user)}, 
                            status=status.HTTP_201_CREATED
                        )

            else:
                return Response(data={'error': 'Password do not match.'})
        except:
            return Response(data={'error': 'Something went worng when registring accout'})

@method_decorator(ensure_csrf_cookie, name='post')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
        data = request.data

        username = data['username']
        password = data['password']

        user = auth.authenticate(username=username, password=password)
        
        try: 
            if user is not None:
                auth.login(request, user)
                return Response(data={'success': 'Used authenticated', 'username': username})
            else:
                return Response(data={'error': 'Error authentication'})
        except: 
            return Response(data={'error': 'Something went wrong when logging in'})

@method_decorator(csrf_protect, name='get')
class CheckUserAuth(APIView):
    """ Check if user is authenticated """
    def get(self, request):
        user = self.request.user or False

        if user is not None:
            isAuthenticated = user.is_authenticated

        try:
            if isAuthenticated:
                return Response(data={'isAuthenticated': 'success'})
            else:
                return Response(data={'isAuthenticated': 'error'})
        except:
            return Response(data={'error': 'Something went wrong while trying to check user authentication.'})

class LogoutView(APIView):
    def post(self, request):
        try:
            auth.logout(request)
            return Response(data={'success': 'Loggout out'})
        except:
            return Response(data={'error': 'Something went wrong when logging out'})

class DeleteAccountView(APIView):
    def delete(self, request):
        try:
            user = self.request.user
            user = User.objects.filter(id=user.id).delete()

            return Response(data={'success': 'User deleted successfully'})
        except:
            return Response(data={'error': 'Something went wrong when trying to delete user'})

class UpdateUserProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user

            user_instance = User.objects.get(username=str(user))

            profile = UserProfile.objects.filter(user=user_instance)

            prev_profile = UserProfile.objects.get(user=user_instance)
            first_name = request.data.get('firstName', prev_profile.first_name)
            last_name = request.data.get('lastName', prev_profile.last_name)
            avatar_image = request.data.get('avatarImage', prev_profile.avatar_image)

            if prev_profile.first_name != first_name:
                profile.update(first_name=first_name)
            
            if prev_profile.last_name != last_name:
                profile.update(last_name=last_name)

            if prev_profile.avatar_image != avatar_image:
                profile.update(avatar_image=avatar_image)

            username = request.data.get('username', None)

            if username is not None and len(username) >= 6:
                user_instance = User.objects.get(username=str(user))
                user_instance.username = username
                user_instance.save()

                # Rewrite username in other models
                Message.objects.filter(sender=str(user)).update(sender=username)
                models.Room.objects.filter(owner_username=str(user)).update(owner_username=username)
                rooms_list = tasks_serializers.RoomSerializer(models.Room.objects.filter(members__contains=str(user)), many=True)

                for room in rooms_list.data:
                    updated_members = room['members'].replace(str(user), username, 1)
                    models.Room.objects.filter(id=room['id']).update(members=updated_members)

            password = request.data.get('password', None)

            if password is not None and len(password) >= 6:
                user = User.objects.get(username=str(user))
                user.set_password(password)
                user.save()

            if username or password:
                user_name = username or str(user)
                pass_word = password or User.objects.get(username=user_name).password
                user = auth.authenticate(username=user_name, password=pass_word)
                auth.login(request, user)

            return Response(data={'succes': 'Profile has been updated successfully'}, status=status.HTTP_200_OK)

        except:
            return Response(data={'error': 'Something went wrong when trying to update user profile'})

class UserProfileView(APIView):
    def get(self, request):
        try:
            user = self.request.user
            user = User.objects.get(username=str(user))

            user_profile = UserProfile.objects.get(user=user)
            user_profile = serializers.UserProfileSerializer(user_profile)

            return Response(data={'user': user_profile.data, 'username': str(user)})

        except:
            return Response(data={'error': 'Something went wrong when trying to get user profile'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='post')
class SearchUser(APIView):

    def post(self, request):
        """ Search user """

        user = self.request.user
        username = request.data.get('username', None)

        try:
            if user is None:
                return Response(data={ 'error': 'Unauthenticated' }, status=status.HTTP_401_UNAUTHORIZED)

            if username is None or len(username) == 0:
                return Response(data={ 'error': 'Username cannot be empty string' }, status=status.HTTP_403_FORBIDDEN)

            founded_users = [instance.username for instance in User.objects.filter(username__startswith=username) if instance.username != str(user)]
            
            if len(founded_users) == 0:
                return Response(data={'success': 'User not found'}, status=status.HTTP_200_OK)
            else:
                return Response(data={ 'success': 'User founded', 'users': founded_users }, status=status.HTTP_200_OK)
        except:
            return Response(data={'error': 'Something went wrong while trying to find user.'})