import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main_app', '0003_remove_course_cover_image_alter_lesson_duration_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE main_app_course DROP COLUMN IF EXISTS user_id;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AddField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RunSQL(
            sql="ALTER TABLE main_app_course DROP COLUMN IF EXISTS instructor;",
            reverse_sql="ALTER TABLE main_app_course ADD COLUMN instructor VARCHAR(255);",
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(help_text='Instructor who created this course', limit_choices_to={'role': 'instructor'}, on_delete=django.db.models.deletion.CASCADE, related_name='courses_taught', to=settings.AUTH_USER_MODEL),
        ),
    ]

