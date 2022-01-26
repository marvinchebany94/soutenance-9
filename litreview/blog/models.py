from django import forms
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.forms.widgets import EmailInput, TextInput


class User(models.Model):
    """
    se renseigner sur : AbstractUser
    """
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def unique_username(self, username):
        try:
            User.objects.get(username=username)
            return False
        except ObjectDoesNotExist:
            return True

    def same_passwords(self, password, password2):
        if password == password2:
            return True
        else:
            return False

    def unique_email(self, email):
        try:
            User.objects.get(email=email)
            return False
        except ObjectDoesNotExist:
            return True

    def connexion_autorized(self, username, password):
        try:
            User.objects.get(username=username, password=password)
            return True
        except ObjectDoesNotExist:
            return False


# Create your models here.
class Ticket(models.Model):
    # Your Ticket model definition goes here
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def unique_title_by_user(self, title, user_id):
        try:
            Ticket.objects.get(title=title, user_id=user_id)
            return False
        except ObjectDoesNotExist:
            return True


class Review(models.Model):
    ticket_associe = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user_associe = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_by")

    def RelationAlreadyExists(self, user_id, followed_user_id):
        try:
            UserFollows.objects.get(user=user_id, followed_user=followed_user_id)
            return True
        except ObjectDoesNotExist:
            return False

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)


class InscriptionForm(forms.Form):
    username = forms.CharField(max_length=150, required=True,
                               widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'placeholder': "Mot de passe"}))
    password2 = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'placeholder': "Comfirmer mot de passe"}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'placeholder': "Ton email"}))


class ConnexionForm(forms.Form):
    username = forms.CharField(max_length=150, required=True,
                               widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'placeholder': "Mot de passe"}))


class TicketForm(forms.Form):
    title = forms.CharField(max_length=128, required=True, label='Titre')
    description = forms.CharField(max_length=2048, label='Description',
                                  widget=forms.TextInput(), required=False)
    image = models.ImageField(blank=True)


class TicketModifForm(forms.Form):
    title = forms.CharField(max_length=128, label='titre', required=False,
                            widget=forms.TextInput(attrs={'value': ''}))
    description = forms.CharField(max_length=2048, label='description', required=False,
                                  widget=forms.TextInput(attrs={'value': ''}))


class CritiqueTicketForm(forms.Form):
    title = forms.CharField(max_length=128, required=True, label='Titre')
    description = forms.CharField(max_length=2048, label='Description',
                                  widget=forms.TextInput(), required=False)
    image = models.ImageField(blank=True)
    headline = forms.CharField(max_length=128, label='Titre', required=True,
                               widget=forms.TextInput())
    body = forms.CharField(max_length=8192, label='Commentaire', required=True,
                           widget=forms.TextInput())


class AddUser(forms.Form):
    UserResearch = forms.CharField(label="Suivre d'autres utilisateurs", required=True,
                                   widget=forms.TextInput(
                                       attrs={'placeholder': "Nom d'utilisateur"}))

