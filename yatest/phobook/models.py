from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

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
        blank=True,
        verbose_name = 'Список сотрудников',
        related_name='list_of_employees'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organizations',
        verbose_name='Создатель справочника организации')

    class Meta:
        #ordering = ['name']
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return f'{self.pk}. {self.name}'


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
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        blank=True,
        #null=True,
        related_name='organizations_of_employees',
        verbose_name='Организация'
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
        ordering = ['organization', 'id']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        constraints = [
            models.UniqueConstraint(
                fields=[            
                    'second_name', 'first_name',
                    'patronymic', 'organization'
                ],
                name='unique_employee'
            )
        ]
    def __str__(self):
        return f'{self.pk}. {self.organization} - {self.second_name} {self.first_name} {self.patronymic} ({self.position})'

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
    phone_number = PhoneNumberField()
    
    #models.CharField(
   #     max_length=14,
    #    verbose_name='Телефонный номер',
    #    default='+',
    #    help_text='Формат для междугороднего сообщения, начинающийся с "+"'
    #)

    class Meta:
        verbose_name = 'Телефонный номер'
        verbose_name_plural = 'Телефонные номера'

    def __str__(self):
        return f'{self.type}: {self.phone_number}'


class Moderator(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='creater',
        verbose_name='Создатель'
    )
    moderator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='moderator',
        verbose_name='Модератор'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='organizations',
        verbose_name='Организация'
    )

    class Meta:
        verbose_name = 'Модератор организации'
        verbose_name_plural = 'Модераторы организации'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'moderator', 'organization'],
                name='unique_moderator'
            )
        ]

    def __str__(self):
        return f'{self.pk}. {self.author} предоставил доступ {self.moderator} к организации {self.organization}'
