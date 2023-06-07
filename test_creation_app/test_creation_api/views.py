import random
import string
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import IQTest, EQTest
from .serializers import IQTestSerializer, EQTestSerializer


# При GET запросе в базе создается IQ И EQ тесты со сгенерированным логинов
@api_view(['GET'])
def create_tests(request):
    login = generate_random_login()
    iq_serializer = IQTestSerializer(data={'login': login})
    eq_serializer = EQTestSerializer(data={'login': login})

    if iq_serializer.is_valid() and eq_serializer.is_valid():
        iq_serializer.save()
        eq_serializer.save()
        return Response({'login': login}, status=status.HTTP_201_CREATED)
    else:
        errors = {}
        if not iq_serializer.is_valid():
            errors['iq_errors'] = iq_serializer.errors
        if not eq_serializer.is_valid():
            errors['eq_errors'] = eq_serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# При запросе POST запросе передаем логин и результат. Сохраняет в IQ тест результат и время выполнения.
@api_view(['POST'])
def save_iq_test_result(request):
    login = request.data.get('login')
    score = request.data.get('score')

    try:
        iq_test = IQTest.objects.get(login=login)
    except IQTest.DoesNotExist:
        return Response({'error': 'Invalid login'}, status=status.HTTP_400_BAD_REQUEST)

    iq_test.score = score
    iq_test.completed_at = datetime.now().strftime('%Y-%m-%d %H:%M')
    iq_test.save()

    return Response({'message': 'IQ test result saved successfully'}, status=status.HTTP_200_OK)


# При запросе POST запросе передаем логин и ответы. Сохраняет в EQ тест ответы и время выполнения.
@api_view(['POST'])
def save_eq_test_result(request):
    login = request.data.get('login')
    letters = request.data.get('letters')

    try:
        eq_test = EQTest.objects.get(login=login)
    except IQTest.DoesNotExist:
        return Response({'error': 'Invalid login'}, status=status.HTTP_400_BAD_REQUEST)

    eq_test.letters = letters
    eq_test.completed_at = datetime.now().strftime('%Y-%m-%d %H:%M')
    eq_test.save()

    return Response({'message': 'IQ test result saved successfully'}, status=status.HTTP_200_OK)


# При запросе GET запросе передаем логин в строке запроса. Получаем результаты из базы.
@api_view(['GET'])
def view_test_results(request, login):
    data = {}

    iq_test = IQTest.objects.filter(login=login).first()
    if iq_test:
        iq_serializer = IQTestSerializer(iq_test)
        data['iq_test'] = iq_serializer.data

    eq_test = EQTest.objects.filter(login=login).first()
    if eq_test:
        eq_serializer = EQTestSerializer(eq_test)
        data['eq_test'] = eq_serializer.data

    if data:
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid login or no tests found'}, status=status.HTTP_404_NOT_FOUND)


# Генерим случайный логин
def generate_random_login(length=10):
    letters = string.ascii_letters
    login = ''.join(random.choice(letters) for _ in range(length))
    return login
