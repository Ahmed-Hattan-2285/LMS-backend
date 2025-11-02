from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Course, Lesson, CoverCourse, User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'role', 'role_display', 'first_name', 'last_name', 'created_at')
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class InstructorSerializer(serializers.ModelSerializer):
    """Simplified serializer for displaying instructor information"""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


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
    instructor = InstructorSerializer(read_only=True)
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='instructor'),
        source='instructor',
        write_only=True,
        required=False
    )
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'instructor', 'instructor_id', 'lessons', 'course_cover', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']