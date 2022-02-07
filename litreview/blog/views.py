from datetime import datetime
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from blog.models import ConnexionForm, InscriptionForm, TicketForm, User, \
    Ticket, Review, TicketModifForm, CritiqueTicketForm, AddUser, UserFollows, \
    CritiqueForm, CritiqueModifForm, ResetPasswordForm
from itertools import chain
from operator import attrgetter

from django.contrib.auth import logout
# Create your views here.


def connexion(request):
    try:
        if request.session['connected']:
            return redirect('/flux')
        else:
            pass
    except KeyError:
        print("probleme avec la session")
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
    else:
        request.session['connected'] = False
        pass
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'templates/blog/index.html', context)


def page_inscription(request):
    try:
        if request.session['connected']:
            return redirect('/flux')
        else:
            pass
    except KeyError:
        print("probleme avec la session")

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
                not_unique_username = True
                context = {
                    'not_unique_username': not_unique_username,
                    'form': form
                }
                return render(request, 'templates/blog/inscription.html', context)
            elif not unique_email:
                print("L'email est déjà pris.")
                not_unique_email = True
                context = {
                    'not_unique_email': not_unique_email,
                    'form': form
                }
                return render(request, 'templates/blog/inscription.html', context)
            elif not same_passwords:
                print("Les mots de passe ne correspondent pas.")
                passwd_error = True
                context = {
                    'passwd_error': passwd_error,
                    'form': form
                }
                return render(request, 'templates/blog/inscription.html', context)
            else:
                try:
                    User(username=username, password=password, email=email).save()
                    print('Tout est bon')
                    return redirect('/index')
                except IntegrityError:
                    print("Le compte n'a pas été crée")
        else:
            pass
    else:
        pass
    context = {
        'form': form
    }

    return render(request, 'templates/blog/inscription.html', context)


def page_onglet_abonnement(request):
    try:
        if not request.session['connected']:
            print(request.session['connected'])
            return redirect('/index')
        else:
            pass
    except KeyError:
        print("probleme avec la session")

    form = AddUser()
    error = False
    relation_exists = False
    error_formulaire = False
    operation_done = False
    want_follow_himself = False
    if request.method == "POST":
        if 'UserResearch' not in request.POST:
            try:
                followed_user = User.objects.get(username=request.POST.get('username'))
                username = request.session['username']
                user = User.objects.get(username=username)
                relation = UserFollows.objects.get(user=user, followed_user=followed_user)
                relation.delete()
                return redirect('/abonnement')
            except followed_user.DoesNotExist:
                return redirect('/abonnement')
            except user.DoesNotExist:
                return redirect('/abonnement')
            except relation.DoesNotExist:
                return redirect('/abonnement')
        else:
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


def page_creation_critique_reponse_a_un_ticket(request, ticket_id):
    try:
        if not request.session['connected']:
            print(request.session['connected'])
            return redirect('/index')
        else:
            pass
    except KeyError:
        print("probleme avec la session")

    error = False
    ticket_doesnt_exist = False
    user = User.objects.get(username=request.session['username'])
    user_id = user.id
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except ObjectDoesNotExist:
        print("le ticket n'existe pas")
        ticket_doesnt_exist = True
        return render(request, 'templates/blog/creation-critique.html',
                      {'ticket_doesnt_exist': ticket_doesnt_exist})
    except ValueError:
        return redirect('/vos-posts')
    try:
        review = Review.objects.get(ticket_associe=ticket, user_associe=user)
        return redirect('/flux')
    except ObjectDoesNotExist:
        print("aucun review relié au ticket")

    form = CritiqueForm()
    if request.method == "POST":
        form = CritiqueForm(request.POST)
        if form.is_valid():
            critique_title = form.cleaned_data['titre']
            critique_note = request.POST.get('checkbox')
            critique_commentaire = form.cleaned_data['commentaire']
            if not critique_note:
                error = True
            else:

                if int(critique_note) not in [0, 1, 2, 3, 4, 5]:
                    error = True
                    print('error')
                else:
                    print(critique_title, critique_note, critique_commentaire)
                    error = False
                    try:
                        review = Review(ticket_associe=ticket, rating=critique_note, headline=critique_title,
                                        body=critique_commentaire, user_associe=user)
                        review.save()
                        return redirect('/vos-posts')
                    except IntegrityError:
                        print("Votre critique n'ont pas été enregistré dans la base de données.")
        else:
            print("le formulaire est invalide.")
            error = True
    else:
        pass

    context = {
        'error': error,
        'ticket_doesnt_exist': ticket_doesnt_exist,
        'form': form,
        'ticket': ticket,
        'user_id': user_id
    }
    return render(request, 'templates/blog/creation-critique.html', context)


def page_creation_ticket(request):
    form = TicketForm()
    already_exists = False
    try:
        if not request.session['connected']:
            print(request.session['connected'])
            return redirect('/index')
        else:
            pass
    except KeyError:
        print("probleme avec la session")

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
                    return redirect('/vos-posts')
                except IntegrityError:
                    print("Votre ticket n'a pas été enregistré.")
            else:
                already_exists = True
                print("Un ticket du même nom existe déjà !")

        else:
            print("le formulaire n'est pas valide")

    context = {
        'form': form,
        'already_exists': already_exists
    }

    return render(request, 'templates/blog/creation_ticket.html', context)


def page_modification_ticket(request, ticket_id):
    try:
        if not request.session['connected']:
            print(request.session['connected'])
            return redirect('/index')
        else:
            pass
    except KeyError:
        print("probleme avec la session")

    form = TicketModifForm()
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except ValueError:
        return redirect('/vos-posts')

    user_id = User.objects.get(username=request.session['username']).id

    if Ticket.objects.get(id=ticket_id).user_id == user_id:
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
                                'champ_vide': champ_vide,
                                'ticket': ticket
                            }
                            return render(request, 'templates/blog/modifier-ticket.html', context)
                        else:
                            if title and not description:
                                ticket = Ticket.objects.get(id=ticket_id)
                                ticket.title = title
                                ticket.time_created = datetime.now()
                            elif title and description:
                                ticket = Ticket.objects.get(id=ticket_id)
                                ticket.description = description
                                ticket.title = title
                                ticket.time_created = datetime.now()
                            else:
                                ticket = Ticket.objects.get(id=ticket_id)
                                ticket.description = description
                                ticket.time_created = datetime.now()

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
    try:
        if not request.session['connected']:
            print(request.session['connected'])
            return redirect('/index')
        else:
            pass
    except KeyError:
        print("probleme avec la session")

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
    except ValueError:
        return redirect('/vos-posts')
    return render(request, 'templates/blog/supprimer_ticket.html', context)


def page_creation_ticket_critique(request):
    try:
        if not request.session['connected']:
            print(request.session['connected'])
            return redirect('/index')
        else:
            pass
    except KeyError:
        print("probleme avec la session")

    form = CritiqueTicketForm()
    if request.method == 'POST':
        form = CritiqueTicketForm(request.POST)
        if form.is_valid():
            critique_note = request.POST.get('checkbox')
            if not critique_note:
                return redirect('/creer-ticket-et-critique')
            else:
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


def logout_view(request):
    request.session['connected'] = False
    return redirect('/index')


def page_flux(request):
    try:
        if not request.session['connected']:
            print(request.session['connected'])
            return redirect('/index')
        else:
            pass
    except KeyError:
        print("probleme avec la session")

    user = User.objects.get(username=request.session['username'])
    user_id = user.id
    users_id = [following.followed_user.id for following in UserFollows.objects.filter(user=user_id)]
    users_id.append(user_id)
    followings_tickets = Ticket.objects.filter(user_id__in=users_id)
    followings_reviews = Review.objects.filter(user_associe_id__in=users_id)
    tickets = Ticket.objects.all()
    reviews = Review.objects.all().order_by('-time_created')
    tickets_already_commented = Review.objects.filter(user_associe_id=user_id)
    tickets_already_commented = [review.ticket_associe_id for review in tickets_already_commented]
    print(tickets_already_commented)
    tickets_reviews = sorted(chain(followings_tickets, followings_reviews), key=attrgetter('time_created'),
                             reverse=True)
    context = {
        'user_id': user_id,
        'tickets_reviews': tickets_reviews,
        'tickets': tickets,
        'reviews': reviews,
        'tickets_already_commented': tickets_already_commented
    }

    return render(request, 'templates/blog/tickets_reviews.html', context)


def page_vos_flux_text(request):
    try:
        if not request.session['connected']:
            print(request.session['connected'])
            return redirect('/index')
        else:
            pass
    except KeyError:
        print("probleme avec la session")

    user = User.objects.get(username=request.session['username'])
    tickets = Ticket.objects.filter(user=user)
    reviews = Review.objects.filter(user_associe=user)
    reviews_ticket_associeted_id = [review.ticket_associe_id for review in reviews]
    tickets_associated_to_reviews = Ticket.objects.filter(id__in=reviews_ticket_associeted_id)
    tickets_reviews = sorted(chain(tickets, reviews), key=attrgetter('time_created'),
                             reverse=True)

    context = {
        'tickets_associated_to_reviews': tickets_associated_to_reviews,
        'tickets_reviews': tickets_reviews,
        'user_id': user.id
    }
    return render(request, 'templates/blog/posts_test.html', context)


def page_supprimer_review(request, review_id):
    try:
        if not request.session['connected']:
            print(request.session['connected'])
            return redirect('/index')
        else:
            pass
    except KeyError:
        print("probleme avec la session")

    user = User.objects.get(username=request.session['username'])
    try:
        review = Review.objects.get(id=review_id, user_associe=user)
    except ObjectDoesNotExist:
        return redirect('/vos-posts')
    except ValueError:
        return redirect('/vos-posts')

    if request.method == 'POST':
        submit_response = request.POST.get('submit')
        if submit_response == "oui":
            review.delete()
            review_deleted = True
            context = {
                'review_deleted': review_deleted
            }
            return render(request, 'templates/blog/supprimer-review.html', context)
        else:
            review_not_delated = True
            context = {
                'review_not_deleted': review_not_delated,
                'review': review
            }
            return render(request, 'templates/blog/supprimer-review.html', context)
    else:
        context = {
            'review': review
        }
        return render(request, 'templates/blog/supprimer-review.html', context)


def page_modifier_review(request, review_id):
    try:
        if not request.session['connected']:
            print(request.session['connected'])
            return redirect('/index')
        else:
            pass
    except KeyError:
        print("probleme avec la session")

    modif_review = True
    error = False
    user = User.objects.get(username=request.session['username'])
    user_id = user.id
    review_modifiee = False
    try:
        review = Review.objects.get(id=review_id, user_associe_id=user_id)
        review_ticket_associe_id = review.ticket_associe_id
        ticket = Ticket.objects.get(id=review_ticket_associe_id)
    except ValueError:
        return redirect('/vos-posts')
    except ObjectDoesNotExist:
        return redirect('/vos-posts')
    form = CritiqueModifForm()
    if request.method == "POST":
        form = CritiqueModifForm(request.POST)
        if form.is_valid():
            critique_title = form.cleaned_data['titre']
            critique_note = request.POST.get('checkbox')
            print(critique_note)
            critique_commentaire = form.cleaned_data['commentaire']
            dictionnaire_post = {'note': critique_note, 'title': critique_title,
                                 'commentaire': critique_commentaire}
            if not critique_note and not critique_commentaire and \
                    not critique_title:
                review_modifiee = False
                error = True
            else:
                for post in dictionnaire_post:
                    if not dictionnaire_post[post]:
                        pass
                    elif dictionnaire_post[post] == critique_note:
                        print("c'est la note")
                        if int(critique_note) not in [0, 1, 2, 3, 4, 5]:
                            error = True
                        else:
                            review.rating = int(critique_note)
                    else:
                        if dictionnaire_post[post] == critique_title:
                            review.headline = critique_title
                        if dictionnaire_post[post] == critique_commentaire:
                            review.body = critique_commentaire
                    try:
                        review.time_created = datetime.now()
                        review.save()
                        review_modifiee = True
                    except IntegrityError:
                        error = True
                        context = {
                            'error': error
                        }
                        return render(request, 'templates/blog/creation-critique.html', context)

            context = {
                'modif_review': modif_review,
                'review_modifiee': review_modifiee,
                'form': form,
                'review': review,
                'ticket': ticket,
                'error': error
            }
            return render(request, 'templates/blog/creation-critique.html', context)
        else:
            print("le formulaire est invalide.")
            error = True
    else:
        pass

    context = {
        'modif_review': modif_review,
        'error': error,
        'form': form,
        'ticket': ticket,
        'review': review,
        'user_id': user_id,
    }
    return render(request, 'templates/blog/creation-critique.html', context)


def page_reset_password(request):
    try:
        if request.session['connected']:
            print(request.session['connected'])
            return redirect('/flux')
        else:
            pass
    except KeyError:
        print("probleme avec la session")
    form = ResetPasswordForm()
    message = False
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not email:
                message = "Le champ n'a pas été rempli"
            else:
                try:
                    User.objects.get(email=email)
                    message = "Un mail a été envoyé pour réinitialiser votre mot de passe"
                except ObjectDoesNotExist:
                    message = "L'email rentré n'existe pas dans la base de données."
        else:
            message = "Le formulaire n'est pas bien rempli."
    else:
        pass
    context = {
        'form': form,
        'message': message
    }
    return render(request, 'templates/blog/password-oublie.html', context)
