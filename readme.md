# Knight Tarot Card Draw

![Knight Tarot Card Draw](knight_tarot.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Data Format](#data-format)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Saving and Loading Characters](#saving-and-loading-characters)
- [Exporting to PDF](#exporting-to-pdf)
- [Help](#help)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

**Knight Tarot Card Draw** is a user-friendly desktop application designed to help users create and manage their Knight characters using Tarot cards. Whether you're a game master, writer, or enthusiast, this tool simplifies the process of generating character traits, advantages, and disadvantages through a randomized Tarot card draw.

Built with Python's Tkinter for the graphical user interface (GUI) and ReportLab for PDF generation, this application ensures an interactive and seamless experience for users with no prior programming knowledge.

## Features

- **Random Tarot Card Draw**: Selects 5 random Tarot cards to define your character's traits.
- **Interactive GUI**: Easy-to-use interface built with Tkinter.
- **Detailed Card Information**: View comprehensive details for each drawn Tarot card.
- **Save and Load Characters**: Store your character data in JSON files and retrieve them later.
- **Export to PDF**: Generate a PDF document of your character sheet for easy sharing or printing.
- **Help Section**: Access a user guide directly within the application.

## Data Format

The application relies on a `tarot_cards.json` file that contains the details of each Tarot card. Each card is represented as a JSON object with the following structure:

```json
{
    "name": "The Magician",
    "past": "Youthful apprenticeship, natural talent that has borne fruit, a spontaneous decision that led to good results, a sudden and unfortunate choice, a childhood rich with opportunity, a change of lifestyle, a change of profession, a rebirth.",
    "bonus": "The PC adds 1 point to their Lady aspect, and 3 points to allocate as they choose to characteristics linked to this aspect.",
    "advantage": "Tireless: The character's body is naturally more resistant to trauma and fatigue inflicted by blows to their meta-armour. The usual loss of health points when their armour is damaged does not apply (ignore the 1 HP loss for every 5 AP damaged rule).",
    "disadvantage": "Wrathful: The character suffers from piques of anger when in stress-inducing situations (heated debate, failure, witnessing things they cannot stand, and the like). This anger can swiftly manifest as fits of uncontrollable rage. The character's Composure tests when trying to calm down or not give in to angry impulses suffer a 3-die penalty."
}
```

Ensure that your `tarot_cards.json` file follows this structure and is placed in the same directory as the `knight_tarot_card_draw.py` script.

## Installation

### Prerequisites

- **Python 3.x**: Ensure that Python is installed on your system. You can download it from the [official website](https://www.python.org/downloads/).
- **Pip**: Python's package installer should be included with your Python installation.

### Required Python Libraries

Install the necessary Python libraries using `pip`:

```bash
pip install reportlab
```

*Note*: `tkinter` is included with most Python installations. If you encounter issues, refer to the [Tkinter Installation Guide](https://docs.python.org/3/library/tkinter.html#module-tkinter).

### Setup Steps

1. **Clone the Repository** *(if applicable)*:
    ```bash
    git clone https://github.com/yourusername/knight_tarot_card_draw.git
    cd knight_tarot_card_draw
    ```

2. **Download the Data File**:
    - Ensure that the `tarot_cards.json` file is present in the project directory.
    - Use the provided sample or create your own following the specified format.

3. **Prepare Icon Files** *(Optional)*:
    - The application uses `knight_tarot.ico` for Windows and `knight_tarot.png` for macOS/Linux.
    - Place these icon files in the project directory. If not available, the app will use default icons.

## Usage

1. **Run the Application**:
    ```bash
    python knight_tarot_card_draw.py
    ```

2. **Main Interface**:
    - **Character Name**: Enter your character's name in the "Character Name" field.
    - **Draw Cards**: Click the "Draw Cards" button to randomly select 5 Tarot cards.
    - **Select Traits**:
        - **Past**: Choose one card from the drawn list.
        - **Bonus**: Assign a bonus based on the selected card.
        - **Advantage 1 & 2**: Select two advantages.
        - **Disadvantage**: Choose one disadvantage.
    - **Save Character**: Click "Save Character" to store your selections in a JSON file.
    - **Load Character**: Click "Load Character" to retrieve previously saved data.
    - **Export to PDF**: Generate a PDF of your character sheet by clicking "Export to PDF".
    - **Help**: Access the user guide by clicking the "Help" button.

## How It Works

### Overview

The application is structured using object-oriented programming principles with three main classes:

1. **Card**: Represents a Tarot card with its associated traits.
2. **HelpWindow**: Creates a separate window displaying the user guide.
3. **TarotCardDraw**: Manages the core functionality, including the GUI, card drawing, saving/loading data, and PDF exporting.

### Key Components

- **Resource Path Function**:
    ```python
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    ```
    - Ensures the application can locate resource files whether running in development or as a bundled executable.

- **Card Class**:
    ```python
    class Card:
        def __init__(self, name, past, bonus, advantage, disadvantage):
            self.name = name
            self.past = past
            self.bonus = bonus
            self.advantage = advantage
            self.disadvantage = disadvantage
    ```
    - Encapsulates the properties of a Tarot card.

- **HelpWindow Class**:
    ```python
    class HelpWindow:
        def __init__(self, master):
            self.window = tk.Toplevel(master)
            self.window.title("Knight Tarot Card Draw - Help")
            self.window.geometry("600x400")
            # Additional setup...
    ```
    - Creates a separate window with user instructions.

- **TarotCardDraw Class**:
    - Handles loading cards, setting up the GUI, managing user interactions, and exporting data.

## Saving and Loading Characters

### Saving a Character

1. **Enter Character Details**:
    - Fill in the "Character Name" and select the desired cards for each trait.
2. **Save**:
    - Click the "Save Character" button.
    - Choose a location and filename for the JSON file.
    - The character data will be saved in the specified JSON format.

### Loading a Character

1. **Load**:
    - Click the "Load Character" button.
    - Select the previously saved JSON file.
    - The application will populate the fields with the loaded data.

## Exporting to PDF

1. **Complete Selections**:
    - Ensure all fields (Past, Bonus, Advantages, Disadvantage) are selected.
2. **Export**:
    - Click the "Export to PDF" button.
    - Choose the destination and filename for the PDF.
    - The application generates a PDF with all selected traits and their details.

*Sample PDF Output*:

```
Character: [Character Name]

Past:
[Past Card Name]: [Past Description]

Bonus:
[Bonus Card Name]: [Bonus Description]

Advantage 1:
[Advantage 1 Card Name]: [Advantage 1 Description]

Advantage 2:
[Advantage 2 Card Name]: [Advantage 2 Description]

Disadvantage:
[Disadvantage Card Name]: [Disadvantage Description]
```

## Help

Access the user guide directly within the application:

1. Click the "Help" button located on the left panel.
2. A new window will open displaying detailed instructions on how to use each feature of the application.

## Contributing

Contributions are welcome! If you have suggestions for improvements or encounter any issues, please feel free to open an issue or submit a pull request.

### Steps to Contribute

1. **Fork the Repository**: Click the "Fork" button at the top right of the repository page.
2. **Clone Your Fork**:
    ```bash
    git clone https://github.com/yourusername/knight_tarot_card_draw.git
    ```
3. **Create a New Branch**:
    ```bash
    git checkout -b feature/YourFeatureName
    ```
4. **Make Your Changes**.
5. **Commit Your Changes**:
    ```bash
    git commit -m "Add your message here"
    ```
6. **Push to Your Fork**:
    ```bash
    git push origin feature/YourFeatureName
    ```
7. **Open a Pull Request**: Navigate to the original repository and click "Compare & pull request".

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

For any questions or feedback, please contact [your-email@example.com](mailto:your-email@example.com).

---

*Happy Tarot Drawing! 🃏✨*