from django.urls import path

from .views import Home, CoursesIndex, CourseDetail, LessonsIndex, CoverCourseDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('courses/', CoursesIndex.as_view(), name='course_index'),
  path('lessons/', LessonsIndex.as_view(), name='lesson_index'),
  path('courses/<int:id>/', CourseDetail.as_view(), name='course_detail'),
  path('courses/<int:id>/cover/', CoverCourseDetail.as_view(), name='cover_course_detail'),
]
