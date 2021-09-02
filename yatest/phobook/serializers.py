from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db import transaction

from .models import Organization, Employee, PhoneNumber, PhoneType
from users.serializers import UserSerializer


User = get_user_model()


class PhoneNumberSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(
        read_only=True,
        slug_field='type'
    )
    class Meta:
        model = PhoneNumber
        fields = ('type', 'phone_number')


class EmployeeSerializer(serializers.ModelSerializer):
    phone_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'second_name',
            'first_name',
            'patronymic',
            'position',
            'phone_numbers'
        )

    def get_phone_numbers(self, obj):
        phone = obj
        qs = phone.employee.all()
        return PhoneNumberSerializer(qs, many=True).data



class AddPhoneNumberSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='type',
        queryset=PhoneType.objects.all()
    )
   # phone_number = serializers.CharField()
   # phone_number = serializers.CharField()

    class Meta:
        model = PhoneNumber
        fields = ('id', 'phone_number')


class EmployeeCreateSerializer(serializers.ModelSerializer):
    phone_numbers = AddPhoneNumberSerializer(many=True)

    class Meta:
        model = Employee
        fields = (
            'second_name',
            'first_name',
            'patronymic',
            'position',
            'phone_numbers'
        )

    def create_bulk_phone_numbers(self, employee, types_data):
        try:
            PhoneNumber.objects.bulk_create([
                PhoneNumber(
                    type=type['type'],
                    employee=employee,
                    phone_number=type['phone_number']
                ) for type in types_data
            ])
        except KeyError:
            raise serializers.ValidationError(
                'Телефонный номер не может быть пустым'
            )

    @transaction.atomic
    def create(self, validated_data):
        types_data = validated_data.pop('phone_numbers')
        author = self.context.get('request').user
        employee = Employee.objects.create(author=author, **validated_data)
        employee.save()
        self.create_bulk_phone_numbers(employee, types_data)
        return employee

    @transaction.atomic
    def update(self, instance, validated_data):
        types_data = validated_data.pop('phone_numbers')
        PhoneNumber.objects.filter(employee=instance).delete()
        self.create_bulk_phone_numbers(instance, types_data)
        instance.second_name = validated_data.pop('second_name')
        instance.first_name = validated_data.pop('first_name')
        instance.patronymic = validated_data.pop('patronymic')
        instance.position = validated_data.pop('position')
        instance.save()
        return instance


    def to_representation(self, instance):
        data = EmployeeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data


    def validate_phone_numbers(self, data):
        phone_numbers = self.initial_data.get('phone_numbers')
        if phone_numbers == []:
            raise serializers.ValidationError(
                'Укажите тип и номер телефона сотрудника'
            )
        return data


class OrganizationSerializer(serializers.ModelSerializer):
    list_of_employees = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = (
            'id',
            'address',
            'name',
            'description',
            'list_of_employees'
        )



class OrganizationCreateSerializer(serializers.ModelSerializer):
   # author = UserSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = (
         #   'author',
            'address',
            'name',
            'description',
            'list_of_employees'
        )

    #@transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
        list_of_employees_data = validated_data.pop('list_of_employees')
        organization = Organization.objects.create(author=author, **validated_data)
        organization.save()
        for employee in list_of_employees_data:
            organization.list_of_employees.add(employee.id)
        return organization




    def to_representation(self, instance):
        data = OrganizationSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data