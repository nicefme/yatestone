from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrganizationViewSet, EmployeeViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employees')
router.register(r'organizations', OrganizationViewSet, basename='organizations')
#router.register(r'types', PhoneTypeViewSet, basename='types')


urlpatterns = [
 #   path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view(),
  #       name='download_shopping_cart'),
    path('v1/', include(router.urls)),
  #  path('recipes/<int:recipe_id>/shopping_cart/', ShoppingVeiwSet.as_view(),
  #       name='add_recipe_to_shopping_cart'),
  #  path('recipes/<int:recipe_id>/favorite/', FavoriteAPIView.as_view(),
  #       name='add_recipe_to_favorite'),
]
