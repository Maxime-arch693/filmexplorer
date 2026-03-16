from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Film2
from .forms import ReviewForm, SignUpForm

# 1. Page d'accueil (Règle l'erreur 404)
def home(request):
    return render(request, 'home.html')

# 2. Le Catalogue AVEC la barre de recherche intégrée
def film_list(request):
    query = request.GET.get('q')
    if query:
        films = Film2.objects.filter(title__icontains=query) 
    else:
        films = Film2.objects.all()
    
    return render(request, 'film_list.html', {"films": films, "query": query})

# 3. La page d'un film (Détails + Bouton Vu + Avis)
@login_required
def film_detail(request, slug):
    film = get_object_or_404(Film2, slug=slug)
    reviews = film.reviews.all()
    
    # On vérifie si l'utilisateur a vu le film pour afficher le bon bouton
    has_viewed = request.user in film.viewed_by.all()

    if request.method == 'POST':
        if 'toggle_viewed' in request.POST:
            if has_viewed:
                film.viewed_by.remove(request.user)
            else:
                film.viewed_by.add(request.user)
            return redirect('film_detail', slug=slug)
        
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.film = film
            review.user = request.user
            review.save()
            return redirect('film_detail', slug=slug)
    else:
        review_form = ReviewForm()

    return render(request, "film_detail.html", {
        "film": film, "reviews": reviews, "review_form": review_form, "has_viewed": has_viewed
    })

# 4. Inscription
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# 5. Espace Personnel
def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile_logged_in.html')
    else:
        return render(request, 'profile_anonymous.html')
