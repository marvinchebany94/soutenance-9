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
from django.urls import path
from blog import views

urlpatterns = [
    path('index/', views.connexion),
    path('inscription/', views.page_inscription),
    path('abonnement/', views.page_onglet_abonnement),
    path('creer-une-critique/<ticket_id>/', views.page_creation_critique_reponse_a_un_ticket,
         name="creer-une-critique"),
    path('creer-un-ticket', views.page_creation_ticket),
    path('vos-posts/', views.page_vos_flux_text),
    path('modifier-ticket/<ticket_id>/', views.page_modification_ticket),
    path('supprimer-ticket/<ticket_id>/', views.page_supprimer_ticket),
    path('creer-ticket-et-critique/', views.page_creation_ticket_critique),
    path('deconnexion/', views.logout_view),
    path('flux/', views.page_flux),
    path('supprimer-review/<review_id>/', views.page_supprimer_review),
    path('modifier-review/<review_id>/', views.page_modifier_review),
    path('mot-de-passe-oublie/', views.page_reset_password, name="passwd oublie")
]