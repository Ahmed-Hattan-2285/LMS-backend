from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, serializers
from .models import Course, Lesson, CoverCourse, User
from .serializers import CourseSerializer, LessonSerializer, CoverCourseSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as err:
            return Response(err.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                content = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
                return Response(content, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            try:
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
            except Exception as token_error:
                return Response({"detail": "Failed to generate token.", "error": str(token_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as err:
            return Response({"detail": "Unexpected error occurred.", "error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Home(APIView):
    def get(self, request):
        content = {
            'message': 'Welcome to the learning management system api home route!'}
        return Response(content)


class CoursesIndex(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer

    def get(self, request):
        try:
            if request.user.is_instructor():
                queryset = Course.objects.filter(instructor=request.user)
            else:
                queryset = Course.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            if not request.user.is_instructor():
                return Response(
                    {'error': 'Only instructors can create courses'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(instructor=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LessonsIndex(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonSerializer

    def get(self, request):
        try:
            queryset = Lesson.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            if not request.user.is_instructor():
                return Response(
                    {'error': 'Only instructors can create lessons'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer

    def get(self, request, id):
        try:
            course = Course.objects.get(id=id)
            serializer = self.serializer_class(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            course = Course.objects.get(id=id)
            if not request.user.is_instructor() or course.instructor != request.user:
                return Response(
                    {'error': 'Only the course instructor can edit this course'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.serializer_class(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            course = Course.objects.get(id=id)
            if not request.user.is_instructor() or course.instructor != request.user:
                return Response(
                    {'error': 'Only the course instructor can delete this course'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CoverCourseDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CoverCourseSerializer

    def get(self, request, id):
        try:
            cover_course = CoverCourse.objects.get(course_id=id)
            serializer = self.serializer_class(cover_course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id):
        try:
            course = Course.objects.get(id=id)
            payload = request.data.copy()
            payload['course'] = course.id
            try:
                cover = CoverCourse.objects.get(course=course)
                serializer = self.serializer_class(cover, data=payload)
            except CoverCourse.DoesNotExist:
                serializer = self.serializer_class(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
