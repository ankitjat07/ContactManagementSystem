
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "contacts.json")


class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("1000x650")
        self.root.minsize(800, 550)
        self.root.configure(bg="#F1F5F9")

        self.contacts = self.load_contacts()
        self.selected_phone = None

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.setup_style()
        self.build_ui()
        self.refresh_table()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="white",
            foreground="#1E293B",
            rowheight=32,
            fieldbackground="white",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#E2E8F0",
            foreground="#0F172A",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )
        style.map("Treeview", background=[("selected", "#BFDBFE")])

    def load_contacts(self):
        if not os.path.exists(FILE_NAME):
            return []

        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            messagebox.showerror(
                "File Error",
                "Could not read contacts.json. Check the file."
            )
            return []

    def save_contacts(self):
        try:
            with open(FILE_NAME, "w", encoding="utf-8") as file:
                json.dump(self.contacts, file, indent=4, ensure_ascii=False)
            return True
        except OSError as error:
            messagebox.showerror("Save Error", str(error))
            return False

    def build_ui(self):
        header = tk.Frame(self.root, bg="#172554", padx=24, pady=18)
        header.pack(fill="x")

        tk.Label(
            header, text="CONTACT MANAGER",
            font=("Segoe UI", 22, "bold"),
            bg="#172554", fg="white"
        ).pack(anchor="w")

        tk.Label(
            header, text="Manage your contacts in one place",
            font=("Segoe UI", 10),
            bg="#172554", fg="#BFDBFE"
        ).pack(anchor="w", pady=(4, 0))

        body = tk.Frame(self.root, bg="#F1F5F9", padx=20, pady=16)
        body.pack(fill="both", expand=True)

        form = tk.LabelFrame(
            body, text=" Contact Details ",
            font=("Segoe UI", 11, "bold"),
            bg="white", fg="#0F172A", padx=14, pady=12
        )
        form.pack(fill="x", pady=(0, 14))

        fields = [
            ("Full Name", self.name_var),
            ("Phone Number", self.phone_var),
            ("Email Address", self.email_var),
            ("Address", self.address_var)
        ]

        for index, (label, variable) in enumerate(fields):
            row, col = divmod(index, 2)
            x = 10 + col * 470

            tk.Label(
                form, text=label, bg="white",
                fg="#475569", font=("Segoe UI", 9)
            ).grid(row=row * 2, column=col, sticky="w",
                   padx=(x, 15), pady=(4, 2))

            entry = ttk.Entry(form, textvariable=variable, width=42)
            entry.grid(row=row * 2 + 1, column=col, sticky="ew",
                       padx=(x, 15), pady=(0, 8), ipady=5)

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        buttons = tk.Frame(form, bg="white")
        buttons.grid(row=4, column=0, columnspan=2,
                     sticky="w", padx=10, pady=(4, 0))

        self.make_button(buttons, "Add Contact", "#2563EB",
                         self.add_contact).pack(side="left", padx=(0, 8))
        self.make_button(buttons, "Update Selected", "#0F766E",
                         self.update_contact).pack(side="left", padx=8)
        self.make_button(buttons, "Delete Selected", "#DC2626",
                         self.delete_contact).pack(side="left", padx=8)
        self.make_button(buttons, "Clear Form", "#64748B",
                         self.clear_form).pack(side="left", padx=8)

        search_frame = tk.Frame(body, bg="#F1F5F9")
        search_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            search_frame, text="Saved Contacts",
            font=("Segoe UI", 13, "bold"),
            bg="#F1F5F9", fg="#0F172A"
        ).pack(side="left")

        ttk.Entry(
            search_frame, textvariable=self.search_var, width=28
        ).pack(side="right", padx=(8, 0), ipady=4)

        tk.Button(
            search_frame, text="Search",
            command=self.search_contacts,
            bg="#2563EB", fg="white",
            activebackground="#1D4ED8",
            activeforeground="white", relief="flat",
            padx=12, pady=5, cursor="hand2"
        ).pack(side="right")

        tk.Button(
            search_frame, text="Show All",
            command=self.refresh_table,
            bg="#E2E8F0", fg="#0F172A",
            relief="flat", padx=10, pady=5, cursor="hand2"
        ).pack(side="right", padx=6)

        table_frame = tk.Frame(body, bg="white")
        table_frame.pack(fill="both", expand=True)

        columns = ("name", "phone", "email", "address")
        self.table = ttk.Treeview(
            table_frame, columns=columns,
            show="headings", selectmode="browse"
        )

        headings = {
            "name": ("Name", 170),
            "phone": ("Phone", 125),
            "email": ("Email", 210),
            "address": ("Address", 230)
        }

        for column, (heading, width) in headings.items():
            self.table.heading(column, text=heading)
            self.table.column(column, width=width, minwidth=80)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.table.bind("<<TreeviewSelect>>", self.select_contact)

        self.status = tk.Label(
            body, text="", bg="#F1F5F9",
            fg="#475569", anchor="w", font=("Segoe UI", 9)
        )
        self.status.pack(fill="x", pady=(8, 0))

    def make_button(self, parent, text, color, command):
        return tk.Button(
            parent, text=text, command=command,
            bg=color, fg="white", activebackground=color,
            activeforeground="white", relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=12, pady=8, cursor="hand2"
        )

    def clear_form(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        self.selected_phone = None
        for item in self.table.selection():
            self.table.selection_remove(item)

    def refresh_table(self):
        self.search_var.set("")
        self.populate_table(self.contacts)

    def populate_table(self, contacts):
        for item in self.table.get_children():
            self.table.delete(item)

        for contact in contacts:
            self.table.insert("", "end", values=(
                contact.get("name", ""),
                contact.get("phone", ""),
                contact.get("email", ""),
                contact.get("address", "")
            ))

        self.status.config(
            text=f"Total contacts: {len(self.contacts)}"
                 f"    |    Showing: {len(contacts)}"
        )

    def search_contacts(self):
        query = self.search_var.get().strip().lower()

        if not query:
            self.populate_table(self.contacts)
            return

        results = [
            c for c in self.contacts
            if query in c.get("name", "").lower()
            or query in c.get("phone", "").lower()
            or query in c.get("email", "").lower()
        ]
        self.populate_table(results)

    def validate_form(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()

        if not name or not phone:
            messagebox.showwarning(
                "Missing Details", "Name and phone number are required."
            )
            return False

        if not phone.isdigit() or not 7 <= len(phone) <= 15:
            messagebox.showwarning(
                "Invalid Phone",
                "Phone number must contain 7-15 digits."
            )
            return False

        return True

    def add_contact(self):
        if not self.validate_form():
            return

        phone = self.phone_var.get().strip()

        if any(c.get("phone") == phone for c in self.contacts):
            messagebox.showwarning(
                "Duplicate Contact", "This phone number already exists."
            )
            return

        contact = {
            "name": self.name_var.get().strip(),
            "phone": phone,
            "email": self.email_var.get().strip(),
            "address": self.address_var.get().strip()
        }

        self.contacts.append(contact)
        if self.save_contacts():
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Success", "Contact added successfully!")
        else:
            self.contacts.remove(contact)

    def select_contact(self, _event=None):
        selection = self.table.selection()
        if not selection:
            return

        values = self.table.item(selection[0], "values")
        if not values:
            return

        name, phone, email, address = values
        self.name_var.set(name)
        self.phone_var.set(phone)
        self.email_var.set(email)
        self.address_var.set(address)
        self.selected_phone = phone

    def update_contact(self):
        if not self.selected_phone:
            messagebox.showwarning(
                "Select Contact", "Select a contact from the table first."
            )
            return

        if not self.validate_form():
            return

        new_phone = self.phone_var.get().strip()

        if any(
            c.get("phone") == new_phone
            and c.get("phone") != self.selected_phone
            for c in self.contacts
        ):
            messagebox.showwarning(
                "Duplicate Contact", "This phone number already exists."
            )
            return

        contact = next(
            (c for c in self.contacts
             if c.get("phone") == self.selected_phone), None
        )

        if contact is None:
            messagebox.showerror("Error", "Contact not found.")
            return

        old_contact = contact.copy()
        contact.update({
            "name": self.name_var.get().strip(),
            "phone": new_phone,
            "email": self.email_var.get().strip(),
            "address": self.address_var.get().strip()
        })

        if self.save_contacts():
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Success", "Contact updated successfully!")
        else:
            contact.update(old_contact)

    def delete_contact(self):
        if not self.selected_phone:
            messagebox.showwarning(
                "Select Contact", "Select a contact from the table first."
            )
            return

        contact = next(
            (c for c in self.contacts
             if c.get("phone") == self.selected_phone), None
        )

        if contact is None:
            messagebox.showerror("Error", "Contact not found.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete contact '{contact['name']}'?"
        )
        if not confirm:
            return

        self.contacts.remove(contact)

        if self.save_contacts():
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Success", "Contact deleted successfully!")
        else:
            self.contacts.append(contact)


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
