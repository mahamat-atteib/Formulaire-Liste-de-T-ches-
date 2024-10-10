#Importer les modules  
import tkinter as tk                   
from tkinter import ttk                   
from tkinter import messagebox            
import sqlite3 as sql           #requête sql : on a une base de donnee 'tasks'       
import logging                  #créer un fichier logging qui s'appelle 'todolist.log'


#Configurer la journalisation
logging.basicConfig(filename='C:/Users/PC/Documents/1. MS-BIGDATA/P1/Kit Big Data/projet todo list Bis/todolist.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#Fonction qui permet d'Ajouter une tâche
def add_task():
    #Obtenir la chaine du champ 
    task_string = task_field.get()  
    #Vérifier si le nom de la tâche est renseignée ou non...  
    if len(task_string) == 0:  
        # Si l'utilisateur essaie d'ajouter une tâche VIDE, 
        # Un onglet "Erreur" s'affiche et annonce "Aucune tâche renseignée!"
        messagebox.showinfo('Erreur', 'Aucune tâche renseignée !')  
    else:  
        #Ajouter à la liste des tâches 
        tasks.append(task_string)  
        #Executer les requêtes SQL avec execute() 
        the_cursor.execute('INSERT INTO tasks VALUES (?)', (task_string ,))
        #Appel de la fonction pour la mise à jour de la liste 
        list_update()
        #Suppression de l'entrée dans le champ de saisie  
        task_field.delete(0, 'end')  
        #Journal : Ajout d'une tâche
    logging.debug(f"Ajout d'une tâche : {task_string}")

  
#Fonction pour mettre à jour la liste des tâches
def list_update():  
    #Appel de la fonction pour effacer la liste  
    clear_list()  
    #Parcourir les chaines de la liste 
    for task in tasks:  
        #Insérer des tâches dans la liste 
        task_listbox.insert('end', task)  
  
#Fonction qui permet de supprimer une tâche de la liste
def delete_task():  
    #utiliser la methode TRY 
    try:  
        #Obtenir l'entrée selectionnée dans la zone de liste
        the_value = task_listbox.get(task_listbox.curselection())  
        #  
        if the_value in tasks:  
            #Supprimer la tâche de la liste  
            tasks.remove(the_value)  
            #Appel de la fonction "mise à jour" de la liste créé plus haut 
            list_update()  
            #Utiliser la methode execute() pour executer une requête SQL 
            the_cursor.execute('DELETE FROM tasks WHERE title = ?', (the_value,))
    except:  
        #Message : aucun élément sélectionné.  
        messagebox.showinfo('Erreur', 'Aucune tâche sélectionnée ! Impossible de supprimer !')   
    #Log : supprimer une tâche
    logging.debug(f"Tâche supprimée : {the_value}")
     
  
#Fonction qui permet de supprimer TOUTES les tâches
def delete_all_tasks():  
    #Message de confirmation avant suppression  
    message_box = messagebox.askyesno('Attention', 'Etes-vous sûr de vouloir tout supprimer ?')  
    #Si la reponse à la question precedente est "OUI"  
    if message_box == True:  
        #Utiliser une boucle "while" pour parcourir toutes les tâches  
        while(len(tasks) != 0):  
            #Avec pop() on extrait les éléments de la liste (les tâches) 
            tasks.pop()  
        #Requête SQL pour supprimer les toutes les taches  
        the_cursor.execute('DELETE FROM tasks')  
        #Appel de la fonction "mise à jour" de la liste  
        list_update()  
  
#Fonction : Supprimer les tâches
def clear_list():  
    #Supprimer les tâches 
    task_listbox.delete(0, 'end')  
  
#Fonction : Quitter l'application 
def close():  
    #Afficher les éléments d'une liste  
    print(tasks)  
    #Fermer l'application avec "destroy()" 
    guiWindow.destroy()  
  
#Fonction : Récupérer les données de la base de donnee 
def retrieve_database():  
    #Parcourir la liste des tâches  
    while(len(tasks) != 0):  
        #Extraire les éléments d'une liste 
        tasks.pop()  
    #Parcourir les lignes de la table tasks
    for row in the_cursor.execute('SELECT title FROM tasks'):  
        # using the append() method to insert the titles from the table in the list  
        tasks.append(row[0])  
  
#Fonction "main" sur la fenêtre : TITRE, DIMENSION et COULEUR
if __name__ == "__main__":
    #Créer un objet de la classe tk()
    guiWindow = tk.Tk()  
    #Titre de la fenêtre
    guiWindow.title("To-Do List - Application")  
    #Dimension de la fenêtre de l'application:Largeur et Longueur
    guiWindow.geometry("500x450+750+250")  
    #Deasctiver l'option de redimensionnement  
    guiWindow.resizable(0, 0)
    #Couleur de l'arrière-plan  
    guiWindow.configure(bg = "#FAEBD7")    #F5FFFA     #FAEBD7     #F5FFFA     #a21e71    #6593c0
    #Connection à la base de donnée  "listOfTasks.db" 
    the_connection = sql.connect('listOfTasks.db')    
    #Création de l'objet "curseur" de la classe "curseur"  
    the_cursor = the_connection.cursor()  
    #Executer une requête SQL : créer une table "tasks"
    #Créer une TABLE "tasks" si elle n'existe pas
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title text)')
  
    #Liste de tâches vides
    tasks = []  
    
    #Exemple de couleurs : #6593c0(bleu), #FAEBD7(orange), #175732(verte), #a21e71(violet), #8B4513
    
    #Définir la couleur de "Frames" 
    header_frame = tk.Frame(guiWindow, bg = "#6593c0")      #coloriage de l'entête "TO-DO LIST"
    functions_frame = tk.Frame(guiWindow, bg = "#6593c0")   #coloriage du gauche, ou il y a les boutons 
    listbox_frame = tk.Frame(guiWindow, bg = "#6593c0")     #coloriage de droite, ou les taches sont enregistrées
  
    #Position des "Frames" dans l'application
    header_frame.pack(fill = "both")                                        #en haut
    functions_frame.pack(side = "left", expand = True, fill = "both")       #à gauche
    listbox_frame.pack(side = "right", expand = True, fill = "both")        #à droite
      
    #Paramètre du titre "TO-DO LIST"
    header_label = ttk.Label(  
        header_frame,  
        text = "To-Do List",           
        font = ("Consolas", "30"),  
        background = "#FAEBD7",  
        foreground = "#8B4513"  
    )

    #Interligne (espace) entre l'entête et ce qui est en dessous
    header_label.pack(padx = 20, pady = 20)  
      
    #Paramètre du WIDGET "Renseigner vos tâches"
    task_label = ttk.Label(  
        functions_frame,  
        text = "Renseigner vos tâches",  
        font = ("Consolas", "11", "bold"),    #bold : mettre en gras
        background = "#FAEBD7",  
        foreground = "#000000"  
    )
    
    # using the place() method to place the label in the application  
    task_label.place(x = 30, y = 40)  
      
    #Definir un champ de saisie : le champ ou on ecrit le nom de la tâche. 
    task_field = ttk.Entry(  
        functions_frame,  
        font = ("Consolas", "12"),  
        width = 19,  
        background = "#FFF8DC",  
        foreground = "#A52A2A"  
    )  
    # using the place() method to place the entry field in the application  
    task_field.place(x = 30, y = 80)  
  
    #Ajout du bouton "Ajout d'une tâche"
    add_button = ttk.Button(  
        functions_frame,  
        text = "Ajout d'une tâche",  
        width = 28,                 #longueur du bouton "Ajout d'une tâche" 
        command = add_task  
    )  
    
    #Ajout du bouton "Supprimer une tâche"
    del_button = ttk.Button(  
        functions_frame,  
        text = "Supprimer une tâche",  
        width = 28,                 #longueur du bouton "Supprimer une tâche" 
        command = delete_task  
    )  
    
    #Ajout du bouton "Supprimer toutes les tâches"
    del_all_button = ttk.Button(  
        functions_frame,  
        text = "Supprimer toutes les tâches",  
        width = 28,                 #longueur du bouton "Supprimer toutes les tâches"
        command = delete_all_tasks  
    )  
    
    #Ajout du bouton "Supprimer toutes les tâches"
    style = ttk.Style()
    # Configurez le style pour mettre en gras le texte du bouton et le rendre rouge
    style.configure('RedBold.TButton', font=('', 8, 'bold'), foreground='red')
    exit_button = ttk.Button(  
        functions_frame,  
        text = "Quitter",
        width = 28,
        style='RedBold.TButton',
        command = close, 
    ) 
    
    #Position des "Frames" : Ajouter, Supprimer,.., Quitter 
    add_button.place(x = 30, y = 120)  
    del_button.place(x = 30, y = 160)  
    del_all_button.place(x = 30, y = 200)  
    exit_button.place(x = 30, y = 240)  
  
    #Paramétrage du Listbox(), c'est là ou est listé toutes les tâches 
    task_listbox = tk.Listbox(  
        listbox_frame,  
        width = 30,                     #largeur
        height = 15,                    #hauteur
        selectmode = 'SINGLE',  
        background = "#FFFFFF",         #couleur fond        #FFFFFF   #000000
        foreground = "#000000",  
        selectbackground = "#CD853F",   #CD853F     #FAEBD7(orange)   #175732(verte)   #6593c0(bleu)   #a21e71(violet)
        selectforeground = "#FFFFFF"  
    )  

    
    # using the place() method to place the list box in the application  
    task_listbox.place(x = 10, y = 20)  
  
    #Appel des FONCTIONS
    retrieve_database()  
    list_update()  
    #Utiliser mainloop() pour executer l'application  
    guiWindow.mainloop()  
    #Etablir la connexion avec la base de donnee 
    the_connection.commit()  
    the_cursor.close()  
    
    #Fermer la journalisation
    logging.shutdown()
