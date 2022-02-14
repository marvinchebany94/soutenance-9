# soutenance-9

Le project consiste en une application web deployée à l'aide du framework django. Le site qu'il nous était demandé de faire est un site sur lequel on peut s'inscrire, se connecter, créer des tickets, répondre à des des tickets, s'abonner à des gens, se désabonner, et se deconncter.

##[Installation]

ouvrir l'invite de commandes

cd "chemin du dossier"

python -m venv env (creer l'environnement env)

cd env/Scripts

activate (pour activer l'environnement)

cd ..

cd ..

python -m pip install -r requirements.txt (on telecharge dans notre environnement les modules nécéssaires)

cd  litreview

manage.py runserver --insecure (le --insecure sert à faire en sorte que le site utilise nos fichiers .css même en DEBUG = False dans settings.py)


###[utilisation]

Dans l'invite de commande la ligne correspondant à l'url à entrer dans le navigateur vous sera donné. 
---> starting development server at http://127.0.0.1/

*-- s'inscrire --*

/inscription/   --> entrer un nom d'utilisateur | mot de passe | confirmation du mot de passe | un email @gmail.com 

/index/         --> entrer son nom d'utilisateur | mot de passe

                mot de passe oublié?  --> Si vous avez oublié votre mot de passe vous cliquer ici, vous entrez votre email, puis un mail vous sera envoyé pour en créer un nouveau. (Obselete pour le moment)
                

/flux/          --> c'est la page sur laquelle on arrive quand on se connecte. On peut voir les tickets et critiques des personnes que l'on suit avec : le nom d'utilisateur, la date de création, le titre, la description et la note attribuée. 

                    --> bouton "demander une critique" pour créer un ticket (titre | description | telecharger le fichier(obselete)) /creer-un-ticket/
                    
                    --> bouton "Créer une critique" pour creer un ticket et sa critique en même temps (titre | description | telecharger le fichier(obselete) | titre critique |
                        Note critique | Commentaire critique)  /creer-ticket-et-critique/
                        
                --> bouton "Crér une critique" sous les tickets auquels nous n'avons pas répondu /creer-une-critique/{ticket_id}/
                
                
/vos-posts/     --> Il faut soit cliquer sur "Posts" dans la liste des liens, soit entrer cet url dans la barre de navigation.

                    --> liste de ses tickets
                    
                       --> bouton modifier | supprimer  
                       
                    --> Liste de ses critiques 
                    
                       --> bouton modifier | supprimer
                       
                       
/abonnement/    --> Cliquer sur le lien "Abonnement" ou écrire l'url dans la barre de navigation.

                   --> Suivre des personnes en entrant leur nom dans le champ sous "Suivre d'autres utilisateurs"
                   
                   --> Liste des personnes auquelles nous sommes abonnés sous le titre "Abonnements"
                   
                      --> bouton "Désabonner" à côté de chaque utilisateur suivi
                      
                   --> liste des personnes qui nous suivent sous le titre "Abonnés"
                   
/deconnexion/     --> lien "Se deconnecter" ou entrer l'url dans la barre de navigation.

###[AXE D AMELIORATION]

Dans les prochaines mises à jours nous allons ajouter : 

    -->la possibilité aux personnes d'ajouter des images dans leurs tickets
    
    -->mise en route de l'url de changement de mot de passe. Pour le moment veuillez nous contacter directement pour recréer un mot de passe.
  
####Dossier Flake-Report 

      Un dossier flake-report se trouve dans /litreview. Le dossier flake-report se crée comme suit :

      Dans l'invite de commande se rendre dans le dossier qui contient blog/litreview/manage.py/db.sqlite3 

      -->flake8 --format=html --htmldir=flake-report
      
      La ligne créra un dossier flake/report contenant toutes les potentielles erreurs. Cliquer sur index.html pour avoir la liste des erreurs de tous les fichiers '.py'.
