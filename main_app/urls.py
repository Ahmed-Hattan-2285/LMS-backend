from django.urls import path

from .views import Home, CoursesIndex, CourseDetail, LessonsIndex, CoverCourseDetail, CreateUserView, LoginView, VerifyUserView, ReviewsIndex, ReviewDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/verify/', VerifyUserView.as_view(), name='verify'),
  path('courses/', CoursesIndex.as_view(), name='course_index'),
  path('lessons/', LessonsIndex.as_view(), name='lesson_index'),
  path('courses/<int:id>/', CourseDetail.as_view(), name='course_detail'),
  path('courses/<int:id>/cover/', CoverCourseDetail.as_view(), name='cover_course_detail'),
  path('reviews/', ReviewsIndex.as_view(), name='reviews_index'),
  path('reviews/<int:id>/', ReviewDetail.as_view(), name='review_detail'),
]
