
import streamlit as st
import pandas as pd
import random
import os

# Charger le fichier de base
def load_data(file_path):
    return pd.read_excel(file_path)

# Fonction pour créer des groupes tout en évitant les redondances
def create_groups(df, group_size, history_file):
    all_participants = df['Nom'] + ' ' + df['Prénom']
    all_participants = all_participants.tolist()

    # Charger l'historique existant
    if os.path.exists(history_file):
        history = pd.read_csv(history_file)
        past_groups = history['Group'].tolist()
    else:
        past_groups = []

    # Mélanger les participants
    random.shuffle(all_participants)

    # Créer les groupes
    groups = []
    while len(all_participants) >= group_size:
        group = all_participants[:group_size]
        all_participants = all_participants[group_size:]

        # Vérifier si le groupe existe déjà dans l'historique
        if ', '.join(sorted(group)) not in past_groups:
            groups.append(group)

    # Ajouter les participants restants dans un groupe
    if all_participants:
        groups.append(all_participants)

    # Sauvegarder dans l'historique
    if groups:
        new_history = pd.DataFrame({
            'Group': [', '.join(sorted(group)) for group in groups]
        })

        if os.path.exists(history_file):
            new_history.to_csv(history_file, mode='a', header=False, index=False)
        else:
            new_history.to_csv(history_file, index=False)

    return groups

# Interface Streamlit
st.title("Créateur de Groupes")

# Charger les données
uploaded_file = st.file_uploader("Chargez le fichier Excel contenant la liste des participants", type=["xlsx"])
if uploaded_file:
    df = load_data(uploaded_file)
    st.write("Aperçu des données :", df.head())

    # Paramètres utilisateur
    group_size = st.number_input("Nombre de personnes par groupe :", min_value=2, max_value=len(df), value=3)

    # Chemin du fichier historique
    history_file = 'group_history.csv'

    if st.button("Créer les groupes"):
        groups = create_groups(df, group_size, history_file)

        if groups:
            st.success("Groupes créés avec succès !")
            for i, group in enumerate(groups, start=1):
                st.write(f"Groupe {i} : {', '.join(group)}")
        else:
            st.warning("Tous les groupes possibles ont déjà été créés !")

    # Option pour afficher l'historique
    if os.path.exists(history_file):
        if st.checkbox("Afficher l'historique des groupes"):
            history = pd.read_csv(history_file)
            st.write(history)
