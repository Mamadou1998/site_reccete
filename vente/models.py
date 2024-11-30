from django.contrib.auth.models import User
from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)  # Date de création de la catégorie

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)  # Date de création du produit
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    image = models.ImageField(upload_to='produits/', blank=True)

    def __str__(self):
        return self.nom  # Utilise 'nom' car c'est le champ que tu définis

# Modèle Panier
class Panier(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paniers')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Panier de {self.utilisateur.username} - {self.produit.nom} ({self.quantite})"

    def get_total(self):
        return self.produit.prix * self.quantite

# Modèle Commande
class Commande(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes')
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, default="En attente")

    def __str__(self):
        return f"Commande de {self.utilisateur.username} - {self.date_commande.strftime('%d/%m/%Y %H:%M:%S')}"
    
    def get_total(self):
        total = 0
        for panier in self.panier.all():
            total += panier.get_total()
        return total
