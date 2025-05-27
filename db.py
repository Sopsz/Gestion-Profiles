import sqlite3

def creer_base_de_donnees():
    # Se connecter à la base de données (elle sera créée si elle n'existe pas)
    connection = sqlite3.connect('gestion_profiles.db')
    curseur = connection.cursor()
    
    # Créer la table addons
    curseur.execute('''
    CREATE TABLE IF NOT EXISTS addons (
        id INTEGER PRIMARY KEY,
        nom TEXT NOT NULL,
        version TEXT NOT NULL
    )
    ''')
    
    # Créer la table profiles avec une clé étrangère vers addons
    curseur.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY,
        nom_profile TEXT NOT NULL,
        description TEXT,
        string_profile TEXT,
        id_addons INTEGER,
        FOREIGN KEY (id_addons) REFERENCES addons(id)
    )
    ''')
    
    # Valider les changements et fermer la connexion
    connection.commit()
    connection.close()
    print("Base de données créée avec succès!")

def clear_all_data():
    """
    Supprime tous les enregistrements des tables addons et profiles
    Returns:
        tuple: (nombre de profiles supprimés, nombre d'addons supprimés)
    """
    connection = None
    try:
        connection = sqlite3.connect('gestion_profiles.db')
        cursor = connection.cursor()
        
        # Désactiver temporairement les contraintes de clé étrangère
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        # Supprimer tous les profiles d'abord
        cursor.execute("DELETE FROM profiles")
        profiles_deleted = cursor.rowcount
        
        # Puis supprimer tous les addons
        cursor.execute("DELETE FROM addons")
        addons_deleted = cursor.rowcount
        
        # Réactiver les contraintes
        cursor.execute("PRAGMA foreign_keys = ON")
        
        connection.commit()
        return (profiles_deleted, addons_deleted)
        
    except sqlite3.Error as e:
        if connection:
            connection.rollback()
        raise Exception(f"Erreur lors de la suppression des données: {e}")
    finally:
        if connection:
            # S'assurer que les contraintes sont réactivées même en cas d'erreur
            try:
                cursor.execute("PRAGMA foreign_keys = ON")
            except:
                pass
            connection.close()

def seed_base_de_donnees():

    print(clear_all_data())

    addons_add("Bartender4", "11.1.5")
    addons_add("WeakAura", "11.0")
    addons_add("omnibar", "5.5.0")

    profiles_add("Mage Arcane PvE", "pack de classe", "!WAerpgerg^zoeringfghzelidnvzehoirnvetestestestestestestestest", 2)
    profiles_add("Main Profile", "barre des sorts PvE", "!Bartender4erpgerg^zoeringfghzelidnvzehoirnvetestestestestestestestest", 1)
    profiles_add("Arena 3s", "Kicks", "!Omnibarerpgerg^zoeringfghzelidnvzehoirnvetestestestestestestestest", 3)

    print('Base de données seedé avec succès!')

def addons_getbyid(addon_id):
    """Récupère un addon par son ID"""
    connection = sqlite3.connect('gestion_profiles.db')
    curseur = connection.cursor()
    
    curseur.execute("SELECT * FROM addons WHERE id = ?", (addon_id,))
    result = curseur.fetchone()
    
    connection.close()
    
    if result:
        return {
            'id': result[0],
            'nom': result[1],
            'version': result[2]
        }
    return None

def profiles_getbyid(profile_id):
    """Récupère un profile par son ID"""
    connection = sqlite3.connect('gestion_profiles.db')
    curseur = connection.cursor()
    
    curseur.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,))
    result = curseur.fetchone()
    
    connection.close()
    
    if result:
        return {
            'id': result[0],
            'nom_profile': result[1],
            'description': result[2],
            'string_profile': result[3],
            'id_addons': result[4]
        }
    return None

def addons_add(nom, version):
    """
    Ajoute un nouvel addon à la table addons
    Args:
        nom (str): Nom de l'addon
        version (str): Version de l'addon
    Returns:
        int: L'ID de l'addon créé
    """
    connection = sqlite3.connect('gestion_profiles.db')
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO addons (nom, version) VALUES (?, ?)",
            (nom, version)
        )
        addon_id = cursor.lastrowid
        connection.commit()
        return addon_id
    except sqlite3.Error as e:
        connection.rollback()
        raise Exception(f"Erreur lors de l'ajout de l'addon: {e}")
    finally:
        connection.close()

def profiles_add(nom_profile, description, string_profile, id_addons):
    """
    Ajoute un nouveau profile à la table profiles
    Args:
        nom_profile (str): Nom du profile
        description (str): Description du profile
        string_profile (str): Chaîne de caractères du profile
        id_addons (int): ID de l'addon associé
    Returns:
        int: L'ID du profile créé
    """
    connection = sqlite3.connect('gestion_profiles.db')
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            """INSERT INTO profiles 
            (nom_profile, description, string_profile, id_addons) 
            VALUES (?, ?, ?, ?)""",
            (nom_profile, description, string_profile, id_addons)
        )
        profile_id = cursor.lastrowid
        connection.commit()
        return profile_id
    except sqlite3.Error as e:
        connection.rollback()
        raise Exception(f"Erreur lors de l'ajout du profile: {e}")
    finally:
        connection.close()

def profiles_delete(profile_id):
    """
    Supprime un profile de la table profiles
    Args:
        profile_id (int): ID du profile à supprimer
    Returns:
        bool: True si suppression réussie, False sinon
    """
    connection = sqlite3.connect('gestion_profiles.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
        connection.commit()
        return cursor.rowcount > 0  # Retourne True si une ligne a été supprimée
    except sqlite3.Error as e:
        connection.rollback()
        raise Exception(f"Erreur lors de la suppression du profile: {e}")
    finally:
        connection.close()

def addons_getall():
    """
    Récupère tous les addons de la table addons
    Returns:
        list: Liste de dictionnaires représentant tous les addons
              ou None en cas d'erreur
    """
    connection = None
    try:
        connection = sqlite3.connect('gestion_profiles.db')
        connection.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM addons ORDER BY id")
        rows = cursor.fetchall()
        
        # Convertir les Row en dictionnaires
        return [dict(row) for row in rows]
        
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des addons: {e}")
        return None
    finally:
        if connection:
            connection.close()

def profiles_getall():
    """
    Récupère tous les profiles de la table profiles
    Returns:
        list: Liste de dictionnaires représentant tous les profiles
              ou None en cas d'erreur
    """
    connection = None
    try:
        connection = sqlite3.connect('gestion_profiles.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM profiles ORDER BY id")
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
        
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des profiles: {e}")
        return None
    finally:
        if connection:
            connection.close()


