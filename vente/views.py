from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import CustomUserCreationForm  # Un formulaire personnalisé si nécessaire
from django.contrib import messages
from .models import Panier
from .models import Produit
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView




class CustomLoginView(LoginView):
    template_name = 'vente/custom_login.html'  # Remplace par ton template personnalisé


# Vue pour la page d'accueil
def index(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    return render(request, 'index.html', {'login_form': login_form, 'register_form': register_form})



def produits(request):
    produits = Produit.objects.all()  # Récupère tous les produits
    return render(request, 'produits.html', {'produits': produits})


# Vue pour la page de contact
def contact(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        message = request.POST.get('message')

        # Envoyer l'email
        try:
            send_mail(
                'Message de contact de ' + prenom + ' ' + nom,  # Sujet de l'email
                message,  # Corps du message
                email,  # Email de l'expéditeur
                [settings.CONTACT_EMAIL],  # Email du destinataire
                fail_silently=False,
            )
            # Ajouter un message de succès
            messages.success(request, "Votre message a été envoyé avec succès !")
        except Exception as e:
            # En cas d'erreur, afficher un message d'erreur
            messages.error(request, "Une erreur est survenue. Veuillez réessayer.")

    return render(request, 'contact.html')

# Detail du produit 
def detail(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    return render(request, 'detail.html', {'produit': produit})


def commande(request):
    # Logique pour afficher la page de commande (ajoute ton code ici)
    return render(request, 'commande.html')  # Assure-toi d'avoir une template 'commande.html'


# Accès au compte utilisateur
@login_required
def profile(request):
    return render(request, 'profile.html')


# Accès au compte 
@login_required
def compte_view(request):
    # Tu peux ajouter des informations supplémentaires de l'utilisateur ici si nécessaire
    return render(request, 'compte.html')

# Créer une vue d'inscription qui prend en compte ces champs
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Connexion automatique de l'utilisateur après l'inscription
            user = form.save()
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


# Vue pour la connexion de l'utilisateur
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {username} !')
                return redirect('index')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
        else:
            messages.error(request, 'Formulaire invalide')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Vue pour la déconnexion de l'utilisateur
def logout_user(request):
    logout(request)
    messages.info(request, 'Vous êtes déconnecté')
    return redirect('index')


def panier_view(request):
    # Récupérer le panier depuis la session
    panier = request.session.get('panier', [])

    # Vérifier si le panier est vide
    if not panier:
        return render(request, 'panier.html', {'message': "Votre panier est vide. Ajoutez des produits avant de passer à la commande."})


    # Calculer les détails du panier
    panier_details = []
    total_panier = 0
    for item in panier:
        try:
            produit = Produit.objects.get(id=item['id'])  # Assurer que l'ID correspond à celui dans le panier
            total = float(item['prix']) * item['quantite']  # Calcul du total pour chaque produit
            panier_details.append({
                'produit': produit,
                'quantite': item['quantite'],
                'total': total
            })
            total_panier += total
        except Produit.DoesNotExist:
            pass  # Ignorer les produits introuvables

    return render(request, 'panier.html', {'panier': panier_details, 'total_panier': total_panier})


# Vue pour ajouter un produit au panier
@login_required
def ajouter_au_panier(request, produit_id):
    # Ne pas vider la session à chaque ajout de produit
    produit = get_object_or_404(Produit, pk=produit_id)

    # Récupérer le panier depuis la session
    panier = request.session.get('panier', [])

    # Chercher si le produit est déjà dans le panier
    for item in panier:
        if item['id'] == produit.id:
            item['quantite'] += 1
            item['total'] = item['quantite'] * float(item['prix'])  # S'assurer que le total est bien un float
            break
    else:
        # Ajouter le produit au panier
        panier.append({
            'id': produit.id,
            'nom': produit.nom,
            'prix': str(produit.prix),  # Stocker le prix sous forme de string pour éviter les erreurs de sérialisation
            'quantite': 1,
            'total': str(produit.prix)  # Le total initial est égal au prix
        })

    # Sauvegarder le panier dans la session
    request.session['panier'] = panier

    # Rediriger vers la page du panier
    return redirect('panier')



# La vue commande
# from django.shortcuts import get_object_or_404

def commande(request):
    panier = request.session.get('panier', [])
    total_panier = 0
    details_panier = []

    for item in panier:
        produit = get_object_or_404(Produit, id=item['id'])  # Utiliser 'id' au lieu de 'produit_id'
        prix = produit.prix
        total_panier += item['quantite'] * prix
        details_panier.append({
            'produit': produit.nom,
            'quantite': item['quantite'],
            'prix': prix,
            'total': item['quantite'] * prix
        })

    # Redirection vers la page de paiement
    return redirect('paiement')  # Assure-toi que le nom de l'URL 'paiement' existe dans ton URLconf



# Vue pour le paiement 
# Vue pour le paiement
def paiement_view(request):
    # Vider la session avant de traiter le paiement (si tu veux tester sans ancien panier)
    # request.session.flush()

    panier = request.session.get('panier', [])
    
    # Calcul du total du panier
    # total_panier = sum(item['quantite'] * item['prix'] for item in panier)
    total_panier = sum(item['quantite'] * float(item['prix']) for item in panier)


    if request.method == 'POST':
        # Récupérer le mode de paiement choisi
        mode_paiement = request.POST.get('mode_paiement')
        # Enregistrer l'achat (simulé ici)
        request.session['paiement'] = {'mode': mode_paiement, 'total': total_panier}
        return redirect('confirmation')  # Rediriger vers la page de confirmation

    return render(request, 'paiement.html', {'panier': panier, 'total_panier': total_panier})



# Confirmation du paiment 
def confirmation_view(request):
    paiement = request.session.get('paiement', {})
    panier = request.session.get('panier', [])
    request.session['panier'] = []  # Vider le panier après l'achat

    return render(request, 'confirmation.html', {
        'paiement': paiement,
        'panier': panier,
    })
