from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from blog.models import ConnexionForm, InscriptionForm, TicketForm, User, \
    Ticket, Review, TicketModifForm, CritiqueTicketForm, AddUser, UserFollows
from itertools import chain
from operator import attrgetter

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
                try:
                    User(username=username, password=password, email=email).save()
                    print('Tout est bon')
                    return redirect('/index')
                except IntegrityError:
                    print("Le compte n'a pas été crée")
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
        form = AddUser()
        error = False
        relation_exists = False
        error_formulaire = False
        operation_done = False
        want_follow_himself = False
        if request.method == "POST":
            form = AddUser(request.POST)
            if form.is_valid():
                followed_user = form.cleaned_data['UserResearch']
                if followed_user == request.session['username']:
                    want_follow_himself = True
                else:
                    try:
                        followed_user = User.objects.get(username=followed_user)
                        username = request.session['username']
                        user = User.objects.get(username=username)
                        if UserFollows.RelationAlreadyExists(UserFollows, user.id, followed_user.id):
                            relation_exists = True
                        else:
                            try:
                                relation_creating = UserFollows(user=user, followed_user=followed_user)
                                relation_creating.save()
                                operation_done = True
                            except IntegrityError:
                                print("La relation n'a pas été créé")
                    except ObjectDoesNotExist:
                        error = True
            else:
                error_formulaire = True
        else:
            pass

    try:
        user = User.objects.get(username=request.session['username']).id
        liste_abonnements = UserFollows.objects.filter(user=user)
        abonnements = []
        for followed_user in liste_abonnements:
            print(followed_user)
            username = User.objects.get(id=followed_user.followed_user.id)
            abonnements.append(username)

    except ObjectDoesNotExist:
        abonnements = []

    try:
        user = User.objects.get(username=request.session['username']).id
        liste_abonnes = UserFollows.objects.filter(followed_user=user)
        abonnes = []
        for followers in liste_abonnes:
            username = User.objects.get(id=followers.user.id)
            abonnes.append(username)
    except ObjectDoesNotExist:
        abonnes = []

    context = {
        'form': form,
        'error': error,
        'relation_exists': relation_exists,
        'error_formulaire': error_formulaire,
        'operation_done': operation_done,
        'want_follow_himself': want_follow_himself,
        'abonnements': abonnements,
        'abonnes': abonnes
    }

    return render(request, 'templates/blog/onglet_abonnement.html', context)


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
        try:
            """
            ligne pour avoir tous les tickets/review dans l'ordre chronologie en partant
            du plus récent
            tickets = Ticket.objects.filter(user_id=user_id)
            reviews = Review.objects.filter(user_associe=user_id)
            liste_tickets_reviews = sorted(chain(tickets, reviews), key=attrgetter('time_created'), 
                                    reverse=True)
            """
            user_id = User.objects.get(username=request.session['username']).id
            tickets = Ticket.objects.filter(user_id=user_id).order_by('-time_created')
            username_demande_critique = "Vous avez publié un ticket"
            date_heure = [ticket.time_created for ticket in tickets]
            #date_heure = date_heure[3] + "h" + date_heure[4] + " ," + date_heure[2] + " " + date_heure[1] + " " +\
                #date_heure[0]
            title = [ticket.title for ticket in tickets]
            description = [ticket.description for ticket in tickets]
            image = [ticket.image for ticket in tickets]
            if not description:
                description = False
            else:
                pass
            if not image:
                image = False
            else:
                pass
            contenue = True

            if request.method == "POST":
                bouton_supprimer_activated = True
                context = {
                    'tickets': tickets,
                    'username': username_demande_critique,
                    'bouton_supprimer_activated': bouton_supprimer_activated
                }

                return render(request, 'templates/blog/vos_posts.html', context)
            else:
                bouton_supprimer_activated = False
                context = {
                    'tickets': tickets,
                    'username': username_demande_critique,
                    'bouton_supprimer_activated': bouton_supprimer_activated
                }
                return render(request, 'templates/blog/vos_posts.html', context)

        except ObjectDoesNotExist:
            print("Vous n'avez aucun contenue.")
            contenue = False

    context = {
        'contenue': contenue
    }
    return render(request, 'templates/blog/vos_posts.html', context)


def page_modification_ticket(request, id):
    if not request.session['connected']:
        return redirect('/index')
    else:
        form = TicketModifForm()
        ticket = Ticket.objects.get(id=id)
        user_id = User.objects.get(username=request.session['username']).id

        if Ticket.objects.get(id=id).user_id == user_id:
            if request.method == 'POST':
                form = TicketModifForm(request.POST)
                if form.is_valid():
                    title = form.cleaned_data['title']
                    description = form.cleaned_data['description']
                    if Ticket.unique_title_by_user(Ticket, title, user_id):
                        try:
                            if not title and not description:
                                champ_vide = True
                                context = {
                                    'form': form,
                                    'champ_vide': champ_vide
                                }
                                return render(request, 'templates/blog/modifier-ticket.html', context)
                            else:
                                if title and not description:
                                    ticket = Ticket.objects.get(id=id)
                                    ticket.title = title
                                elif title and description:
                                    ticket = Ticket.objects.get(id=id)
                                    ticket.description = description
                                    ticket.title = title
                                else:
                                    ticket = Ticket.objects.get(id=id)
                                    ticket.description = description

                            ticket.save()
                            print('Ton ticket a bien été modifié.')
                            return redirect('/vos-posts')
                        except IntegrityError:
                            print("Ton ticket n'a pas été modifie.")
                    else:
                        title_already_exists = True
                        context = {
                            'form': form,
                            'title_already_exists': title_already_exists
                        }
                        return render(request, 'templates/blog/modifier-ticket.html', context)

        else:
            return redirect('/flux')

    context = {
        'form': form,
        'ticket': ticket
        }
    return render(request, 'templates/blog/modifier-ticket.html', context)


def page_supprimer_ticket(request, ticket_id):
    if not request.session['connected']:
        return redirect('/index')
    else:
        user_id = User.objects.get(username=request.session['username']).id
        ticket_no_deleted = False
        not_your_ticket = False
        try:
            ticket = Ticket.objects.get(id=ticket_id, user_id=user_id)

            if request.method == "POST":
                print(request.POST.get("submit"))
                if request.POST.get('submit') == "oui":
                    ticket.delete()
                    return redirect('/vos-posts')
                else:
                    ticket_no_deleted = True
            else:
                pass
            context = {
                'ticket': ticket,
                'ticket_no_deleted': ticket_no_deleted,
                'not_your_ticket': not_your_ticket
            }

        except ObjectDoesNotExist:
            not_your_ticket = True
            context = {
                'not_your_ticket': not_your_ticket
            }
    return render(request, 'templates/blog/supprimer_ticket.html', context)


def page_creation_ticket_critique(request):
    """
    Mettre en place un systeme de sécurité pour empêcher les gens de modifier la valeur des notes
    :param request:
    :return:
    """
    if not request.session['connected']:
        return redirect('/index')
    else:
        form = CritiqueTicketForm()
        if request.method == 'POST':
            form = CritiqueTicketForm(request.POST)
            if form.is_valid():

                username = request.session['username']
                user_id = User.objects.get(username=username).id
                ticket_title = form.cleaned_data['title']
                if Ticket.unique_title_by_user(Ticket, ticket_title, user_id):
                    ticket_description = form.cleaned_data['description']
                    critique_title = form.cleaned_data['headline']
                    critique_note = request.POST.get('checkbox')
                    critique_commentaire = form.cleaned_data['body']
                    print(ticket_title, ticket_description, critique_title, critique_note, critique_commentaire)
                    try:
                        user = User.objects.get(username=username)
                        ticket = Ticket(title=ticket_title, description=ticket_description, user_id=user.id)
                        ticket.save()

                        ticket = Ticket.objects.get(title=ticket_title, user_id=user_id)
                        review = Review(ticket_associe=ticket, rating=critique_note, headline=critique_title,
                                        body=critique_commentaire, user_associe=user)
                        review.save()
                    except IntegrityError:
                        print("Votre ticket et critique n'ont pas été enregistré dans la base de données.")
                else:
                    print("Vous avez déjà créé un ticket du même titre.")
            else:
                print("le forrmulaire n'est pas bon")
        else:
            pass
        context = {
            'form': form
        }
    return render(request, 'templates/blog/creation_ticket_et_critique.html', context)


def page_abonnements(request):
    if not request.session['connected']:
        return redirect('/index')
    else:
        pass


def logout_view(request):
    request.session['connected'] = False
    return redirect('/index')