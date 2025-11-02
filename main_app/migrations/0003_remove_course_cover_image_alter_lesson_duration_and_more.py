import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_course_category_course_cover_image_alter_course_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='cover_image',
        ),
        migrations.AlterField(
            model_name='lesson',
            name='duration',
            field=models.IntegerField(help_text='Duration in minutes'),
        ),
        migrations.CreateModel(
            name='CoverCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=250)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.course')),
            ],
        ),
    ]
