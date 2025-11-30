import sys
import os

# Add the project root to the python path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ui.main_window import MainWindow

def main():
    """
    Entry point for the Airport Cost-Sharing Game application.
    """
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
