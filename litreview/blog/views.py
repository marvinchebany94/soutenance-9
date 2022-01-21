from django.shortcuts import render

# Create your views here.


def connexion(request):
    return render(request, 'templates/blog/index.html')


def page_inscription(request):
    return render(request, 'templates/blog/inscription.html')


def page_flux(request):
    return render(request, 'templates/blog/flux.html')


def page_onglet_abonnement(request):
    return render(request, 'templates/blog/onglet_abonnement.html')


def page_creation_critique(request):
    return render(request, 'templates/blog/creation_critique_pas_reponse_a_un_ticket.html')


def page_creation_critique_reponse_a_un_ticket(request):
    return render(request, 'templates/blog/creation_critique_reponse_a_un_ticket.html')


def page_posts(request):
    return render(request, 'templates/blog/posts.html')


def page_creation_ticket(request):
    return render(request, 'templates/blog/creation_ticket.html')

