#!/usr/bin/python3
#-*-Coding:utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire Financier Personnel")
        self.user_id = None

        self.username_label = tk.Label(root, text="Nom d'utilisateur")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Mot de passe")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Connexion", command=self.login)
        self.login_button.pack()

        self.create_account_button = tk.Button(root, text="Créer un compte", command=self.create_account)
        self.create_account_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.user_id = user[0]
            self.show_dashboard()
        else:
            messagebox.showerror("Erreur d'authentification", "Nom d'utilisateur ou mot de passe incorrect")

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Erreur de création de compte", "Ce nom d'utilisateur existe déjà.")
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Création de compte réussie", "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.")

    def show_dashboard(self):
        self.username_label.destroy()
        self.username_entry.destroy()
        self.password_label.destroy()
        self.password_entry.destroy()
        self.login_button.destroy()
        self.create_account_button.destroy()

        dashboard = Dashboard(self.root, self.user_id)

class Dashboard:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.income_frame = tk.Frame(self.notebook)
        self.expenses_frame = tk.Frame(self.notebook)
        self.report_frame = tk.Frame(self.notebook)

        self.notebook.add(self.income_frame, text="Revenus")
        self.notebook.add(self.expenses_frame, text="Dépenses")
        self.notebook.add(self.report_frame, text="Rapports")

        # Widgets pour la gestion des revenus
        self.income_amount_label = tk.Label(self.income_frame, text="Montant")
        self.income_amount_label.pack()
        self.income_amount_entry = tk.Entry(self.income_frame)
        self.income_amount_entry.pack()

        self.income_category_label = tk.Label(self.income_frame, text="Catégorie")
        self.income_category_label.pack()
        self.income_category_entry = tk.Entry(self.income_frame)
        self.income_category_entry.pack()

        self.income_description_label = tk.Label(self.income_frame, text="Description")
        self.income_description_label.pack()
        self.income_description_entry = tk.Entry(self.income_frame)
        self.income_description_entry.pack()

        self.income_date_label = tk.Label(self.income_frame, text="Date")
        self.income_date_label.pack()
        self.income_date_entry = tk.Entry(self.income_frame)
        self.income_date_entry.pack()

        self.income_button = tk.Button(self.income_frame, text="Ajouter Revenu", command=self.add_income)
        self.income_button.pack()

        # Widgets pour la gestion des dépenses
        self.expenses_amount_label = tk.Label(self.expenses_frame, text="Montant")
        self.expenses_amount_label.pack()
        self.expenses_amount_entry = tk.Entry(self.expenses_frame)
        self.expenses_amount_entry.pack()

        self.expenses_category_label = tk.Label(self.expenses_frame, text="Catégorie")
        self.expenses_category_label.pack()
        self.expenses_category_entry = tk.Entry(self.expenses_frame)
        self.expenses_category_entry.pack()

        self.expenses_description_label = tk.Label(self.expenses_frame, text="Description")
        self.expenses_description_label.pack()
        self.expenses_description_entry = tk.Entry(self.expenses_frame)
        self.expenses_description_entry.pack()

        self.expenses_date_label = tk.Label(self.expenses_frame, text="Date")
        self.expenses_date_label.pack()
        self.expenses_date_entry = tk.Entry(self.expenses_frame)
        self.expenses_date_entry.pack()

        self.expenses_button = tk.Button(self.expenses_frame, text="Ajouter Dépense", command=self.add_expense)
        self.expenses_button.pack()

        # Widgets pour la génération de rapports
        self.report_text = scrolledtext.ScrolledText(self.report_frame, wrap=tk.WORD)
        self.report_text.pack()
        self.generate_report_button = tk.Button(self.report_frame, text="Générer Rapport", command=self.generate_report)
        self.generate_report_button.pack()

    def add_income(self):
        amount = float(self.income_amount_entry.get())
        category = self.income_category_entry.get()
        description = self.income_description_entry.get()
        date = self.income_date_entry.get()

        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO income (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
                       (self.user_id, amount, category, date, description))
        conn.commit()
        conn.close()

        self.income_amount_entry.delete(0, tk.END)
        self.income_category_entry.delete(0, tk.END)
        self.income_description_entry.delete(0, tk.END)
        self.income_date_entry.delete(0, tk.END)

    def add_expense(self):
        amount = float(self.expenses_amount_entry.get())
        category = self.expenses_category_entry.get()
        description = self.expenses_description_entry.get()
        date = self.expenses_date_entry.get()

        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
                       (self.user_id, amount, category, date, description))
        conn.commit()
        conn.close()

        self.expenses_amount_entry.delete(0, tk.END)
        self.expenses_category_entry.delete(0, tk.END)
        self.expenses_description_entry.delete(0, tk.END)
        self.expenses_date_entry.delete(0, tk.END)

    def generate_report(self):
        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()

        cursor.execute('SELECT SUM(amount) FROM income WHERE user_id = ?', (self.user_id,))
        total_income = cursor.fetchone()[0]

        cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ?', (self.user_id,))
        total_expense = cursor.fetchone()[0]

        conn.close()

        balance = total_income - total_expense

        report = "Rapport Financier\n"
        report += f"Total des Revenus : {total_income} EUR\n"
        report += f"Total des Dépenses : {total_expense} EUR\n"
        report += f"Solde : {balance} EUR\n"

        report += "\nDétail des Revenus :\n"
        report += self.get_income_details()

        report += "\nDétail des Dépenses :\n"
        report += self.get_expense_details()

        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report)

    def get_income_details(self):
        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()

        cursor.execute('SELECT category, amount, date, description FROM income WHERE user_id = ?', (self.user_id,))
        income_details = cursor.fetchall()

        conn.close()

        details = ""
        for row in income_details:
            category, amount, date, description = row
            details += f"Catégorie : {category}, Montant : {amount} EUR, Date : {date}, Description : {description}\n"

        return details

    def get_expense_details(self):
        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()

        cursor.execute('SELECT category, amount, date, description FROM expenses WHERE user_id = ?', (self.user_id,))
        expense_details = cursor.fetchall()

        conn.close()

        details = ""
        for row in expense_details:
            category, amount, date, description = row
            details += f"Catégorie : {category}, Montant : {amount} EUR, Date : {date}, Description : {description}\n"

        return details

def main():
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

