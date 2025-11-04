from django.test import TestCase
from main_app.models import User, Course, Lesson, CoverCourse, Review

class ModelsTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            username='instructor1',
            password='testpass123',
            email='instructor@test.com',
            role='instructor'
        )
        
        self.student1 = User.objects.create_user(
            username='student1',
            password='testpass123',
            email='student1@test.com',
            role='student'
        )
        
        self.student2 = User.objects.create_user(
            username='student2',
            password='testpass123',
            email='student2@test.com',
            role='student'
        )
        
        self.course1 = Course.objects.create(
            title='Python Basics',
            description='Introduction to Python programming',
            category='Programming',
            instructor=self.instructor
        )
        
        self.course2 = Course.objects.create(
            title='Web Development',
            description='Learn web development',
            category='Web Development',
            instructor=self.instructor
        )
        
        self.lesson1 = Lesson.objects.create(
            course=self.course1,
            title='Variables and Data Types',
            video_url='https://example.com/video1',
            duration=30
        )
        
        self.lesson2 = Lesson.objects.create(
            course=self.course1,
            title='Control Flow',
            video_url='https://example.com/video2',
            duration=45
        )
        
        self.lesson3 = Lesson.objects.create(
            course=self.course2,
            title='HTML Basics',
            duration=25
        )
        
        self.cover1 = CoverCourse.objects.create(
            course=self.course1,
            url='https://example.com/cover1.jpg'
        )
        
        self.review1 = Review.objects.create(
            course=self.course1,
            student=self.student1,
            rating=5,
            comment='Great course!'
        )
        
        self.review2 = Review.objects.create(
            course=self.course1,
            student=self.student2,
            rating=4,
            comment='Awesome course!'
        )
        
        self.review3 = Review.objects.create(
            course=self.course2,
            student=self.student1,
            rating=5
        )

    def test_user_create(self):
        self.assertEqual(str(self.instructor), 'instructor1 (Instructor)')
        self.assertEqual(str(self.student1), 'student1 (Student)')

    def test_user_role_methods(self):
        self.assertTrue(self.instructor.is_instructor())
        self.assertFalse(self.instructor.is_student())
        self.assertTrue(self.student1.is_student())
        self.assertFalse(self.student1.is_instructor())

    def test_course_create(self):
        self.assertEqual(str(self.course1), 'Python Basics')
        self.assertEqual(str(self.course2), 'Web Development')

    def test_lesson_create(self):
        self.assertEqual(str(self.lesson1), 'Variables and Data Types - Python Basics')
        self.assertEqual(str(self.lesson2), 'Control Flow - Python Basics')
        self.assertEqual(str(self.lesson3), 'HTML Basics - Web Development')

    def test_cover_course_create(self):
        self.assertEqual(str(self.cover1), f'Cover for course_id: {self.course1.id} @https://example.com/cover1.jpg')

    def test_review_create(self):
        self.assertEqual(str(self.review1), 'student1 - Python Basics (5/5)')
        self.assertEqual(str(self.review2), 'student2 - Python Basics (4/5)')
        self.assertEqual(str(self.review3), 'student1 - Web Development (5/5)')

    def test_course_instructor_relationship(self):
        self.assertEqual(self.course1.instructor, self.instructor)
        self.assertEqual(self.course2.instructor, self.instructor)
        self.assertEqual(self.instructor.courses_taught.count(), 2)

    def test_lesson_course_relationship(self):
        self.assertEqual(self.lesson1.course, self.course1)
        self.assertEqual(self.lesson2.course, self.course1)
        self.assertEqual(self.lesson3.course, self.course2)
        self.assertEqual(self.course1.lessons.count(), 2)
        self.assertEqual(self.course2.lessons.count(), 1)

    def test_cover_course_relationship(self):
        self.assertEqual(self.cover1.course, self.course1)

    def test_review_course_relationship(self):
        self.assertEqual(self.review1.course, self.course1)
        self.assertEqual(self.review2.course, self.course1)
        self.assertEqual(self.review3.course, self.course2)
        self.assertEqual(self.course1.reviews.count(), 2)
        self.assertEqual(self.course2.reviews.count(), 1)

    def test_review_student_relationship(self):
        self.assertEqual(self.review1.student, self.student1)
        self.assertEqual(self.review2.student, self.student2)
        self.assertEqual(self.student1.reviews.count(), 2)
        self.assertEqual(self.student2.reviews.count(), 1)

    def test_course_average_rating(self):
        avg_rating = self.course1.average_rating()
        self.assertEqual(avg_rating, 4.5)

    def test_course_rating_count(self):
        self.assertEqual(self.course1.rating_count(), 2)
        self.assertEqual(self.course2.rating_count(), 1)

    def test_course_no_reviews(self):
        new_course = Course.objects.create(
            title='New Course',
            description='Description',
            category='Category',
            instructor=self.instructor
        )
        self.assertIsNone(new_course.average_rating())
        self.assertEqual(new_course.rating_count(), 0)

    def test_review_ordering(self):
        reviews = list(self.course1.reviews.all())
        self.assertEqual(reviews[0], self.review2)
        self.assertEqual(reviews[1], self.review1)

    def test_review_unique_together(self):
        with self.assertRaises(Exception):
            Review.objects.create(
                course=self.course1,
                student=self.student1,
                rating=3
            )

    def test_deleting_instructor_cascades_to_courses(self):
        self.instructor.delete()
        self.assertEqual(Course.objects.count(), 0)

    def test_deleting_course_cascades_to_lessons(self):
        self.course1.delete()
        self.assertEqual(Lesson.objects.count(), 1)

    def test_deleting_course_cascades_to_cover(self):
        self.course1.delete()
        self.assertEqual(CoverCourse.objects.count(), 0)

    def test_deleting_course_cascades_to_reviews(self):
        self.course1.delete()
        self.assertEqual(Review.objects.count(), 1)

    def test_deleting_student_cascades_to_reviews(self):
        self.student1.delete()
        self.assertEqual(Review.objects.count(), 1)
