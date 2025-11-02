from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  category = models.CharField(max_length=200)
  instructor = models.CharField(max_length=255)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')

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