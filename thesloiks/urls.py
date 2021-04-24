from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jar/', views.jar, name='jar'),
    path('jar/<int:jar_id>', views.jar, name='jar_with_id'),
    path('transaction/', views.transaction, name='transaction'),
]
