#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 12:36:41 2023

@author: ezequielhurtado
"""
from tabulate import tabulate
import pandas as pd
import numpy as np
import re 
from ast import literal_eval

import rapidfuzz as rf 
from datetime import datetime
from difflib import SequenceMatcher

import tkinter as tk 
from tkinter import ttk

def search_artist_functions(df_tracks,
                            df_artists,
                            df_top,
                            name):
    
    """
    Recherche du nombre d'abonnées, chansons le plus populaires et recentes ainsi 
    que le nombre de chansons ayant été dans le top 200 spotify en 2020.

    Paramètres
    ----------
    df_tracks : DataFrame
        DataFrame contenant les données des musiques.
    df_artists : DataFrame 
        DataFrame contenant les données des artistes. 
    df_top : DataFrame 
        DataFrame contenant les top 200 de musiques en 2020. 
    name : String 
        Nom de l'artiste de notre intéret. 
    """

    name = name.strip().lower().replace(" ","")
    df_artists['name'] = df_artists['name'].apply(lambda x : str(x).strip().lower().replace(" ",""))

    df_artists_filter = pd.DataFrame(df_artists[df_artists['name']== name].sort_values(by = ['popularity'],
                                                                                       ascending = False))

    if df_artists_filter.empty == True: 
        res = str(f"Nous ne trouvons pas de correspondance pour '{name}' dans notre base.\n")
        return res
    
    df_artists_filter_resume = df_artists_filter.head(1)
    res = str(f"L'artiste '{name}' a {df_artists_filter_resume['followers'].values[0]} followers.\n")

    id_artist_filter = df_artists_filter_resume['id'].values[0]

    df_tracks_filter_popularity = pd.DataFrame(df_tracks[df_tracks['id_artists'].apply(lambda x : id_artist_filter in x)]).sort_values(by = ['popularity'],
                                                                                                                                       ascending= False)
    df_tracks_filter_popularity = df_tracks_filter_popularity.drop_duplicates(subset = ['name'],
                                                                              keep = 'first')
    popular_songs = list(df_tracks_filter_popularity['name'].head(3))

    if df_tracks_filter_popularity.empty: 
        res_temp_popularity = str(f"Aucune chanson a été trouvé pour la popularité.\n")
    else: 
        res_temp_popularity = str(f"L'artiste {name} a comme\nChansons populaires:{popular_songs}\n")

    res = res + res_temp_popularity

    df_tracks_filter_recent = pd.DataFrame(df_tracks[df_tracks['id_artists'].apply(lambda x : id_artist_filter in x)]).sort_values(by = ['release_date'],
                                                                                                                                   ascending= False)
    df_tracks_filter_recent = df_tracks_filter_recent.drop_duplicates(subset = ['name'],
                                                                      keep = 'first')
    recent_songs = list(df_tracks_filter_recent['name'].head(3))

    if df_tracks_filter_recent.empty: 
        res_temp_recent = str(f"Aucune chanson a été trouvé pour la recence.\n")
    else: 
        res_temp_recent = str(f"Chansons recentes:{recent_songs}\n")

    res = res + res_temp_recent

    list_songs_artists= set(df_tracks_filter_popularity['name'])
    list_top_200 = set(df_top['Title'])
    songs_top_200_artists = len(list(list_songs_artists & list_top_200 ))

    if songs_top_200_artists == 0: 
        res_temp_top = str(f"Aucune chanson a été trouvé dans le top200.")
    else: 
        res_temp_top = str(f"Il a {songs_top_200_artists} chansons dans le top 200")

    res = res +  res_temp_top
    return res

def search_song_functions(df_tracks, name):
    """
    Recherche dans notre base les chansons correspondant ou proche du texte introduit.

    Paramètres
    ----------
    df_tracks : DataFrame
        DataFrame contenant les données des musiques.
    name : String 
        Texte correspondant au nom de la chanson que l'on souhaite retrouver

    Retourne
    --------
    DataFrame
        Table contenant les liste qui sont proches de plus de 80%.

    Exemples
    --------
    """
    name = name.strip().lower().replace(" ","")
    df_tracks['name'] = df_tracks['name'].apply(lambda x : str(x).strip().lower().replace(" ",""))

    df_tracks['match_rate'] = df_tracks['name'].apply(lambda x : rf.distance.DamerauLevenshtein.normalized_similarity(x,name))
    
    df_tracks_filter = df_tracks[df_tracks['match_rate']> 0.8].sort_values(by = ['match_rate'],
                                                                           ascending = True)

    if df_tracks_filter.empty == True: 
        res = str(f"La chanson '{name}' ne trouve pas une correspondance. Veuillez rentrer un autre nom.")
        return df_tracks_filter
    else:
        near_songs = df_tracks_filter[['name',
                                       'artists',
                                       'popularity',
                                       'release_date',
                                       'match_rate']].head(20)

    res = near_songs[['name',
                      'artists',
                      'popularity',
                      'release_date',
                      'match_rate']]

    return near_songs

def search_gender_year_functions(year,
                                 gender,
                                 df_tracks,
                                 df_artists):
    """
    Recherche dans notre base par année et par genre les chansons les plus
    populaires par artistes

    Paramètres
    ----------
    year : Integer
        Année sur laquelle nous voulons faire notre recherche.
    gender : String 
        Texte correspondant au genre auquel on s'interesse
    df_tracks : DataFrame 
        DataFrame contenant les données des musiques. 
    df_artists : DataFrame 
        DataFrame contenant les données des artistes. 

    Retourne
    --------
    DataFrame
        Table contenant un tableau de maximum 20 lignes correspondant aux 
        musiques du genre et de l'année selectionnées. 

    Exemples
    --------
    """
    
    
    gender = gender.strip().lower().replace(" ","")
    year = int(year)

    df_artists_gender = df_artists[['id',
                                    'name',
                                    'genres',
                                    'popularity']][df_artists['genres'].apply(lambda x : gender in x)]
    
    df_tracks['year_release'] = df_tracks['release_date'].str[0:4].apply(lambda x: int(x))
    
    df_tracks_year = df_tracks[df_tracks['year_release']==year]

    artists_id_liste = list(set(df_artists_gender['id']))
    
    df_tracks_year = df_tracks_year.explode('id_artists')
    df_tracks_year['id_artists'] = df_tracks_year['id_artists'].apply(lambda x : str(x[2:-2]))
    
    df_tracks_year_filter = df_tracks_year[df_tracks_year['id_artists'].isin(artists_id_liste)]
    df_tracks_year_filter_merge = df_tracks_year_filter.merge(df_artists_gender[["id","popularity"]], 
                                                              how = 'left', 
                                                              left_on = 'id_artists', 
                                                              right_on = 'id',
                                                              suffixes=('_tracks', '_artists' )).sort_values(by = ['popularity_artists',
                                                                                                                   'popularity_tracks'],
                                                                                                             ascending = False)
    
    top_gender_year = df_tracks_year_filter_merge[['name',
                                                   'artists',
                                                   'popularity_tracks',
                                                   'release_date',
                                                   'popularity_artists']].head(20)

    res = top_gender_year.to_string(index=False)
    return  top_gender_year

def view_table(data,
               two_frame):
    """
    Introduire graphiquement notre tableau dans l'interface Tkinter. 

    Paramètres
    ----------
    data : DataFrame
        DataFrame contenant les données que nous voulons afficher.
    two_frame : Frame Tkinter 
        Frame de tkinter sur lequel nous voulons afficher notre tableau. 

    Retourne
    --------
    Permettre l'affichage sur Tkinter. 

    Exemples
    --------
    """
    for widget in two_frame.winfo_children():
        widget.destroy()

    if data.empty == False : 
        column_names = data.columns
        table = ttk.Treeview(two_frame,
                            columns = list(column_names),
                            show = 'headings')

        for i in data.columns: 
            table.heading(i, text= i)
        table.pack(expand= True)
        for i, row in data.iterrows():
            table.insert(parent = "",
                        index = tk.END,
                        values = list(row))
        table.place(x  = 20 , y = 70)
    else: 
        result_lable_search = tk.Label(two_frame, text ="La recherche n'aboutit à aucun résultat. Veuillez saisir les informations à nouveau.",
                       font =("GothamBold",14) ,
                       fg = "#1ED760", 
                       bg = "black")
        result_lable_search.place(x  = 20 , y = 70)

def apply_data(df_tracks):
    '''

    Parameters
    ----------
    df_tracks : 
        Mise en forme des dates dans le bon format.

    Returns
    -------
    df_tracks : DateTime
        Colonnes dates au bon format .

    '''
    df_tracks['release_date'] = pd.to_datetime(df_tracks['release_date'], errors='coerce')
    return df_tracks