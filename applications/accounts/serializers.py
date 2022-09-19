from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class JwtRegisterSerializer(serializers.ModelSerializer):
    """
    jwt 활용 회원가입을 위한 Serializer 입니다.
    request 받은 username과 password를 validate()에서 검증한 후 return
    """

    password = serializers.CharField(
        required=True,
        write_only=True,
        help_text='비밀번호 제약조건 없음',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    email = serializers.EmailField(
        help_text='필수 입력 항목'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email'
        ]

    def save(self, **kwargs):
        user = super().save()
        user.username = self.validated_data['username']
        user.email = self.validated_data['email']
        user.password = self.validated_data['password']
        user.set_password(self.validated_data['password'])
        user.save()

        return user

    def validate(self, attrs):
        username = attrs.get('username', None)

        # AbstractUser 사용으로 username_validator 가 먼저 적용이 된다.
        # 추후에 User 모델을 Customizing 하는 등 확장을 염두해 두었다.
        if User.objects.filter(username=username).exists():
            raise AuthenticationFailed('중복되는 아이디입니다.')
        return attrs


class JwtLoginSerializer(serializers.ModelSerializer):
    """
    jwt 활용 로그인을 위한 Serializer 입니다.
    request 받은 username과 password를 validate()에서 검증한 후 return
    """

    password = serializers.CharField(
        required=True,
        write_only=True,
        help_text='비밀번호 제약조건 없음',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)

        # 1. 아이디가 존재한다면
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username)

            # 1.1. 비밀번호가 다르다면 Error를 올린다.
            if not user.check_password(password):
                raise AuthenticationFailed('아이디 혹은 비밀번호를 확인해주세요')

        # 2. 아이디가 없다면
        else:
            raise AuthenticationFailed('아이디 혹은 비밀번호를 확인해주세요')

        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
            'user': user,
            'refresh': refresh,
            'access': access,
        }

        return attrs
