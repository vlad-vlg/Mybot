import json
import os
from django.conf import settings
# from datetime import datetime
from manage_channels.models import Student, Course, Grade
# settings.configure(DJANGO_SETTINGS_MODULE='channels_manager.settings',
#                    INSTALLED_APPS=['manage_channels']
#                    )
ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
os.environ["DJANGO_SETTINGS_MODULE"] = "channels_manager.settings"
# set DJANGO_SETTINGS_MODULE=channels_manager.settings


with open('fake-data.json', 'r') as file:
    data = json.load(file)

print(data)
for item in data:
    student = Student.objects.create(
        id=item["id"],
        name=item["name"],
        age=item["age"],
        email=item["email"],
        is_enrolled=item["is_enrolled"],
        registered_at=item["registered_at"]
    )
    for course_name in item["courses"]:
        course, _ = Course.objects.get_or_create(name=course_name)
        grade_value = item["grades"].get(course_name, 0)
        Grade.objects.create(student_id=student.id, course_id=course.id, grade=grade_value)
