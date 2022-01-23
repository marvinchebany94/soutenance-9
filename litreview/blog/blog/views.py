from django.db import IntegrityError
from django.shortcuts import render, redirect
from blog.models import ConnexionForm, InscriptionForm, TicketForm, User, \
    Ticket, Review
from django.contrib.auth import logout
# Create your views here.


def connexion(request):
    form = ConnexionForm()
    error = False
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.connexion_autorized(User, username, password):
                print("Compte valide.")
                request.session['connected'] = True
                request.session['username'] = username
                return redirect('/flux')

            else:
                print("Compte inexistant.")
                error = True

    elif request.session['connected']:
        return redirect('/flux')

    else:
        request.session['connected'] = False
        pass
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'templates/blog/index.html', context)


def page_inscription(request):
    form = InscriptionForm()
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']

            unique_username = User.unique_username(User, username)
            unique_email = User.unique_email(User, email)
            same_passwords = User.same_passwords(User, password, password2)
            if not unique_username:
                print("Le peseudo est déjà pris.")
            elif not unique_email:
                print("L'email est déjà pris.")
            elif not same_passwords:
                print("Les mots de passe ne correspondent pas.")
            else:
                print('Tout est bon')

        else:
            pass
    elif request.session['connected']:
        return redirect('/flux')
    else:
        pass
    context = {
        'form': form
    }

    return render(request, 'templates/blog/inscription.html', context)


def page_flux(request):
    if not request.session['connected']:
        return redirect('/index')
    else:
        pass
    return render(request, 'templates/blog/flux.html')


def page_onglet_abonnement(request):
    if not request.session['connected']:
        return redirect('/index')
    else:
        pass
    return render(request, 'templates/blog/onglet_abonnement.html')


def page_creation_critique(request):
    if not request.session['connected']:
        return redirect('/index')
    else:
        pass
    return render(request, 'templates/blog/creation_critique_pas_reponse_a_un_ticket.html')


def page_creation_critique_reponse_a_un_ticket(request):
    if not request.session['connected']:
        return redirect('/index')
    else:
        pass
    return render(request, 'templates/blog/creation_critique_reponse_a_un_ticket.html')


def page_posts(request):
    if not request.session['connected']:
        return redirect('/index')
    else:
        pass
    return render(request, 'templates/blog/posts.html')


def page_creation_ticket(request):
    form = TicketForm()
    already_exists = False
    if not request.session['connected']:
        return redirect('/index')
    else:
        if request.method == 'POST':
            form = TicketForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                user_identifiant = User.objects.get(username=request.session['username']).id
                if Ticket.unique_title_by_user(Ticket, title=title, user_id=user_identifiant):
                    try:
                        new_ticket = Ticket(title=title, description=description)
                        new_ticket.user_id = user_identifiant
                        new_ticket.save()
                        print("votre ticket a bien été enregistré")
                        return redirect('/flux')
                    except IntegrityError:
                        print("Votre ticket n'a pas été enregistré.")
                else:
                    already_exists = True
                    print("Un ticket du même nom existe déjà !")

            else:
                print("le formulaire n'est pas valide")

    context = {
        'form': form,
        'already_exists':already_exists
    }

    return render(request, 'templates/blog/creation_ticket.html', context)


def page_vos_posts(request):
    if not request.session['connected']:
        return redirect('/index')
    else:
        pass
    return render(request, 'templates/blog/vos_posts.html')


def page_modification_ticket(request):
    if not request.session['connected']:
        return redirect('/index')
    else:
        pass
    return render(request, 'templates/blog/modifier-ticket.html')


def logout_view(request):
    request.session['connected'] = False
    return redirect('/index')