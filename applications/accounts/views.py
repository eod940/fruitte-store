from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from applications.accounts.serializers import JwtRegisterSerializer


class JwtRegisterAPIView(APIView):

    serializer_class = JwtRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = JwtRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = TokenObtainPairSerializer.get_token(user)  # jwt token 접근
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    "user": serializer.data,
                    "message": "회원가입 성공",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            response.set_cookie("access", access_token, httponly=True)
            response.set_cookie("refresh", refresh_token, httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
