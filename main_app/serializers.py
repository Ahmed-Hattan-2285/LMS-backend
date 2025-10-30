from rest_framework import serializers
from .models import Course, Lesson, CoverCourse

class CoverCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoverCourse
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    course_cover = CoverCourseSerializer(source='covercourse', read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'instructor', 'lessons', 'course_cover']