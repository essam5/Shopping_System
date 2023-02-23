from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter()

router.register(r"orders", views.OrdersViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("order/<int:pk>/", views.OrderView.as_view()),
]
