# main.py
import tkinter as tk
from tkinter import messagebox, ttk
import db
import pyperclip

class AddonsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Addons et Profiles")
        self.root.geometry("1400x900")
        
        # Cadre principal
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame pour les addons (à gauche)
        self.addons_frame = tk.LabelFrame(
            self.main_frame, 
            text="Gestion des Addons",
            padx=10,
            pady=10
        )
        self.addons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame pour les profiles (à droite)
        self.profiles_frame = tk.LabelFrame(
            self.main_frame, 
            text="Gestion des Profiles",
            padx=10,
            pady=10
        )
        self.profiles_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # ----------------------------
        # PARTIE ADDONS (GAUCHE)
        # ----------------------------
        
        # Formulaire d'ajout d'addon
        self.add_addon_frame = tk.LabelFrame(
            self.addons_frame,
            text="Ajouter un Addon",
            padx=10,
            pady=10
        )
        self.add_addon_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(self.add_addon_frame, text="Nom:").grid(row=0, column=0, sticky=tk.W)
        self.nom_entry = tk.Entry(self.add_addon_frame, width=30)
        self.nom_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.add_addon_frame, text="Version:").grid(row=1, column=0, sticky=tk.W)
        self.version_entry = tk.Entry(self.add_addon_frame, width=15)
        self.version_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.add_button = tk.Button(
            self.add_addon_frame,
            text="Ajouter Addon",
            command=self.ajouter_addon,
            bg="#4CAF50",
            fg="white"
        )
        self.add_button.grid(row=2, column=1, sticky=tk.E, pady=5)
        
        # Liste des addons
        self.list_addons_frame = tk.LabelFrame(
            self.addons_frame,
            text="Liste des Addons",
            padx=10,
            pady=10
        )
        self.list_addons_frame.pack(fill=tk.BOTH, expand=True)
        
        self.addons_tree = ttk.Treeview(
            self.list_addons_frame,
            columns=("id", "nom", "version"),
            show="headings",
            selectmode="browse"
        )
        self.addons_tree.heading("id", text="ID")
        self.addons_tree.heading("nom", text="Nom")
        self.addons_tree.heading("version", text="Version")
        
        self.addons_tree.column("id", width=50, anchor=tk.CENTER)
        self.addons_tree.column("nom", width=200)
        self.addons_tree.column("version", width=100, anchor=tk.CENTER)
        
        addons_scroll = ttk.Scrollbar(
            self.list_addons_frame,
            orient=tk.VERTICAL,
            command=self.addons_tree.yview
        )
        self.addons_tree.configure(yscrollcommand=addons_scroll.set)
        
        self.addons_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        addons_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ----------------------------
        # PARTIE PROFILES (DROITE)
        # ----------------------------
        
        # Formulaire d'ajout de profile
        self.add_profile_frame = tk.LabelFrame(
            self.profiles_frame,
            text="Ajouter un Profile",
            padx=10,
            pady=10
        )
        self.add_profile_frame.pack(fill=tk.X, pady=5)
        
        # Nom du profile
        tk.Label(self.add_profile_frame, text="Nom:").grid(row=0, column=0, sticky=tk.W)
        self.profile_nom_entry = tk.Entry(self.add_profile_frame, width=30)
        self.profile_nom_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Description
        tk.Label(self.add_profile_frame, text="Description:").grid(row=1, column=0, sticky=tk.W)
        self.profile_desc_entry = tk.Entry(self.add_profile_frame, width=30)
        self.profile_desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # String Profile
        tk.Label(self.add_profile_frame, text="String Profile:").grid(row=2, column=0, sticky=tk.W)
        self.profile_string_entry = tk.Text(self.add_profile_frame, width=40, height=5)
        self.profile_string_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Addon associé
        tk.Label(self.add_profile_frame, text="Addon associé:").grid(row=3, column=0, sticky=tk.W)
        self.profile_addon_combobox = ttk.Combobox(self.add_profile_frame, width=28)
        self.profile_addon_combobox.grid(row=3, column=1, padx=5, pady=5)
        
        # Bouton d'ajout
        self.add_profile_button = tk.Button(
            self.add_profile_frame,
            text="Ajouter Profile",
            command=self.ajouter_profile,
            bg="#2196F3",
            fg="white"
        )
        self.add_profile_button.grid(row=4, column=1, sticky=tk.E, pady=5)
        
        # Liste des profiles associés
        self.list_profiles_frame = tk.LabelFrame(
            self.profiles_frame,
            text="Profiles Associés",
            padx=10,
            pady=10
        )
        self.list_profiles_frame.pack(fill=tk.BOTH, expand=True)
        
        self.profiles_tree = ttk.Treeview(
            self.list_profiles_frame,
            columns=("id", "nom", "description"),
            show="headings"
        )
        self.profiles_tree.heading("id", text="ID")
        self.profiles_tree.heading("nom", text="Nom du Profile")
        self.profiles_tree.heading("description", text="Description")
        
        self.profiles_tree.column("id", width=50, anchor=tk.CENTER)
        self.profiles_tree.column("nom", width=200)
        self.profiles_tree.column("description", width=300)
        
        profiles_scroll = ttk.Scrollbar(
            self.list_profiles_frame,
            orient=tk.VERTICAL,
            command=self.profiles_tree.yview
        )
        self.profiles_tree.configure(yscrollcommand=profiles_scroll.set)
        
        self.profiles_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        profiles_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ----------------------------
        # CONFIGURATION INITIALE
        # ----------------------------
        
        # Bind des événements
        self.addons_tree.bind("<<TreeviewSelect>>", self.afficher_profiles)
        self.profiles_tree.bind("<Double-1>", self.afficher_string_profile)
        
        # Charger les données initiales
        self.charger_addons()
        self.charger_combobox_addons()
        
    def charger_addons(self):
        """Charge la liste des addons dans le Treeview"""
        self.addons_tree.delete(*self.addons_tree.get_children())
        addons = db.addons_getall()
        
        if addons:
            for addon in addons:
                self.addons_tree.insert(
                    "",
                    tk.END,
                    values=(addon["id"], addon["nom"], addon["version"])
                )
    
    def charger_combobox_addons(self):
        """Charge la liste des addons dans la combobox"""
        addons = db.addons_getall()
        if addons:
            self.profile_addon_combobox['values'] = [
                f"{addon['id']} - {addon['nom']}" for addon in addons
            ]
            if addons:
                self.profile_addon_combobox.current(0)
    
    def afficher_profiles(self, event):
        """Affiche les profiles associés à l'addon sélectionné"""
        self.profiles_tree.delete(*self.profiles_tree.get_children())
        selection = self.addons_tree.selection()
        if not selection:
            return
            
        addon_id = self.addons_tree.item(selection[0])["values"][0]
        all_profiles = db.profiles_getall()
        
        if all_profiles:
            for profile in all_profiles:
                if profile["id_addons"] == addon_id:
                    self.profiles_tree.insert(
                        "",
                        tk.END,
                        values=(profile["id"], profile["nom_profile"], profile["description"])
                    )
    
    def afficher_string_profile(self, event):
        """Ouvre une fenêtre avec le string_profile du profile sélectionné"""
        selection = self.profiles_tree.selection()
        if not selection:
            return
            
        profile_id = self.profiles_tree.item(selection[0])["values"][0]
        profile = db.profiles_getbyid(profile_id)
        
        if profile:
            profile_window = tk.Toplevel(self.root)
            profile_window.title(f"Profile: {profile['nom_profile']}")
            profile_window.geometry("800x600")
            
            main_frame = tk.Frame(profile_window, padx=20, pady=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(
                main_frame,
                text=f"Contenu du profile '{profile['nom_profile']}'",
                font=("Helvetica", 14, "bold")
            ).pack(pady=10)
            
            text_frame = tk.Frame(main_frame)
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            text_scroll = tk.Scrollbar(text_frame)
            text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            profile_text = tk.Text(
                text_frame,
                wrap=tk.WORD,
                yscrollcommand=text_scroll.set,
                font=("Courier", 10)
            )
            profile_text.insert(tk.END, profile["string_profile"])
            profile_text.pack(fill=tk.BOTH, expand=True)
            
            text_scroll.config(command=profile_text.yview)
            
            btn_frame = tk.Frame(main_frame)
            btn_frame.pack(pady=10)
            
            tk.Button(
                btn_frame,
                text="Copier dans le presse-papier",
                command=lambda: self.copier_presse_papier(profile["string_profile"]),
                bg="#2196F3",
                fg="white"
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                btn_frame,
                text="Fermer",
                command=profile_window.destroy,
                bg="#f44336",
                fg="white"
            ).pack(side=tk.LEFT, padx=5)
    
    def ajouter_addon(self):
        """Ajoute un nouvel addon à la base de données"""
        nom = self.nom_entry.get()
        version = self.version_entry.get()
        
        if not nom or not version:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
            return
            
        try:
            db.addons_add(nom, version)
            self.charger_addons()
            self.charger_combobox_addons()
            self.nom_entry.delete(0, tk.END)
            self.version_entry.delete(0, tk.END)
            messagebox.showinfo("Succès", "Addon ajouté avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
    
    def ajouter_profile(self):
        """Ajoute un nouveau profile à la base de données"""
        nom = self.profile_nom_entry.get()
        description = self.profile_desc_entry.get()
        string_profile = self.profile_string_entry.get("1.0", tk.END).strip()
        addon_selection = self.profile_addon_combobox.get()
        
        if not nom or not string_profile or not addon_selection:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs obligatoires")
            return
            
        try:
            # Extraire l'ID de l'addon
            addon_id = int(addon_selection.split(" - ")[0])
            
            # Ajouter le profile
            db.profiles_add(nom, description, string_profile, addon_id)
            
            # Recharger les données
            selection = self.addons_tree.selection()
            if selection:
                self.afficher_profiles(None)
            
            # Vider les champs
            self.profile_nom_entry.delete(0, tk.END)
            self.profile_desc_entry.delete(0, tk.END)
            self.profile_string_entry.delete("1.0", tk.END)
            
            messagebox.showinfo("Succès", "Profile ajouté avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")
    
    def copier_presse_papier(self, text):
        """Copie le texte dans le presse-papier"""
        try:
            pyperclip.copy(text)
            messagebox.showinfo("Succès", "Le contenu a été copié dans le presse-papier!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de copier: {str(e)}")
    
        def supprimer_profile(self):
        """Supprime un profile par son ID"""
        profile_id = self.delete_profile_id_entry.get()
        
        if not profile_id:
            messagebox.showwarning("Erreur", "Veuillez entrer un ID de profile")
            return
            
        try:
            profile_id = int(profile_id)
            # Vérifier si le profile existe
            profile = db.profiles_getbyid(profile_id)
            if not profile:
                messagebox.showwarning("Erreur", f"Aucun profile trouvé avec l'ID {profile_id}")
                return
                
            # Confirmation de suppression
            if not messagebox.askyesno(
                "Confirmation",
                f"Êtes-vous sûr de vouloir supprimer le profile '{profile['nom_profile']}' (ID: {profile_id}) ?"
            ):
                return
                
            # Suppression
            success = db.profiles_delete(profile_id)
            if success:
                messagebox.showinfo("Succès", "Profile supprimé avec succès!")
                # Recharger les profiles affichés
                selection = self.addons_tree.selection()
                if selection:
                    self.afficher_profiles(None)
                # Vider le champ
                self.delete_profile_id_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Erreur", "La suppression a échoué")
                
        except ValueError:
            messagebox.showerror("Erreur", "L'ID doit être un nombre entier")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

if __name__ == "__main__":
    # Initialiser la base de données
    db.creer_base_de_donnees()
    db.seed_base_de_donnees()
    
    # Installer pyperclip si nécessaire
    try:
        import pyperclip
    except ImportError:
        import os
        os.system("pip install pyperclip")
        import pyperclip
    
    # Créer et lancer l'interface
    root = tk.Tk()
    app = AddonsApp(root)
    root.mainloop()