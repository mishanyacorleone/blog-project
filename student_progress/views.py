import os
import uuid
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404, JsonResponse, HttpRequest, HttpResponse
import xml.etree.ElementTree as ET
from .forms import GradeForm, UploadXMLForm
from .models import StudentGrade
import json

DATA_DIR = os.path.join(settings.MEDIA_ROOT, 'uploads')
os.makedirs(DATA_DIR, exist_ok=True)

STATIC_XML_FILE = os.path.join(DATA_DIR, 'students.xml')


def view_xml_files(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        files = os.listdir(DATA_DIR)
        return render(request, 'views_students_xml.html', {'files': files})


def handle_uploaded_file(file):
    name = file.name
    is_xml = True

    if os.path.splitext(name)[1] != '.xml':
        is_xml = False
        return is_xml

    file_path = os.path.join(DATA_DIR, name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return is_xml


def save_to_file(file_path: str, data: dict):
    student_name = data['student_name']
    subject = data['subject']
    grade = str(data['grade'])

    if not os.path.exists(file_path):
        root = ET.Element('students')
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)

    tree = ET.parse(file_path)
    root = tree.getroot()

    student_elem = ET.SubElement(root, 'student')
    ET.SubElement(student_elem, 'name').text = student_name
    ET.SubElement(student_elem, 'subject').text = subject
    ET.SubElement(student_elem, 'grade').text = grade

    tree.write(STATIC_XML_FILE, encoding='utf-8', xml_declaration=True)


def save_to_db(data: dict):

    exists = StudentGrade.objects.filter(
        student_name=data["student_name"],
        subject=data["subject"],
        grade=data["grade"]
    ).exists()
    print(exists)
    if not exists:
        StudentGrade.objects.create(
            student_name=data["student_name"],
            subject=data["subject"],
            grade=data["grade"]
        )
        message = "Запись успешно создана"

    else:
        message = "Обнаружен дубликат. Запись не создана"
    print(message)
    return message


def add_xml_file(request: HttpRequest):
    message = None
    grade_form = GradeForm()
    upload_form = UploadXMLForm()

    if request.method == 'POST':
        if 'file' in request.FILES:
            upload_form = UploadXMLForm(request.POST, request.FILES)
            print(upload_form.is_valid())
            if upload_form.is_valid():
                is_xml = handle_uploaded_file(upload_form.cleaned_data['file'])
                if is_xml:
                    return redirect('student_progress:views')
                else:
                    upload_form = UploadXMLForm()
                    message = 'Неверное расширение файла. Загрузите файл в формате .xml'

        else:
            grade_form = GradeForm(request.POST)
            if grade_form.is_valid():
                data = grade_form.cleaned_data

                if data['save_place'] == 'file':
                    save_to_file(STATIC_XML_FILE, data)
                else:
                    message = save_to_db(data)
                    if message == "Обнаружен дубликат. Запись не создана":
                        print(111111)
                        messages.warning(request, message)

                message = 'Запись успешно добавлена'
                grade_form = GradeForm()

            else:
                message = "Исправьте ошибки в форме"

    return render(request, 'add_xml_file.html', {
        'upload_form': upload_form,
        'grade_form': grade_form,
        'message': message,
    })


def view_db(request):
    students = StudentGrade.objects.all()
    print(StudentGrade.objects.all())
    print(type(StudentGrade.objects.all()[0]))
    for i in StudentGrade.objects.all():
        print(i)
        print(type(i))

    return render(request, 'view_db.html', {'students': students})


def view_single_xml(request, filename):
    file_path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(file_path):
        raise Http404('Файл не найден!')

    tree = ET.parse(file_path)
    root = tree.getroot()

    data = []
    headers = []

    for elem in root.findall('.//student'):
        for child in elem:
            if child.tag not in headers:
                headers.append(child.tag)

    headers = list(headers)

    for elem in root.findall('.//student'):
        row = {}
        for header in headers:
            child = elem.find(header)
            row[header] = child.text if (child is not None and child.text) else '--'
        data.append(row)

    context = {
        'selected_file': filename,
        'headers': headers,
        'data': data
    }

    return render(request, 'student_progress_index.html', context)


def save_xml(request, filename):
    if request.method == 'POST':
        file_path = os.path.join(DATA_DIR, filename)
        try:
            rows = json.loads(request.body.decode('utf-8'))

            tree = ET.parse(file_path)
            root = tree.getroot()
            student_tag = root[0].tag if len(root) > 0 else 'student'

            new_root = ET.Element(root.tag)
            for row in rows:
                student_elem = ET.SubElement(new_root, student_tag)
                for key, value in row.items():
                    child = ET.SubElement(student_elem, key)
                    child.text = value if value else "--"

            tree = ET.ElementTree(new_root)
            tree.write(file_path, encoding='utf-8', xml_declaration=True)

            return JsonResponse({'message': 'Изменения успешно сохранены'})

        except Exception as ex:
            return JsonResponse({'message': f'Ошибка: {str(ex)}'}, status=500)


def index(request):
    return render(request, 'student_progress_index.html')