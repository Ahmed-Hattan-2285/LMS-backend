from django.urls import path

from .views import Home, CoursesIndex, CourseDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('courses/', CoursesIndex.as_view(), name='course_index'),
  path('courses/<int:id>/', CourseDetail.as_view(), name='course_detail'),
]
