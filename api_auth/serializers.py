from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    # @classmethod
    # def get_token(cls, user: AuthUser) -> Token:
    #     token = super().get_token(user)
    #
    #     token['username'] = user.username
    #     token['is_staff'] = user.is_staff
    #     token['is_superuser'] = user.is_superuser
    #     token['permissions'] = list(user.get_all_permissions())
    #
    #     return token

    def validate(self, attrs):
        data = super().validate(attrs)

        token = super().get_token(self.user)

        access_token = token.access_token

        access_token['username'] = self.user.username
        access_token['is_staff'] = self.user.is_staff
        access_token['is_superuser'] = self.user.is_superuser
        access_token['permissions'] = list(self.user.get_all_permissions())

        data['access'] = str(access_token)

        return data