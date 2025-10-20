from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class StudentGrade(BaseModel):
    student_name = models.CharField(max_length=100, verbose_name="Имя студента")
    subject = models.CharField(max_length=100, verbose_name="Предмет")
    grade = models.IntegerField(verbose_name="Оценка")

    def __str__(self):
        return f"{self.student_name} {self.subject} {self.grade}"
