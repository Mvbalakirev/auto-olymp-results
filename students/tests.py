from django.test import TestCase

from .models import *

class StudentModelTests(TestCase):

    def test_no_last_or_first_name(self):
        flag = False
        try:
            student = Student(last_name=None, first_name='Иван')
            student.save()
            student = Student(last_name='Иванов', first_name=None)
            student.save()
            flag = True
        except:
            pass
        self.assertIs(flag, False)