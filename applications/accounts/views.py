from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from applications.accounts.serializers import JwtRegisterSerializer, JwtLoginSerializer


class JwtRegisterAPIView(APIView):
    """
    회원가입을 위한 APIView입니다.
    jwt 인증을 받고 정보를 쿠키에 받아 보내줍니다.
    """

    serializer_class = JwtRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = JwtRegisterSerializere(data=request.data)

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


class JwtLoginView(APIView):

    serializer_class = JwtLoginSerializer

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )
        if user is not None:
            serializer = self.serializer_class(user)

            # if serializer.is_valid():
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    "user": serializer.data,
                    "message": "로그인 성공",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return response

            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class JwtLogoutView(APIView):
    """
    클라이언트 refreshtoken 쿠키를 삭제함으로 로그아웃처리
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response({
            "message": "로그아웃 성공"
        }, status=status.HTTP_202_ACCEPTED)

        return response
