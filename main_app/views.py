from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer

class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the learning management system api home route!'}
    return Response(content)
  
class CoursesIndex(APIView):
  
  serializer_class = CourseSerializer

  def get(self, request):
    try:
      queryset = Course.objects.all()
      serializer = self.serializer_class(queryset, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseDetail(APIView):
  serializer_class = CourseSerializer

  def get(self, request, id):
    try:
      course = Course.objects.get(id=id)
      serializer = self.serializer_class(course)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)