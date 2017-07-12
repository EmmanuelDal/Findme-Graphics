#!/usr/bin/python
# -*-coding:UTF-8 -*-

from Tkinter import *
from pierky.ipdetailscache import IPDetailsCache
from tkFont import Font
import geocoder, os, socket, tkFileDialog, dns, dns.resolver, tkMessageBox

def data_ip():
    try:
        ip = donnee.get()
        name = socket.gethostbyname(ip) #convertir le site web en une adresse ip de type x.x.x.x

        i = geocoder.maxmind(name) #utilisation de package "maxmind" du module geocoder afin de geolocaliser
        a = i.json                 #l'hebergement du site web
        for b, c in a.items():
            texte.insert('1.0',(b, ":",c,'\n'))

        cache = IPDetailsCache()  # appel de la classe 'IPDetailsCache()'
        r = cache.GetIPInformation(name)  #utilisation de la methode 'GetIPInformation() pour obtenir l'ASN
        for cle, vals in r.items():  # select the items methods for show 'cle and valeur' values in boucle
            texte.insert('end',(cle, ":",vals,'\n'))

        reponse = dns.resolver.query(ip, 'MX')  # the variable 'reponse' contains the value MX of dns server
        for rdata in reponse:
            texte.insert('end',("seveurs mails:",rdata.exchange,'\n'))

        contenu = dns.resolver.query(ip, 'NS')  # the variable 'contenu' contains the value NS of dns server
        for resultat in contenu:
            texte.insert('end',("seveurs DNS:", resultat,'\n'))  # affiche tout les serveurs DNS

        command = "whois" + " " + ip
        process = os.popen(command)  # appel d'un commande systeme "popen" ppur executer la commande au dessus
        results = str(process.read())  # convertion du resultat en chaine de caractere et stockage dans une variable
        texte.insert('end', (results), '\n')

        command1 = "dnsmap" + " " + ip
        process1 = os.popen(command1)  # appel d'un commande systeme "popen" ppur executer la commande au dessus
        results1 = str(process1.read())  # convertion du resultat en chaine de caractere et stockage dans une variable
        texte.insert('end',(results1),'\n')

        tkMessageBox.showinfo('Resultat', 'Scan terminé')

    except socket.gaierror:
        return ("Address Unknown or Connection failed, tip on reset and put a good domain name")# msg a affiche quand le nom de domaine n'est pas connue

def message(): #fonction qui permet a inserer les données du resultat dans le widget Text() de Tkinter
    butonscan.config(state = NORMAL)
    butonscan.update_idletasks()
    col = data_ip()
    texte.insert('end',col)
    texte.config(state= DISABLED) # configuration du mode lecture de la fenetre(mode = lecture/ecriture)
    tkMessageBox.showerror('Erreur', 'Erreur réseau')

##CREATION DE LA FENTERE TKINTER ET SES PROPRIETES

#fonction pour reinitialiser toutes les entrées de la fenetre graphique
def reset_entree():
    entree.delete(0, END)
    texte.delete(1.0,END)

#fonction pour sauvegarder le resultat obtenu sous forme de fichier a extension ".csv"
def save_file():
    name = tkFileDialog.asksaveasfilename(initialdir='/',
                                          filetypes= (("json files", "*.csv"),("all files", "*.*")))
    data = texte.get(1.0, 'end-1c') #recuperation de tout les caractere du widget Text()
    with open(name, 'w') as outputFile:
        outputFile.write(data)

fen = Tk() #initialisation de la fenetre
fen.geometry('735x550') #dimensionnement de la fenetre
fen.title('AUDIT SITE') #titre de la fenetre
texte =Text(fen, width=100, height=30,wrap= 'word') #le cadre qui permet d'afficher les resultat de tout les scan

donnee = StringVar() #definir le type de donnée entré, ici c'est le type "string() = chaine de caractere"
donnee.set('')#configuration de la mise a jour de l'entrée

#creation des Labels(affichage) des noms sur la fenêtre
label= Label(fen, text='Entrer votre site web:', fg='red')
label_nom_entreprise_pied = Label(fen,text='Write by TheRipper, Copyright 2017, v1.0', fg='black')
taille = Font(family ='Cambria', weight = 'bold', size = 16)
label_nom = Label(fen,text= 'AUDIT SITE WEB',font = taille, fg = 'black')

#création de la zone de saisie
entree = Entry(fen, textvariable=donnee, width=30, bg='white', fg='black')

#creation des buttonns (Scan, Reinitiliser, Sortie, Sauvegarder)
butonscan = Button(fen, text='Scan', bg= 'red', command=message)
butonreset = Button(fen, text='Reinitialiser', bg= 'blue', fg = 'white', command= reset_entree)
butonexit = Button(fen, text='Sortie', bg= 'red', command= fen.destroy)
butonsave = Button(fen, text='Sauvegarder', bg= 'blue', fg = 'white', command= save_file)

#disposition de chaque button, label et zone de saisie sur la fenetre
entree.place(x= '130', y='450')
label.place(x= '0', y='450')
label_nom.place(x='250', y= '490')
label_nom_entreprise_pied.place(x='280', y='520')

texte.pack(side= TOP, padx= 0, fill =BOTH, expand= 0)
butonscan.place(x='380', y='446')
butonreset.place(x='445', y='446')
butonexit.place(x='548', y='446')
butonsave.place(x='620', y='446')

#lancement de la fenetre
fen.mainloop()
