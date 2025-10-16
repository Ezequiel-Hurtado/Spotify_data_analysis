# 🎵 Spotify Project – Data Analysis and GUI in Python

**Programming Language 1 – Academic Year 2023-2024**

---

## 🎯 Project Objective

The goal of this project is to analyze **Spotify streaming data** using Python, build a **content search engine**, and develop a **graphical user interface (GUI)** that allows interactive exploration of the dataset.

The project is divided into **three main parts**:

1. **Descriptive analysis and data visualization**
2. **Content search and retrieval program**
3. **Graphical interface using Tkinter**

---

## 📂 Data Sources

  * `artists.csv` – Artist information
  * `tracks.csv` – Track information (1921–2020)
  * `spotify_top200_global.csv` – Global Top 200 songs for 2020

All data files are stored in the `/data` directory.

---

## 🧭 Project Structure

```
spotify_project/
│
├── data/                       # Source CSV files
│   ├── artists.csv
│   ├── tracks.csv
│   └── spotify_top200_global.csv
│
├── scripts/                    # Python scripts
│   ├── analysis.py             # Part 1: descriptive analysis and plots
│   ├── search_engine.py        # Part 2: search functionalities
│   ├── interface.py            # Part 3: Tkinter GUI
│   
│
├── report.pdf                  # Project report
└── README.md                   # This file
```

---

## 🧮 Part 1 – Descriptive Analysis and Visualization

This section focuses on **exploring and describing the Spotify datasets** using Python libraries such as Pandas and Matplotlib.

Analyses performed:

1. Identify the **10 most popular artists** and visualize their follower counts.
2. Compute the **number of tracks released per year** and display the trend over time.
3. Find **artists with the most distinct tracks in the 2020 Global Top 200**, ordered by total streams if tied.
4. Examine **relationships between song popularity** and other variables (energy, danceability, valence, etc.) from `tracks.csv`.

All visualizations are created with `matplotlib` and `seaborn`.

---

## 🔍 Part 2 – Content Search Program

A **search engine** allows users to query the datasets interactively.
It includes the following functionalities:

* **Search by artist name**
  ➤ Displays follower count, top 3 most popular songs, top 3 most recent songs, and number of songs appearing in the 2020 Global Top 200.

* **Search by song title**
  ➤ Returns matching results sorted by popularity (limited to 20 results).

* **Search by year and genre**
  ➤ Returns matching songs, sorted by artist popularity and then by song popularity.

Results can be displayed in the console or through the graphical interface.

---

## 🖥️ Part 3 – Graphical User Interface (Tkinter)

The GUI allows users to interact with the program without writing code.
It provides:

* Input fields for **artist name**, **song title**, **year**, and **genre**
* A **results display area** showing songs and artist information
* **Clickable links to artist Wikipedia pages**, when available

---
