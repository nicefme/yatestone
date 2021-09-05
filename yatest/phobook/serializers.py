from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .models import Organization, Employee, PhoneNumber, PhoneType, Moderator
from .functions import moderators_lists

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
            'organization',
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
          #  'organization',
            'phone_numbers'
        )
       # validators = [
       #     UniqueTogetherValidator(
       #         queryset=Employee.objects.all(),
       ##         fields=[
       #             'second_name', 'first_name',
       #             'patronymic', 'organization'
       #         ],
       #         message=('В одной организации невозможно добавить сотрудников с одинаковыми ФИО')
       #     )
       # ]
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
        author = self.context.get('request').user
        organization_id = (self.context['request'].parser_context['kwargs'].
                           get('organization_id'))
        queryset = Moderator.objects.filter(organization_id=organization_id).values_list()
        moderators_list = moderators_lists(queryset)

        aa = (not author.is_staff)
        bb = author.id not in moderators_list
        author_org = get_object_or_404(Organization, id=organization_id).author
        cc = author.id != author_org.id
        #dd = validated_data


        
        if author.id not in moderators_list and (not author.is_staff) and author.id != author_org.id:
           # return validate_moderators()
            raise serializers.ValidationError(
                'У вас нет доступа к созданию сотрудников '
                'этой организации'
                )
        types_data = validated_data.pop('phone_numbers')

        # for type in types_data:
        #     type_value = list(type.values())[0].type
        #     if list(type.values())[0].type == 'Личный':




        try:
            employee = Employee.objects.create(author=author, organization_id=organization_id, **validated_data)
            employee.save()
            self.create_bulk_phone_numbers(employee, types_data)
            return employee
        except IntegrityError:
            raise serializers.ValidationError(
                'В одной организации невозможно добавить сотрудников с одинаковыми ФИО'
            )

    @transaction.atomic
    def update(self, instance, validated_data):
        types_data = validated_data.pop('phone_numbers')
        PhoneNumber.objects.filter(employee=instance).delete()
       # if types_data is None:
      #      ss = types_data is None
       #     dd
        self.create_bulk_phone_numbers(instance, types_data)
        instance.second_name = validated_data.pop('second_name')
        instance.first_name = validated_data.pop('first_name')
        instance.patronymic = validated_data.pop('patronymic')
        instance.position = validated_data.pop('position')
        #instance.organization = validated_data.pop('organization')
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
   # list_of_employees = EmployeeSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        slug_field='email'
    )
    list_of_employees = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = (
            'id',
            'author',
            'name',
            'address',
            'description',
            'list_of_employees',
            #'eee'
        )

    def get_list_of_employees(self, obj):
        name = obj
        qs = Employee.objects.filter(organization_id=name.id)
        #ss = EmployeeSerializer(qs, many=True).data
        #dd
        return EmployeeSerializer(qs, many=True).data

class OrganizationCreateSerializer(serializers.ModelSerializer):
   # author = UserSerializer(read_only=True)
  #  list_of_employees = serializers.SerializerMethodField()
   # eee = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = (
         #   'author',
            'name',
            'address',
            'description',
#            'list_of_employees',
            #'eee'
        )

   # def get_list_of_employees(self, obj):
    #    name = obj
     #   qs = Employee.objects.filter(organization_id=name.id)
     #   ss
     #   return EmployeeSerializer(qs, many=True).data

        #phone = obj
       # dd
        #qs = phone.employee.all()
        #return EmployeeSerializer(qs, many=True).data

    #@transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
#        list_of_employees_data = validated_data.pop('list_of_employees')
        organization = Organization.objects.create(author=author, **validated_data)
        organization.save()
#        for employee in list_of_employees_data:
#            organization.list_of_employees.add(employee.id)
        return organization

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        author = instance.author
        if (author != user and (not user.is_staff)
            and (validated_data['address'] != instance.address
                 or validated_data['description'] != instance.description
                 or validated_data['name'] != instance.name)):
            raise serializers.ValidationError(
                ('У вас нет доступа к редактированию данных '
                'организации (название, адрес, описание)')
            )
        return super().update(instance, validated_data)


    def to_representation(self, instance):
        data = OrganizationSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data


#class OrganizationModeratorUpdateSerializer(OrganizationCreateSerializer):
   # def create(self, validated_data):
    #    raise serializers.ValidationError(
    #            'У вас нет доступа для создания ')

   # def update(self, instance, validated_data):
    #    a = instance.address#get_object_or_404(Organization, id=instance.id)
    #    validated_data['address']=instance.address
    #    validated_data['description']=instance.description
    #    validated_data['name']=instance.name
#
       # b = validated_data
       # organization_id = (self.context['request'].parser_context['kwargs'].
        #                   get('organization_id'))
       # ss
#        return super().update(instance, validated_data)



class ModeratorSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    moderator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )
    organization = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Moderator
        fields = ('id', 'author', 'moderator', 'organization')



class ModeratorCreateSerializer(serializers.ModelSerializer):
   # moderator = serializers.SerializerMethodField()
   # author = serializers.CharField()
    moderator = serializers.SlugRelatedField(queryset = User.objects.all(), slug_field='email')
    #organization = serializers.SlugRelatedField(read_only=True, slug_field='name')
   # organization = serializers.CharField()
    class Meta:
        model = Moderator
        fields = ('moderator', )
      #  validators = [
      #      UniqueTogetherValidator(
      #          queryset=Moderator.objects.all(),
       #         fields=['author', 'moderator', 'organization'],
       #         message=('Вы уже предоставили права модератора пользователю для этой организации.')
      #      )
      #  ]


    def create(self, validated_data):
        organization_id = (self.context['request'].parser_context['kwargs'].
                           get('organization_id'))
        try:
            author_id = Organization.objects.get(id=organization_id).author_id
        except Organization.DoesNotExist:
            raise serializers.ValidationError(
                'Организация отсутствует'
            )
        moderator_id = validated_data.get('moderator').id
        user = self.context.get('request').user
       # ss = not user.is_staff
        #tt = user.is_staff
        #ff
        if author_id != user.id and (not user.is_staff):
            raise serializers.ValidationError(
                'У вас нет прав доступа для добавления пользователя в модераторы'
            )
        if author_id == moderator_id:
            raise serializers.ValidationError(
                'Вы не можете добавить автора в список модераторов'
            )
        try:
            organization = Moderator.objects.create(author_id=user.id, organization_id=organization_id, **validated_data)
            organization.save()
            return organization
        except IntegrityError:
            raise serializers.ValidationError(
                'Модератор уже добавлен в организацию'
            )
        


    def to_representation(self, instance):
        data = ModeratorSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data



class OrganizationForModeratorOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'address',

        )

class ModeratorOrganizationSerializer(serializers.ModelSerializer):
    organization = OrganizationForModeratorOrganizationSerializer(read_only=True)#, many=True)
    class Meta:
        model = Moderator
        fields = ('organization', )