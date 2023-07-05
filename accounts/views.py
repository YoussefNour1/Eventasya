import datetime
import pyotp as pyotp
from django.contrib.auth import authenticate, get_user_model
from django.template.loader import render_to_string
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, generics
from rest_framework.views import APIView
from Eventasya.utils import send_http_email
from .models import PreviousWork, WorkImages, EventPlanner
from .permissions import IsEventPlanner
from .serializers import UserSerializer, SignupSerializer, PreviousWorksSerializer, EventPlannerSerializer
import firebase_admin
from firebase_admin import credentials, auth

# Create your views here.

User = get_user_model()


# generating otp used in confirmation and verification
class GenerateKey:
    @staticmethod
    def returnValue():
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, interval=86400)
        OTP = totp.now()
        print(f"Your OTP is {OTP} and it will expire at {totp.timecode(datetime.datetime.now()) + 86400}")
        return {"totp": secret, "OTP": OTP}


class SignUpAPIView(CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()
            key = GenerateKey.returnValue()

            user.otp = key['OTP']
            user.activation_key = key['totp']
            user.is_active = False

            # Send verification email
            email_template = render_to_string('signup_otp.html', {
                "otp": key['OTP'],
                "first_name": serializer.data['name']
            })
            email_subject = "OTP Verification"
            email_to = serializer.data['email']
            try:
                send_http_email(subject=email_subject, message=email_template, email_to=email_to)
                user.save()
                response = {
                    "message": "User created",
                    "data": serializer.data,
                }
                return Response(response, status=status.HTTP_201_CREATED)
            except Exception as e:
                user.delete()
                return Response({'msg': str(e)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def signup_verify(request: Request):
    try:
        otp = request.data['otp']
        user = User.objects.get(otp=otp, is_active=False)
        _otp = user.otp
        if otp != _otp:
            return Response({"otp": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            activation_key = user.activation_key
            totp = pyotp.TOTP(activation_key, interval=86400)
            verify = totp.verify(otp)
            if verify:
                email_template = render_to_string('verified.html', {"first_name": user.name})
                email_subject = "Account Successfully Activated"
                email_to = user.email
                send_http_email(subject=email_subject, message=email_template, email_to=email_to)
                user.is_active = True
                user.otp = None
                user.activation_key = None
                user.save()
                token, _ = Token.objects.get_or_create(user=user)

                return Response(
                    {"message": "Your account has been successfully activated!",
                     "token": token.key},
                    status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message": "Given OTP has expired!"}, status=status.HTTP_408_REQUEST_TIMEOUT)
    except User.DoesNotExist:
        return Response({"message": "The OTP doesn't exist."}, status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        user = authenticate(
            email=request.data['email'],
            password=request.data['password'])
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_202_ACCEPTED)
        return Response(data={"message": "invalid email or password"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request: Request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)


class UserDetailsAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email field is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with provided email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        key = GenerateKey.returnValue()
        otp = key['OTP']
        user.otp = otp
        user.activation_key = key['totp']
        user.save()

        email_template = render_to_string('forgot_password_otp.html', {"otp": otp, "first_name": user.name})
        send_http_email(subject="Forgot Password OTP", message=email_template, email_to=email)

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


class ForgotPasswordVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        if not email or not otp:
            return Response({"error": "Email and OTP fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            activation_key = user.activation_key
            totp = pyotp.TOTP(activation_key, interval=86400)
            print(user.email, otp)
            verify = totp.verify(otp)
            if verify:
                user.otp = None
                user.activation_key = None
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_202_ACCEPTED)
            return Response({"error": "Invalid OTP provided"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid Email provided"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        password = request.data.get('password')
        if not password:
            return Response({"error": "Password field is required"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


class PreviousWorkListCreate(generics.ListCreateAPIView):
    serializer_class = PreviousWorksSerializer

    def get_queryset(self):
        planner = self.kwargs['planner']
        return PreviousWork.objects.filter(event_planner_id=planner)


class EventPlannersList(generics.ListAPIView):
    queryset = EventPlanner.objects.all()
    serializer_class = EventPlannerSerializer
    permission_classes = [AllowAny]


class SinglePrevWork(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PreviousWorksSerializer
    queryset = PreviousWork.objects.all()


class PrevWorkCreate(generics.ListAPIView):

    serializer_class = PreviousWorksSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsEventPlanner()]
        return [AllowAny()]

    def post(self, request, *args, **kwargs):
        planner = self.request.user
        prev_work_serializer = self.serializer_class(data=self.request.data)
        if prev_work_serializer.is_valid():
            prev_work = prev_work_serializer.save(event_planner=planner)
            images = self.request.FILES.getlist('images')
            work_images = []

            for image in images:
                image = WorkImages(image=image, previous_work=prev_work)
                work_images.append(image)

            WorkImages.objects.bulk_create(work_images)

            return Response(prev_work_serializer.data, status=status.HTTP_201_CREATED)
        return Response(prev_work_serializer.errors)
