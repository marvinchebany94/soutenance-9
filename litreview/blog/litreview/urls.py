"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from blog import views

urlpatterns = [
    path('connexion/', views.connexion),
    path('inscription/', views.page_inscription),
    path('flux/', views.page_flux),
    path('abonnement/', views.page_onglet_abonnement),
    path('creer-une-critique/', views.page_creation_critique),
    path('creer-une-reponse/', views.page_creation_critique_reponse_a_un_ticket),

]