from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrganizationViewSet, EmployeeViewSet, ModeratorViewSet, ModeratorAPIView


router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organizations')
#router.register(r'moderatorpages', ModeratorViewSet, basename='moderatorpages')


router_two = DefaultRouter()
router_two.register(r'moderators', ModeratorViewSet, basename='moderators')
router_two.register(r'employees', EmployeeViewSet, basename='employees')

urlpatterns = [
 #   path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view(),
  #       name='download_shopping_cart'),
    path('v1/', include(router.urls)),
  #  path('v1/organizations/<int:organization_id>/moderators/', ModeratorAPIView.as_view(),
  #       name='moderators'),
    path('v1/organizations/<int:organization_id>/', include(router_two.urls)),
    path('v1/moderatorpages/', ModeratorAPIView.as_view())
  #  path('recipes/<int:recipe_id>/favorite/', FavoriteAPIView.as_view(),
  #       name='add_recipe_to_favorite'),
]
