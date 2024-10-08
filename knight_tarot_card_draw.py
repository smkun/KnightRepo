import random
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
import sys
import os
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Card:
    def __init__(self, name, past, bonus, advantage, disadvantage):
        self.name = name
        self.past = past
        self.bonus = bonus
        self.advantage = advantage
        self.disadvantage = disadvantage

class HelpWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Knight Tarot Card Draw - Help")
        self.window.geometry("600x400")

        self.text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD)
        self.text.pack(expand=True, fill='both', padx=10, pady=10)

        self.text.insert(tk.END, """
Knight Tarot Card Draw - User Guide

1. Drawing Cards:
   - Enter your character's name in the "Character Name" field.
   - Click "Draw Cards" to randomly select 5 tarot cards.

2. Selecting Cards:
   - Choose one card each for Past, Bonus, Disadvantage, and two for Advantages.
   - Use the dropdown menus to make your selections.

3. Viewing Card Details:
   - Click on a card in the "Drawn Cards" list to view its full details.

4. Saving Character:
   - After making your selections, click "Save Character" to store your choices.
   - Your character will be saved as a JSON file.

5. Loading Character:
   - Click "Load Character" to retrieve a previously saved character.
   - Select the JSON file when prompted.

6. Exporting to PDF:
   - Click "Export to PDF" to create a PDF of your character sheet.
   - The PDF will include all your selected cards and their details.

Remember, you can always draw new cards if you're not satisfied with your initial draw. Have fun creating your Knight character!
        """)
        self.text.config(state=tk.DISABLED)
class TarotCardDraw:
    def __init__(self, master):
        self.master = master
        self.master.title("Knight Tarot Card Draw")
        self.master.geometry("1200x800")

        # Set the window icon
        if sys.platform.startswith('win'):
            self.master.iconbitmap(resource_path('knight_tarot.ico'))
        elif sys.platform.startswith('darwin'):  # macOS
            img = tk.Image("photo", file=resource_path('knight_tarot.png'))
            self.master.tk.call('wm', 'iconphoto', self.master._w, img)
        else:  # Linux and other platforms
            img = tk.PhotoImage(file=resource_path('knight_tarot.png'))
            self.master.tk.call('wm', 'iconphoto', self.master._w, img)

        self.cards = self.load_cards()
        self.drawn_cards = []
        self.selected_past = None
        self.selected_bonus = None
        self.selected_advantages = []
        self.selected_disadvantage = None

        self.create_widgets()

    def load_cards(self):
        with open(resource_path('tarot_cards.json'), 'r') as f:
            card_data = json.load(f)
        return [Card(**card) for card in card_data]

    def create_widgets(self):
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Add Help button
        self.help_button = ttk.Button(left_frame, text="Help", command=self.show_help)
        self.help_button.pack(pady=5)

        # Character Name
        ttk.Label(left_frame, text="Character Name:").pack(anchor='w')
        self.character_name = ttk.Entry(left_frame, width=30)
        self.character_name.pack(fill=tk.X, pady=(0, 10))

        # Buttons frame
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.pack(fill=tk.X, pady=10)

        self.draw_button = ttk.Button(buttons_frame, text="Draw Cards", command=self.draw_cards)
        self.draw_button.pack(side=tk.LEFT, padx=(0, 5))

        self.save_button = ttk.Button(buttons_frame, text="Save Character", command=self.save_character)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.load_button = ttk.Button(buttons_frame, text="Load Character", command=self.load_character)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.card_frame = ttk.Frame(left_frame)
        self.card_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.past_var = tk.StringVar()
        self.bonus_var = tk.StringVar()
        self.adv1_var = tk.StringVar()
        self.adv2_var = tk.StringVar()
        self.disadv_var = tk.StringVar()

        ttk.Label(self.card_frame, text="Past:").grid(row=0, column=0, sticky="w")
        self.past_menu = ttk.Combobox(self.card_frame, textvariable=self.past_var, state="readonly", width=30)
        self.past_menu.grid(row=0, column=1, pady=5)

        ttk.Label(self.card_frame, text="Bonus:").grid(row=1, column=0, sticky="w")
        self.bonus_menu = ttk.Combobox(self.card_frame, textvariable=self.bonus_var, state="readonly", width=30)
        self.bonus_menu.grid(row=1, column=1, pady=5)

        ttk.Label(self.card_frame, text="Advantage 1:").grid(row=2, column=0, sticky="w")
        self.adv1_menu = ttk.Combobox(self.card_frame, textvariable=self.adv1_var, state="readonly", width=30)
        self.adv1_menu.grid(row=2, column=1, pady=5)
        self.adv1_menu.bind("<<ComboboxSelected>>", self.update_adv2_menu)

        ttk.Label(self.card_frame, text="Advantage 2:").grid(row=3, column=0, sticky="w")
        self.adv2_menu = ttk.Combobox(self.card_frame, textvariable=self.adv2_var, state="readonly", width=30)
        self.adv2_menu.grid(row=3, column=1, pady=5)
        self.adv2_menu.bind("<<ComboboxSelected>>", self.update_adv1_menu)

        ttk.Label(self.card_frame, text="Disadvantage:").grid(row=4, column=0, sticky="w")
        self.disadv_menu = ttk.Combobox(self.card_frame, textvariable=self.disadv_var, state="readonly", width=30)
        self.disadv_menu.grid(row=4, column=1, pady=5)

        self.export_button = ttk.Button(left_frame, text="Export to PDF", command=self.export_to_pdf)
        self.export_button.pack(pady=10)

        # Drawn Cards List
        ttk.Label(right_frame, text="Drawn Cards:").pack(anchor='w')
        self.drawn_cards_list = tk.Listbox(right_frame, width=30, height=5)
        self.drawn_cards_list.pack(fill=tk.X, pady=(0, 10))
        self.drawn_cards_list.bind('<<ListboxSelect>>', self.show_selected_card_details)

        # Card Details
        ttk.Label(right_frame, text="Card Details:").pack(anchor='w')
        self.details_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=40, height=20)
        self.details_text.pack(pady=10, fill=tk.BOTH, expand=True)

    def show_help(self):
        HelpWindow(self.master)
    def draw_cards(self):
        self.drawn_cards = random.sample(self.cards, 5)
        self.update_menus()
        self.details_text.delete('1.0', tk.END)
        self.details_text.insert(tk.END, "Cards drawn. Select a card from the 'Drawn Cards' list to see details.")

        # Update drawn cards list
        self.drawn_cards_list.delete(0, tk.END)
        for card in self.drawn_cards:
            self.drawn_cards_list.insert(tk.END, card.name)

    def update_menus(self):
        card_names = [card.name for card in self.drawn_cards]
        for menu in [self.past_menu, self.bonus_menu, self.adv1_menu, self.adv2_menu, self.disadv_menu]:
            menu['values'] = card_names
            menu.set('')

    def show_selected_card_details(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            card_name = event.widget.get(index)
            self.show_card_details(card_name)

    def show_card_details(self, card_name):
        card = next((card for card in self.drawn_cards if card.name == card_name), None)
        if card:
            details = f"Card: {card.name}\n\n"
            details += f"Past: {card.past}\n\n"
            details += f"Bonus: {card.bonus}\n\n"
            details += f"Advantage: {card.advantage}\n\n"
            details += f"Disadvantage: {card.disadvantage}\n"
            self.details_text.delete('1.0', tk.END)
            self.details_text.insert(tk.END, details)

    def update_adv1_menu(self, event):
        selected_adv2 = self.adv2_var.get()
        self.adv1_menu['values'] = [card.name for card in self.drawn_cards if card.name != selected_adv2]

    def update_adv2_menu(self, event):
        selected_adv1 = self.adv1_var.get()
        self.adv2_menu['values'] = [card.name for card in self.drawn_cards if card.name != selected_adv1]

    def export_to_pdf(self):
        if not self.character_name.get().strip():
            messagebox.showerror("Error", "Please enter a character name before exporting.")
            return

        if not all([self.past_var.get(), self.bonus_var.get(), self.adv1_var.get(), self.adv2_var.get(),
                    self.disadv_var.get()]):
            messagebox.showerror("Error", "Please select all options before exporting.")
            return

        filename = f"{self.character_name.get().strip()}_Tarot_Cards.pdf"
        # Ensure filename is valid
        filename = "".join(x for x in filename if x.isalnum() or x in ("_", "-", ".")).rstrip()

        doc = SimpleDocTemplate(filename, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

        story = []

        def add_field(title, content):
            story.append(Paragraph(f"<b>{title}</b>", styles["Heading3"]))
            story.append(Paragraph(content, styles["Justify"]))
            story.append(Spacer(1, 12))

        story.append(Paragraph(f"Character: {self.character_name.get().strip()}", styles["Title"]))
        story.append(Spacer(1, 12))

        past_card = next(card for card in self.drawn_cards if card.name == self.past_var.get())
        bonus_card = next(card for card in self.drawn_cards if card.name == self.bonus_var.get())
        adv1_card = next(card for card in self.drawn_cards if card.name == self.adv1_var.get())
        adv2_card = next(card for card in self.drawn_cards if card.name == self.adv2_var.get())
        disadv_card = next(card for card in self.drawn_cards if card.name == self.disadv_var.get())

        add_field("Past", f"{past_card.name}: {past_card.past}")
        add_field("Bonus", f"{bonus_card.name}: {bonus_card.bonus}")
        add_field("Advantage 1", f"{adv1_card.name}: {adv1_card.advantage}")
        add_field("Advantage 2", f"{adv2_card.name}: {adv2_card.advantage}")
        add_field("Disadvantage", f"{disadv_card.name}: {disadv_card.disadvantage}")

        doc.build(story)
        messagebox.showinfo("Success", f"Tarot cards exported to {filename}")

    def save_character(self):
        if not self.character_name.get().strip():
            messagebox.showerror("Error", "Please enter a character name before saving.")
            return

        if not all([self.past_var.get(), self.bonus_var.get(), self.adv1_var.get(), self.adv2_var.get(),
                    self.disadv_var.get()]):
            messagebox.showerror("Error", "Please select all options before saving.")
            return

        character_data = {
            "name": self.character_name.get().strip(),
            "past": self.past_var.get(),
            "bonus": self.bonus_var.get(),
            "advantage1": self.adv1_var.get(),
            "advantage2": self.adv2_var.get(),
            "disadvantage": self.disadv_var.get(),
            "drawn_cards": [card.name for card in self.drawn_cards]
        }

        filename = f"{self.character_name.get().strip()}_Tarot_Cards.json"
        filename = "".join(x for x in filename if x.isalnum() or x in ("_", "-", ".")).rstrip()

        with open(filename, 'w') as f:
            json.dump(character_data, f)

        messagebox.showinfo("Success", f"Character saved to {filename}")

    def load_character(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not filename:
            return

        with open(filename, 'r') as f:
            character_data = json.load(f)

        self.character_name.delete(0, tk.END)
        self.character_name.insert(0, character_data["name"])

        self.drawn_cards = [next(card for card in self.cards if card.name == name) for name in
                            character_data["drawn_cards"]]
        self.update_menus()

        self.past_var.set(character_data["past"])
        self.bonus_var.set(character_data["bonus"])
        self.adv1_var.set(character_data["advantage1"])
        self.adv2_var.set(character_data["advantage2"])
        self.disadv_var.set(character_data["disadvantage"])

        self.drawn_cards_list.delete(0, tk.END)
        for card in self.drawn_cards:
            self.drawn_cards_list.insert(tk.END, card.name)

        messagebox.showinfo("Success", f"Character loaded from {filename}")


def main():
    root = tk.Tk()
    app = TarotCardDraw(root)
    root.mainloop()


if __name__ == "__main__":
    main()