from random import randint
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_200_OK
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from taskapp.twilio import send_sms
from .models import User
from .serializers import UserSerializer


@api_view(['POST'])
def register(request):
    if 'phone_number' not in request.data or 'priority' not in request.data:
        return Response({'error': 'Missing credentials'}, status=HTTP_400_BAD_REQUEST)

    if User.objects.filter(phone_number=request.data['phone_number']).exists():
        return Response({
            'error': f"An account already exists with {request.data['phone_number']} phone_number. Please login."
        }, status=HTTP_403_FORBIDDEN)

    try:
        new_user = User.objects.create_user(phone_number=request.data['phone_number'],
                                            password=None,
                                            priority=request.data['priority'])
    except ValueError as e:
        return Response({'error': "Oops! something went wrong"}, status=HTTP_400_BAD_REQUEST)

    return Response(UserSerializer(new_user, many=False).data, status=HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    if 'phone_number' not in request.data:
        return Response({'error': 'Missing credentials'}, status=HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(phone_number=request.data['phone_number'])
    except (ObjectDoesNotExist, ValueError):
        return Response({'error': 'Invalid phone number'}, status=HTTP_403_FORBIDDEN)

    user.otp = randint(100000, 999999)
    user.save()

    send_sms(f'Your OTP for TaskApp is {user.otp}',
             f'{user.country_code}{user.phone_number}')

    return Response({'success': 'OTP sent successfully'}, status=HTTP_200_OK)


@api_view(['POST'])
def token(request):
    if 'phone_number' not in request.data or \
            'otp' not in request.data:
        return Response({'error': 'Missing credentials'}, status=HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(phone_number=request.data['phone_number'])
    except (ObjectDoesNotExist, ValueError):
        return Response({'error': 'Invalid phone number'}, status=HTTP_403_FORBIDDEN)

    if user.otp is None or request.data['otp'] != user.otp:
        return Response({'error': 'Invalid otp'}, status=HTTP_403_FORBIDDEN)

    user.otp = None
    user.save()

    return Response({
        "access": str(AccessToken.for_user(user)),
        "refresh": str(RefreshToken.for_user(user))
    }, status=HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def user(request):
    if request.method == 'GET':
        return Response(UserSerializer(request.user, many=False).data, HTTP_200_OK)
    elif request.method == 'PUT' or request.method == 'PATCH':
        if 'priority' in request.data:
            request.user.priority = request.data['priority']
        if 'phone_number' in request.data:
            if User.objects.filter(phone_number=request.data['phone_number']).exists():
                return Response({
                    'error': f"An account already exists with {request.data['phone_number']} phone_number. Please login."
                }, status=HTTP_403_FORBIDDEN)
            request.user.phone_number = request.data['phone_number']
        request.user.save()
        return Response(UserSerializer(request.user, many=False).data, status=HTTP_200_OK)
    elif request.method == 'DELETE':
        request.user.delete()
        return Response({'success': 'User deleted successfully'}, status=HTTP_200_OK)
