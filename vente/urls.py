from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Vue de connexion de Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Vue de déconnexion de Django
    path('panier/', views.panier_view, name='panier'),
    path('produits/', views.produits, name='produits'),
    path('contact/', views.contact, name='contact'),
    path('compte/', views.compte_view, name='compte'),
    path('ajouter_au_panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('produit/<int:produit_id>/', views.detail, name='produit_detail'),
    path('commande/', views.commande, name='commande'),
    path('paiement/', views.paiement_view, name='paiement'),
    path('confirmation/', views.confirmation_view, name='confirmation'),
]
