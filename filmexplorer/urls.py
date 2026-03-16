from django.contrib import admin
from django.urls import path, include
from films import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    
    # Nouvelles URLs propres et définitives
    path('', views.home, name='home'), # Règle l'erreur 404 !
    path('films/', views.film_list, name='film_list'),
    path('film/<slug:slug>/', views.film_detail, name='film_detail'),
    path('profile/', views.profile, name='profile'),
]
