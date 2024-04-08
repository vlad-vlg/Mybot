from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(max_length=100)
    is_enrolled = models.BooleanField(default=False)
    registered_at = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'students'


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'courses'


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.IntegerField()

    class Meta:
        db_table = 'grades'
