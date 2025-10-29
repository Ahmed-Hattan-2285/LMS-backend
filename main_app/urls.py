from django.urls import path

from .views import Home, CoursesIndex

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('courses/', CoursesIndex.as_view(), name='course_index'),
]
