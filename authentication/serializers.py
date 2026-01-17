from rest_framework import serializers

from authentication.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        # 1. Создание и сохранение пользователя в базе данных с использованием базового метода
        user = super().create(validated_data)

        # 2. Хеширование пароля пользователя
        user.set_password(user.password)

        # 3. Сохранение пользователя с хешированным паролем
        user.save()

        # 4. Возврат созданного пользователя
        return user
