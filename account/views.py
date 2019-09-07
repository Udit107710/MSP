from rest_framework.views import View
from rest_framework.response import Response
from .serializers import UserLoginSerializer
from django.contrib.auth import authenticate, login
import logging

logger = logging.getLogger(__name__)


class Login(View):
    def post(self, request):
        serializer = UserLoginSerializer(request.body)
        logger.log("Login data received")
        if serializer.is_valid:
            user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                login(request, user=user)
                return Response({'user': user.username, 'error': ''}, status=200)
            else:
                return Response({'user': '', 'error': 'Invalid credentials'}, status=401)
        else:
            return Response({'user': '', 'error': 'Invalid username/password'}, status=400)

