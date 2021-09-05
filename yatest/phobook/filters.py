import django_filters as filters

from .models import Organization, Employee


class OrganizationFilter(filters.FilterSet):
    name = filters.AllValuesMultipleFilter(field_name='name')
 #   second_name = filters.CharFilter(
 #       field_name='organizations_of_employees__second_name',
  #      lookup_expr='icontains',
  #      label = 'Фамилия сотрудника',
  #  )
   # full_name = filters.CharFilter(
   #     field_name='organizations_of_employees__second_name',
   #     lookup_expr='icontains',
   #     label = 'ФИО сотрудника',
   #     method='full_name_method'
   # )
  #  first_name = filters.CharFilter(
 #       field_name='organizations_of_employees__first_name',
 #       lookup_expr='icontains',
 #       label = 'Имя сотрудника',
 #   )
  #  patronymic = filters.CharFilter(
 #       field_name='organizations_of_employees__patronymic',
  #      lookup_expr='icontains',
  #      label = 'Отчетство сотрудника',
  #  )
    #type = filters.AllValuesMultipleFilter(
   #     field_name='organizations_of_employees__employee__type__type',
   #     label = 'Тип телефонного номера сотрудника'
   # )
   # filters.CharFilter(
   #     field_name='organizations_of_employees__employee__type',
   #     lookup_expr='icontains',
   #     label = 'Тип телефонного номера сотрудника'
    #)
  #  phone_number = filters.CharFilter(
   #     field_name='organizations_of_employees__employee__phone_number',
   #     lookup_expr='icontains',
   #     label = 'Телефонный номер сотрудника'
  #  )

    class Meta:
        model = Organization
        fields = (
            'name',
          #  'second_name',
           # 'first_name',
           # 'patronymic',
            #'full_name',
           # 'phone_number'
        )


  #  is_favorited = filters.BooleanFilter(
  #      method='get_is_favorited'
  #  )
   # is_in_shopping_cart = filters.BooleanFilter(
  #      method='get_is_in_shopping_cart'
  #  )
  #  search_fields = [
   #     'name',
    #    'organizations_of_employees__second_name',
     #   'organizations_of_employees__first_name',
     #   'organizations_of_employees__patronymic',
     #   'organizations_of_employees__employee__phone_number'
   # ]
#'author', 'is_favorited', 'is_in_shopping_cart')

 #   def get_is_favorited(self, queryset, name, value):
 #       user = self.request.user
 #       if value:
  #          return Organization.objects.filter(favorites__user=user)
  #      return Organization.objects.all()

  #  def get_is_in_shopping_cart(self, queryset, name, value):
  #      user = self.request.user
 #       if value:
  #          return Organization.objects.filter(purchases__user=user)
  #      return Organization.objects.all()

class EmployeeFilter(filters.FilterSet):
    second_name = filters.CharFilter(
        field_name='second_name',
        lookup_expr='icontains',
        label = 'Фамилия сотрудника',
    )
    first_name = filters.CharFilter(
        field_name='first_name',
        lookup_expr='icontains',
        label = 'Имя сотрудника',
    )
    patronymic = filters.CharFilter(
        field_name='patronymic',
        lookup_expr='icontains',
        label = 'Отчетство сотрудника',
    )
    phone_number = filters.CharFilter(
        field_name='employee__phone_number',
        lookup_expr='icontains',
        label = 'Телефонный номер сотрудника'
    )
    class Meta:
        model = Employee
        fields = (
            'second_name',
            'first_name',
            'patronymic',
            'phone_number'
        )
