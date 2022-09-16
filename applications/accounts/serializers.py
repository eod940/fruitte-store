from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class JwtRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        required=True,
        write_only=True,
        help_text='비밀번호 제약조건 없음',
        style={'input_type': 'password', 'placeholder': 'Password'}
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
            raise serializers.ValidationError('중복되는 아이디입니다.')
        return attrs
