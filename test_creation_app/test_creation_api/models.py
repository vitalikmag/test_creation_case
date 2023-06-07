from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


# Создаем модели для тестов
class IQTest(models.Model):
    login = models.CharField(max_length=10, unique=True)
    score = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(50)])
    completed_at = models.DateTimeField(auto_now_add=True)


class EQTest(models.Model):
    login = models.CharField(max_length=10, unique=True)
    letters = models.CharField(max_length=5, validators=[RegexValidator(r'^[абвгд]+$')], blank=True, null=True)
    completed_at = models.DateTimeField(auto_now_add=True)
