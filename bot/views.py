# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TelegramUser
from .serializers import TelegramUserSerializer

class RegisterView(APIView):
#    def post(self, request):
#        serializer = TelegramUserSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_id = request.query_params.get('user_id')
        try:
            user = TelegramUser.objects.get(user_id=user_id)
            serializer = TelegramUserSerializer(user)
            return Response(serializer.data)
        except TelegramUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)



# class RegisterView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')

        # Проверяем существующего пользователя
        try:
            user = TelegramUser.objects.get(user_id=user_id)
            serializer = TelegramUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TelegramUser.DoesNotExist:
            serializer = TelegramUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)