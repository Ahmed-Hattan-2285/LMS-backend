from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = [
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        help_text='User role: instructor or student'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_instructor(self):
        return self.role == 'instructor'
    
    def is_student(self):
        return self.role == 'student'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Course(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  category = models.CharField(max_length=200)
  instructor = models.ForeignKey(
      settings.AUTH_USER_MODEL, 
      on_delete=models.CASCADE, 
      related_name='courses_taught',
      limit_choices_to={'role': 'instructor'},
      help_text='Instructor who created this course'
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def average_rating(self):
    from django.db.models import Avg
    reviews = self.reviews.all()
    if reviews.exists():
      return round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0, 2)
    return None

  def rating_count(self):
    return self.reviews.count()

  def __str__(self):
    return self.title

class CoverCourse(models.Model):
    url = models.CharField(max_length=250)
    created_at = models.DateField(auto_now_add=True) 
    updated_at = models.DateField(auto_now=True)
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
  

    def __str__(self):
        return f"Cover for course_id: {self.course.id} @{self.url}"

class Lesson(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
  title = models.CharField(max_length=255)
  video_url = models.URLField(blank=True, null=True)
  duration = models.IntegerField(help_text='Duration in minutes')
  
  
  def __str__(self):
    return f"{self.title} - {self.course.title}"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        limit_choices_to={'role': 'student'},
        help_text='Student who wrote this review'
    )
    rating = models.IntegerField(choices=RATING_CHOICES, help_text='Rating from 1 to 5')
    comment = models.TextField(blank=True, null=True, help_text='Optional review comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['course', 'student']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title} ({self.rating}/5)"