from rest_framework import serializers
from .models import IQTest, EQTest

# Создаем сериалайзеры
class IQTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = IQTest
        fields = '__all__'


class EQTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EQTest
        fields = '__all__'
