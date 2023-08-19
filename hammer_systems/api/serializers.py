from rest_framework import serializers

from api.models import User, InviteCode


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class TokenSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class InviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteCode
        fields = (
            'owner',
            'invite_code'
        )


class UsersSerializer(serializers.ModelSerializer):
    invite_code_list = InviteCodeSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'telephone_number',
            'invite_code',
            'invite_code_list'
        )
