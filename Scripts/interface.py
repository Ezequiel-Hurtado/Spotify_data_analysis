#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 14:16:13 2023

@author: ezequielhurtado
"""


#from tabulate import tabulate
import pandas as pd
#import numpy as np

from ast import literal_eval

from datetime import datetime

import tkinter as tk
from tkinter import ttk

import webbrowser

import functions as ft

import rapidfuzz as rf 
from difflib import SequenceMatcher

# import packages as pk -> Module contenant tous les fonctions 

artists = pd.read_csv("../DATA/artists.csv")
spotify_top200_global = pd.read_csv("../DATA/spotify_top200_global.csv")
tracks = pd.read_csv("../DATA/tracks.csv")

# Utilisation Module Fonctions
# ft.apply_data(df_tracks)

# Les fonctions search font appel au modul Fonctions
def search_artist():
    """
Fonction appelée pour chercher des informations sur un artiste.
Récupère le nom de l'artiste à partir de ce que l'utilisateur a saisi,
puis utilise la fonction 'info_artiste' pour afficher les résultats dans l'interface.

Input:
    La fonction utilise les variables suivantes:
    - artist_entry: Entry, champ de saisie pour le nom de l'artiste
    - result_text: StringVar, variable de texte pour afficher les résultats
    - df_artists: DataFrame, DataFrame des artistes
    - df_top: DataFrame, DataFrame du top 200 global
    - df_tracks: DataFrame, DataFrame des chansons

Output:
    La fonction met à jour la variable result_text
    pour afficher les informations sur l'artiste dans l'interface.
"""
    artist_name = artist_entry.get()
    # result_text.set(search_artist_info(artist_name))
    result_text.set(ft.search_artist_functions(tracks, artists,
                                    spotify_top200_global, artist_name))
 
    
def search_song():
    """
  Fonction appelée quand on recherche les informations d'une chanson.
  Récupère le titre de la chanson à partir de ce qu'a saisi l'utilisateur,
  puis utilise la fonction 'recherche_chanson' pour afficher les résultats dans l'interface.

  Input:
      La fonction utilise les variables suivantes:
      - song_entry: Entry, champ de saisie pour le titre de la chanson
      - result_text: StringVar, variable de texte pour afficher les résultats
      - df_tracks: DataFrame, DataFrame des chansons

  Output:
      La fonction met à jour la variable result_text
      pour afficher les résultats de recherche de chanson dans l'interface.
  """
    song_title = song_entry.get()
    ft.view_table(ft.search_song_functions(tracks,song_title), two_frame)


def search_year_genre():
    """
Fonction appelée quand on recherche par année et par genre.
Récupère l'année et le genre à partir de ce qu'a saisi l'utilisateur,
puis utilise la fonction 'rechercher_par_annee_genre' pour afficher les résultats dans l'interface.

Input:
    La fonction utilise les variables suivantes:
    - year_entry: Entry, champ de saisie pour l'année
    - genre_entry: Entry, champ de saisie pour le genre
    - result_text: StringVar, variable de texte pour afficher les résultats
    - df_tracks: DataFrame, DataFrame des chansons
    - df_artists: DataFrame, DataFrame des artistes

Output:
    La fonction met à jour la variable result_text
    pour afficher les résultats de recherche par année et genre dans l'interface.
"""
    year = year_entry.get()
    genre = genre_entry.get()
    ft.view_table(ft.search_gender_year_functions(year, genre, tracks,
                                                  artists), two_frame)
    

def wiki_open():
    """
   Récupère le nom de l'artiste à partir de ce qu'a saisi l'utilisateur,
   l'ajoute à l'URL de Wikipedia, puis ouvre la page Wikipedia associée dans un navigateur.

   Input:
       Aucun argument explicite ici, mais la fonction utilise les variables globales suivantes:
       - artist_entry: Entry, champ de saisie pour le nom de l'artiste

   Output:
       Aucun retour explicite ici, mais la fonction ouvre la page Wikipedia de l'artiste
       dans un navigateur.
   """
    artist_name = artist_entry.get()
    artist_name = artist_name.replace(" ","_")
    webbrowser.open_new('https://en.wikipedia.org/wiki/'+ artist_name)
       

# Interface graphique Tkinter

# Couleur de fond de la fenêtre et création de la fenêtre
root = tk.Tk()

root.title('Recherche Spotify Data') # Titre Fenetre

root.geometry('1800x500') # Dimensions
root['bg'] = 'black' # Couleur de fond

root.resizable(height = True, width = True)

one_frame = tk.Frame(root, background= 'black', height=500, width=700)
two_frame = tk.Frame(root,background= 'black',height= 500, width=1100)


# Titre dans la fênetre où  le code de couleur correspond à celui utilisé par Spotify
title_label = tk.Label(one_frame, text =' Spotify Recherche',
                       font =("GothamBold",30, "bold") ,
                       fg = "#1ED760", 
                       bg = "black")
title_label.place( x ='140 ', y='20')



# Ajout des éléments de l'interface (entrées, boutons, résultats, etc.)
artist_label = tk.Label(one_frame, text='Nom de l\'artiste:', fg = "#1ED760", bg = "black")
artist_entry = tk.Entry(one_frame) # Barre d'entrée de texte
artist_button = tk.Button(one_frame,
                          text='Rechercher', 
                          command= search_artist, 
                          highlightbackground= "black") # Paramétres et fonctions des boutons


# Ajout des autres éléments (song_label, song_entry, song_button, year_label, year_entry, genre_label, genre_entry, etc.)
song_label = tk.Label(one_frame,
                      text='Titre de la chanson:', 
                      fg = "#1ED760", 
                      bg = "black")
song_entry = tk.Entry(one_frame)
song_button = tk.Button(one_frame, 
                        text='Rechercher',
                        command= search_song,
                        highlightbackground= "black")

year_label = tk.Label(one_frame,
                      text='Année:', 
                      fg = "#1ED760", 
                      bg = "black")

year_entry = tk.Entry(one_frame, 
                      width=10)

genre_label = tk.Label(one_frame,
                       text='Genre:',
                       fg = "#1ED760",
                       bg = "black")

genre_entry = tk.Entry(one_frame,
                       width=10)

year_button = tk.Button(one_frame, 
                        text='Rechercher', 
                        command= search_year_genre,
                        highlightbackground= "black")

yt_button = tk.Button(one_frame,
                      text='Wikipedia',
                      command= wiki_open, highlightbackground= "black")

# Placement des éléments dans la fenêtre Tkinter 

artist_label.place(x ='20 ', y='70')
artist_entry.place(x='150', y ='70')
artist_button.place(x='350', y='70')

song_label.place(x ='20 ', y='120')
song_entry.place(x='150', y ='120')
song_button.place(x='350', y='120')

year_label.place(x ='20', y='170')
year_entry.place(x='150', y ='170')
genre_label.place(x ='275 ', y='170')
genre_entry.place(x='350', y ='170')
year_button.place(x='460', y='170')

yt_button.place(x ="460" ,y="70")

result_text = tk.StringVar()
result_label = tk.Label(one_frame,
                        textvariable=result_text,
                        fg = "black",
                        bg = "#1ED760",
                        justify = "center")

result_label.place(x = 20, y= 275)


one_frame.pack(side = 'left')
two_frame.pack(side= 'right')
root.mainloop()

