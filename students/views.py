from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse

from .models import Student


def index(request):
    students_list = Student.objects.filter(group__alumnus=False).order_by('group__num', 'group__liter', 'last_name', 'first_name', 'middle_name')[:5]
    context = {'students': students_list}
    return render(request, 'students/index.html', context)

def detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'students/detail.html', {'student': student})

def edit(request, student_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % student_id)

def add(request):
    return HttpResponse("All good!")

def add_file(request):
    return render(request, 'students/add_file.html')

def aff_file_submit(request):
    return render(request, 'students/add_file_submit.html')
