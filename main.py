
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "contacts.json"
)

BG = "#F4F6FC"
WHITE = "#FFFFFF"
NAVY = "#171C36"
NAVY_LIGHT = "#252B4B"
BLUE = "#635BFF"
BLUE_HOVER = "#5148E5"
TEXT = "#20243A"
MUTED = "#7D849D"
BORDER = "#E8EAF3"
GREEN = "#159A79"
RED = "#E05260"


class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contactly | Contact Manager")
        self.root.geometry("1280x820")
        self.root.minsize(1000, 760)
        self.root.configure(bg=BG)

        self.contacts = self.load_contacts()
        self.selected_phone = None

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.setup_styles()
        self.build_ui()
        self.refresh_table()

    def load_contacts(self):
        if not os.path.exists(FILE_NAME):
            return []

        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)
            return [item for item in data if isinstance(item, dict)] if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            messagebox.showerror(
                "File Error", "Unable to read contacts.json."
            )
            return []

    def save_contacts(self):
        try:
            with open(FILE_NAME, "w", encoding="utf-8") as file:
                json.dump(
                    self.contacts, file, indent=4, ensure_ascii=False
                )
            return True
        except OSError as error:
            messagebox.showerror("Save Error", str(error))
            return False

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Modern.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=42,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Modern.Treeview.Heading",
            background="#F0F2FA",
            foreground="#565D78",
            font=("Segoe UI", 9, "bold"),
            padding=(12, 14),
            relief="flat"
        )
        style.map(
            "Modern.Treeview",
            background=[("selected", "#E6E9FF")],
            foreground=[("selected", TEXT)]
        )
        style.configure(
            "Modern.Vertical.TScrollbar",
            background="#DDE1EF",
            troughcolor=WHITE,
            bordercolor=WHITE,
            arrowsize=12
        )

    def make_button(self, parent, text, color, command,
                    fg=WHITE, padx=16, pady=10):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=fg,
            activebackground=color,
            activeforeground=fg,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=padx,
            pady=pady,
            cursor="hand2"
        )

    def card(self, parent, padx=18, pady=16):
        return tk.Frame(
            parent,
            bg=WHITE,
            padx=padx,
            pady=pady,
            highlightbackground=BORDER,
            highlightthickness=1
        )

    def build_ui(self):
        # Sidebar
        sidebar = tk.Frame(self.root, bg=NAVY, width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg=NAVY)
        brand.pack(fill="x", padx=22, pady=(28, 36))

        tk.Label(
            brand, text="C",
            font=("Segoe UI", 22, "bold"),
            bg=BLUE, fg=WHITE, width=2, pady=2
        ).pack(side="left", padx=(0, 10))

        brand_text = tk.Frame(brand, bg=NAVY)
        brand_text.pack(side="left")

        tk.Label(
            brand_text, text="Contactly",
            font=("Segoe UI", 16, "bold"),
            bg=NAVY, fg=WHITE
        ).pack(anchor="w")

        tk.Label(
            brand_text, text="CONTACT MANAGER",
            font=("Segoe UI", 8, "bold"),
            bg=NAVY, fg="#929AB9"
        ).pack(anchor="w", pady=(2, 0))

        tk.Label(
            sidebar, text="WORKSPACE",
            font=("Segoe UI", 9, "bold"),
            bg=NAVY, fg="#929AB9"
        ).pack(anchor="w", padx=24, pady=(0, 12))

        nav = tk.Frame(sidebar, bg=NAVY_LIGHT, padx=12, pady=12)
        nav.pack(fill="x", padx=12)

        tk.Label(
            nav, text="▦",
            font=("Segoe UI", 15),
            bg=NAVY_LIGHT, fg="#AFAAFF"
        ).pack(side="left", padx=(5, 12))

        tk.Label(
            nav, text="All Contacts",
            font=("Segoe UI", 11, "bold"),
            bg=NAVY_LIGHT, fg=WHITE
        ).pack(side="left")

        tk.Label(
            sidebar, text="YOUR PERSONAL\nCONTACT SPACE",
            font=("Segoe UI", 9, "bold"),
            bg=NAVY, fg="#929AB9",
            justify="left"
        ).pack(side="bottom", anchor="w", padx=24, pady=(0, 28))

        tk.Label(
            sidebar, text="Python  •  Tkinter",
            font=("Segoe UI", 9),
            bg=NAVY, fg="#B8C0D9"
        ).pack(side="bottom", anchor="w", padx=24, pady=(0, 5))

        # Main area
        main = tk.Frame(self.root, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        header = tk.Frame(main, bg=WHITE, padx=30, pady=14)
        header.pack(fill="x")

        tk.Label(
            header, text="Good to see you!",
            font=("Segoe UI", 10),
            bg=WHITE, fg=MUTED
        ).pack(anchor="w")

        tk.Label(
            header, text="Your Contacts",
            font=("Segoe UI", 25, "bold"),
            bg=WHITE, fg=TEXT
        ).pack(anchor="w", pady=(3, 2))

        tk.Label(
            header,
            text="Everything you need to manage your connections.",
            font=("Segoe UI", 10),
            bg=WHITE, fg=MUTED
        ).pack(anchor="w")

        content = tk.Frame(main, bg=BG, padx=22, pady=14)
        content.pack(fill="both", expand=True)

        # Statistics cards
        stats = tk.Frame(content, bg=BG)
        stats.pack(fill="x", pady=(0, 18))

        self.total_var = tk.StringVar(value="0")
        self.email_var_count = tk.StringVar(value="0")
        self.selection_var = tk.StringVar(value="Ready to manage contacts")

        self.stat_card(
            stats, "TOTAL CONTACTS", self.total_var,
            "People saved in your list", BLUE, "01"
        ).pack(side="left", fill="x", expand=True, padx=(0, 9))

        self.stat_card(
            stats, "EMAIL ADDRESSES", self.email_var_count,
            "Contacts with an email", GREEN, "02"
        ).pack(side="left", fill="x", expand=True, padx=(9, 0))

        # Contact form
        form = self.card(content, 20, 12)
        form.pack(fill="x", pady=(0, 18))

        form_header = tk.Frame(form, bg=WHITE)
        form_header.pack(fill="x", pady=(0, 10))

        tk.Label(
            form_header, text="Contact Information",
            font=("Segoe UI", 14, "bold"),
            bg=WHITE, fg=TEXT
        ).pack(side="left")

        tk.Label(
            form_header, text="* Required fields",
            font=("Segoe UI", 9),
            bg=WHITE, fg=MUTED
        ).pack(side="right")

        # Use a separate frame for grid-managed fields.
        # Tkinter cannot mix pack and grid inside the same parent.
        fields_frame = tk.Frame(form, bg=WHITE)
        fields_frame.pack(fill="x")

        self.add_field(
            fields_frame, "Full Name *", self.name_var, 0, 0
        )
        self.add_field(
            fields_frame, "Phone Number *", self.phone_var, 0, 1
        )
        self.add_field(
            fields_frame, "Email Address", self.email_var, 2, 0
        )
        self.add_field(
            fields_frame, "Address", self.address_var, 2, 1
        )

        fields_frame.columnconfigure(0, weight=1, uniform="form")
        fields_frame.columnconfigure(1, weight=1, uniform="form")

        # Buttons use pack inside their own child frame.
        actions = tk.Frame(form, bg=WHITE)
        actions.pack(fill="x", pady=(6, 0))

        self.make_button(
            actions, "+  Add Contact", BLUE, self.add_contact
        ).pack(side="left", padx=(0, 8))

        self.make_button(
            actions, "Update", GREEN, self.update_contact
        ).pack(side="left", padx=4)

        self.make_button(
            actions, "Delete", RED, self.delete_contact
        ).pack(side="left", padx=4)

        self.make_button(
            actions, "Clear Form", "#EDF0F8", self.clear_form,
            fg=TEXT
        ).pack(side="left", padx=4)

        # Contact list
        list_card = self.card(content, 0, 0)
        list_card.pack(fill="both", expand=True)

        list_header = tk.Frame(list_card, bg=WHITE, padx=18, pady=16)
        list_header.pack(fill="x")

        title_area = tk.Frame(list_header, bg=WHITE)
        title_area.pack(side="left")

        tk.Label(
            title_area, text="Saved Contacts",
            font=("Segoe UI", 14, "bold"),
            bg=WHITE, fg=TEXT
        ).pack(anchor="w")

        tk.Label(
            title_area, text="Select a row to edit or delete",
            font=("Segoe UI", 9),
            bg=WHITE, fg=MUTED
        ).pack(anchor="w", pady=(3, 0))

        search_area = tk.Frame(list_header, bg=WHITE)
        search_area.pack(side="right")

        search_entry = ttk.Entry(
            search_area, textvariable=self.search_var, width=23
        )
        search_entry.pack(side="left", ipady=6, padx=(0, 7))
        search_entry.bind(
            "<Return>", lambda _event: self.search_contacts()
        )

        self.make_button(
            search_area, "Search", BLUE, self.search_contacts,
            padx=12, pady=8
        ).pack(side="left", padx=(0, 5))

        self.make_button(
            search_area, "All", "#EDF0F8", self.refresh_table,
            fg=TEXT, padx=12, pady=8
        ).pack(side="left")

        separator = tk.Frame(list_card, bg=BORDER, height=1)
        separator.pack(fill="x")

        table_frame = tk.Frame(list_card, bg=WHITE)
        table_frame.pack(fill="both", expand=True, padx=14, pady=8)

        columns = ("name", "phone", "email", "address")
        self.table = ttk.Treeview(
            table_frame, columns=columns,
            show="headings", selectmode="browse", height=8,
            style="Modern.Treeview"
        )

        for key, label, width in [
            ("name", "NAME", 155),
            ("phone", "PHONE", 125),
            ("email", "EMAIL ADDRESS", 190),
            ("address", "ADDRESS", 175)
        ]:
            self.table.heading(key, text=label)
            self.table.column(key, width=width, minwidth=70)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical",
            command=self.table.yview,
            style="Modern.Vertical.TScrollbar"
        )
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.table.bind("<<TreeviewSelect>>", self.select_contact)

        footer = tk.Frame(list_card, bg="#F8F9FD", padx=18, pady=11)
        footer.pack(fill="x")

        tk.Label(
            footer, textvariable=self.selection_var,
            font=("Segoe UI", 9),
            bg="#F8F9FD", fg=MUTED
        ).pack(side="left")

        tk.Label(
            footer, text="LOCAL JSON STORAGE",
            font=("Segoe UI", 8, "bold"),
            bg="#F8F9FD", fg="#8A90A8"
        ).pack(side="right")

    def stat_card(self, parent, title, variable, subtitle, accent, number):
        card = self.card(parent, 18, 14)

        top = tk.Frame(card, bg=WHITE)
        top.pack(fill="x")

        tk.Label(
            top, text=title,
            font=("Segoe UI", 9, "bold"),
            bg=WHITE, fg=MUTED
        ).pack(side="left")

        tk.Label(
            top, text=number,
            font=("Segoe UI", 9, "bold"),
            bg="#F0EFFF", fg=accent,
            padx=8, pady=4
        ).pack(side="right")

        tk.Label(
            card, textvariable=variable,
            font=("Segoe UI", 26, "bold"),
            bg=WHITE, fg=TEXT
        ).pack(anchor="w", pady=(7, 0))

        tk.Label(
            card, text=subtitle,
            font=("Segoe UI", 9),
            bg=WHITE, fg=MUTED
        ).pack(anchor="w", pady=(2, 0))

        return card

    def add_field(self, parent, label, variable, row, col):
        field = tk.Frame(parent, bg=WHITE)
        field.grid(
            row=row, column=col, sticky="ew",
            padx=(0, 18 if col == 0 else 0),
            pady=(0, 10)
        )

        tk.Label(
            field, text=label,
            font=("Segoe UI", 9, "bold"),
            bg=WHITE, fg="#505770"
        ).pack(anchor="w", pady=(0, 6))

        entry = ttk.Entry(field, textvariable=variable)
        entry.pack(fill="x", ipady=7)

    def clear_form(self):
        for variable in (
            self.name_var, self.phone_var,
            self.email_var, self.address_var
        ):
            variable.set("")

        self.selected_phone = None

        for item in self.table.selection():
            self.table.selection_remove(item)

        self.selection_var.set("Form cleared")

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

        self.total_var.set(str(len(self.contacts)))
        self.email_var_count.set(
            str(sum(bool(str(c.get("email", "")).strip())
                    for c in self.contacts))
        )

        self.selection_var.set(
            f"Showing {len(contacts)} of {len(self.contacts)} contacts"
        )

    def search_contacts(self):
        query = self.search_var.get().strip().lower()

        if not query:
            self.populate_table(self.contacts)
            return

        results = [
            c for c in self.contacts
            if query in str(c.get("name", "")).lower()
            or query in str(c.get("phone", "")).lower()
            or query in str(c.get("email", "")).lower()
            or query in str(c.get("address", "")).lower()
        ]

        self.populate_table(results)
        if not results:
            self.selection_var.set("No matching contacts found")

    def validate_form(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()

        if not name or not phone:
            messagebox.showwarning(
                "Required Fields", "Name and phone number are required."
            )
            return False

        if not phone.isdigit() or not 7 <= len(phone) <= 15:
            messagebox.showwarning(
                "Invalid Phone", "Enter a phone number with 7-15 digits."
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
            self.selection_var.set("Contact added successfully")
        else:
            self.contacts.remove(contact)

    def select_contact(self, _event=None):
        selected = self.table.selection()
        if not selected:
            return

        values = self.table.item(selected[0], "values")
        if not values:
            return

        name, phone, email, address = values
        self.name_var.set(name)
        self.phone_var.set(phone)
        self.email_var.set(email)
        self.address_var.set(address)
        self.selected_phone = phone
        self.selection_var.set(f"Selected: {name}")

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

        old = contact.copy()
        contact.update({
            "name": self.name_var.get().strip(),
            "phone": new_phone,
            "email": self.email_var.get().strip(),
            "address": self.address_var.get().strip()
        })

        if self.save_contacts():
            self.refresh_table()
            self.clear_form()
            self.selection_var.set("Contact updated successfully")
        else:
            contact.update(old)

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

        if not messagebox.askyesno(
            "Confirm Delete", f"Delete '{contact['name']}'?"
        ):
            return

        self.contacts.remove(contact)

        if self.save_contacts():
            self.refresh_table()
            self.clear_form()
            self.selection_var.set("Contact deleted successfully")
        else:
            self.contacts.append(contact)


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
