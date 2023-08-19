from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from .serializers import UserSerializer, TokenSerializer, UsersSerializer
from api.models import ActivationCode, User, InviteCode


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    """Функция создает пользователя и отправляет код на вход"""
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    user, created = User.objects.get_or_create(telephone_number=username)
    if not created:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    code = ActivationCode.objects.create(user=user)
    return Response({'Ваш код активации': str(code.code)},
                    status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
@permission_classes([AllowAny])
def check_activation_code(request):
    """Функция проверяет код и присваивает токен"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = get_object_or_404(
        ActivationCode,
        code=serializer.data.get('code')
    )
    if not code:
        return Response("код не существует")
    user = code.user
    code.delete()
    InviteCode.objects.get_or_create(owner=user)
    invite = InviteCode.objects.get(owner=user)
    invite = str(invite.invite_code)
    user = User.objects.get(telephone_number=user)
    token = default_token_generator.make_token(user)
    user.invite_code = invite
    user.save()
    return Response({'Ваш токен': str(token), 'Ваш инвайт код': str(invite)},
                    status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'telephone_number'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[AllowAny])
    def me(self, request):
        """Функция для получения и редактирования текущим пользователем своих
        данных"""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
