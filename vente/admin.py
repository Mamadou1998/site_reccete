from django.contrib import admin
from .models import Categorie, Produit

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'date')  # Colonnes visibles dans la liste
    search_fields = ('nom',)  # Barre de recherche par nom

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'categorie', 'prix', 'date')  # Colonnes visibles
    search_fields = ('nom', 'categorie__nom')  # Barre de recherche
    list_per_page = 10  # Nombre de lignes par page (plus compact)
