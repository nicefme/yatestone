from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Organization(models.Model):
    address = models.CharField(
        max_length=300,
        blank=False,
        verbose_name='Адрес'
    )
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False,
        verbose_name='Название организации'
    )
    description = models.CharField(
        max_length=1000,
        verbose_name='Описание'
    )
    list_of_employees = models.ManyToManyField(
        'Employee',
        verbose_name = 'Список сотрудников',
        related_name='list_of_employees'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organizations',
        verbose_name='Создатель справочника организации')

    class Meta:
        ordering = ['name']
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Имя'
    )
    second_name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Фамилия'
    )
    patronymic = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Отчетсво'
    )
    position = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Должность'
    )
    phone_numbers = models.ManyToManyField(
        'PhoneType',
        through='PhoneNumber',
        blank=True,
        verbose_name = 'Телефонные номера',
        related_name='phone_of_employee'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='employee',
        verbose_name='Создатель сотрудника')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.second_name} {self.first_name} {self.patronymic} ({self.position})'

class PhoneType(models.Model):
    type = models.CharField(
        max_length=100,
        verbose_name='Тип телефонного номера'
    )

    class Meta:
        verbose_name = 'Тип телефонного номера'
        verbose_name_plural = 'Типы телефонных номеров'

    def __str__(self):
        return self.type


class PhoneNumber(models.Model):
    type = models.ForeignKey(
        PhoneType,
        on_delete=models.CASCADE,
        verbose_name='Тип телефонного номера',
        related_name='type_of_phone'
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Сотрудник',
        related_name='employee'
    )
    phone_number = models.CharField(
        max_length=14,
        verbose_name='Телефонный номер',
        default='+',
        help_text='Формат для междугороднего сообщения, начинающийся с "+"'
    )

    class Meta:
        verbose_name = 'Телефонный номер'
        verbose_name_plural = 'Телефонные номера'

    def __str__(self):
        return f'{self.type}: {self.phone_number}'