from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('about/', views.about, name='about'),
    path('creatures/', views.creatures_index, name='creatures_index'),
    path('creatures/<int:creature_id>/', views.creature_detail, name='creature_detail'),
    path('creatures/create/', views.CreatureCreate.as_view(), name='creature_create'),
    path('creatures/<int:pk>/update/', views.CreatureUpdate.as_view(), name='creature_update'),
    path('creatures/<int:pk>/delete/', views.CreatureDelete.as_view(), name='creature_delete'),
    path('creatures/<int:creature_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('toys/', views.ToyList.as_view(), name='toys_list'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toy_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toy_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toy_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toy_delete'),
    path('creatures/<int:creature_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    path('creatures/<int:creature_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
    path('creatures/<int:creature_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),

]