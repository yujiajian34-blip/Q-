import sys
from PyQt5.QtWidgets import QApplication
from pet_widget import PetWidget

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    
    pet = PetWidget()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
