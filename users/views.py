from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from djoser.views import TokenCreateView
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from firebase_admin import auth
from firebase_admin._auth_utils import UserNotFoundError
import firebase_admin
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import UserProfile
from users.serializers import UserProfileSerializer, UserCreateSerializer


# Create your views here.


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CustomTokenCreateView(TokenCreateView):
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_by_uid(request):
    uid = request.GET.get('uid')
    if not uid:
        return JsonResponse({'error': 'UID required'}, status=400)
    return get_user(uid=uid)


def get_user(uid=None, email=None):
    if uid:
        try:
            user = auth.get_user(uid)
            return return_response(user)
        except UserNotFoundError:
            return JsonResponse({'error': 'User not found'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif email:
        try:
            user = auth.get_user_by_email(email)
            return return_response(user)
        except UserNotFoundError:
            return JsonResponse({'error': 'User not found'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Bad Request'}, status=400)


def return_response(user):
    return JsonResponse(
        {
            'uid': user.uid,
            'email': user.email,
            'phone_number': user.phone_number,
            'display_name': user.display_name,
        }, status=200
    )


@api_view(['GET'])
@permission_classes(AllowAny)
def get_user_by_email(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'error': 'User not found'}, status=400)
    return get_user(email=email)
