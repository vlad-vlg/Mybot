from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField(max_length=100)
    is_enrolled = models.BooleanField(default=False)
    course1_id = models.IntegerField()
    grade1_id = models.IntegerField()
    course2_id = models.IntegerField()
    grade2_id = models.IntegerField()
    course3_id = models.IntegerField()
    grade3_id = models.IntegerField()
    registered_at = models.DateTimeField()

    class Meta:
        db_table = 'users'


class Course(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'courses'


class Grade(models.Model):
    grade = models.IntegerField()

    class Meta:
        db_table = 'grades'
