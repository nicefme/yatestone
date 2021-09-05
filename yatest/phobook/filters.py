import django_filters as filters

from .models import Organization, Employee


class OrganizationFilter(filters.FilterSet):
    name = filters.AllValuesMultipleFilter(field_name='name')

    class Meta:
        model = Organization
        fields = ('name',)


class EmployeeFilter(filters.FilterSet):
    second_name = filters.CharFilter(
        field_name='second_name',
        lookup_expr='icontains',
        label='Фамилия сотрудника',
    )
    first_name = filters.CharFilter(
        field_name='first_name',
        lookup_expr='icontains',
        label='Имя сотрудника',
    )
    patronymic = filters.CharFilter(
        field_name='patronymic',
        lookup_expr='icontains',
        label='Отчетство сотрудника',
    )
    phone_number = filters.CharFilter(
        field_name='employee__phone_number',
        lookup_expr='icontains',
        label='Телефонный номер сотрудника'
    )

    class Meta:
        model = Employee
        fields = (
            'second_name',
            'first_name',
            'patronymic',
            'phone_number'
        )
