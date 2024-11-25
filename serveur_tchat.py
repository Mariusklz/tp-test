import sys
from PyQt6.QtWidgets import QApplication,QWidget,QCheckBox,QComboBox,QDateEdit,QDateTimeEdit,QDial,QDoubleSpinBox,QFontComboBox,QLCDNumber,QLabel,QLineEdit,QProgressBar,QPushButton,QRadioButton,QSlider,QSpinBox,QTimeEdit, QGridLayout, QMainWindow, QMenu, QMessageBox
from PyQt6.QtGui import QAction
import socket
import time

widgets = [
 QCheckBox,
 QComboBox,
 QDateEdit,
 QDateTimeEdit,
 QDial,
 QDoubleSpinBox,
 QFontComboBox,
 QLCDNumber,
 QLabel,
 QLineEdit,
 QProgressBar,
 QPushButton,
 QRadioButton,
 QSlider,
 QSpinBox,
 QTimeEdit,
 QGridLayout,
 ]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Taille et Titre de la fênetre
        self.setWindowTitle("Le serveur de tchat")
        self.resize(400, 400)

        # Widget central
        widget = QWidget()
        self.setCentralWidget(widget)
            
        # Création d'un layout vertical pour organiser les widgets
        grid = QGridLayout()
        grid.setSpacing(10)  # Espacement entre widgets
        grid.setContentsMargins(20, 20, 20, 20)  # Marges autour
        widget.setLayout(grid)

        #Label d'invite pour saisir l'adresse du serveur
        self.__Labelserv = QLabel("Serveur :")
        grid.addWidget(self.__Labelserv, 0, 0, 1, 2)

        #Texte pour saisir le nom
        self.__ipserv = QLineEdit("0.0.0.0")
        grid.addWidget(self.__ipserv, 0, 2, 1, 2)

        #Label d'invite pour saisir un port
        self.__Labelport = QLabel("Port :")
        grid.addWidget(self.__Labelport, 1, 0, 1, 2)

        #Texte pour afficher le port
        self.__port = QLineEdit("4200")
        grid.addWidget(self.__port , 1, 2, 1, 2)

        #Label d'invite pour saisir le nombre de clients max
        self.__Label = QLabel("Nombre de clients maximum:")
        grid.addWidget(self.__Label, 2, 0, 1, 2)

        #Texte pour saisir nombre de clients
        self.__text_input = QLineEdit("5")
        grid.addWidget(self.__text_input, 2, 2, 1, 2)


        # Création du bouton ok
        self.__bouton_demarrage_serv = QPushButton("Démarrage du serveur") # Le texte affiché sur le bouton
        grid.addWidget(self.__bouton_demarrage_serv, 3, 0, 1 ,4 )

         #Texte pour saisir le nom
        self.__message_recu = QLineEdit("")
        self.__message_recu.setReadOnly(True)
        grid.addWidget(self.__message_recu, 4, 0, 3, 4)


        # Création du bouton Quitter
        bouton_quit = QPushButton("Quitter")
        grid.addWidget(bouton_quit, 7, 0, 1, 4)

        # Connexion des actions aux boutons
        self.__bouton_demarrage_serv.clicked.connect(self.fonction__demmarrage_serv)
        bouton_quit.clicked.connect(self.__action_quit)


    # Accesseur (getter) pour récupérer le port saisi
    def get_port(self):
        return int(self.__port())

    # Accesseur (getter) pour récupérer l'ip saisi
    def get_ip(self):
        return self.__ipserv.text()
    
    # Accesseur (getter) pour récupérer le message recu par le client
    def get_message(self):
        return self.__message
    
    # Accesseur (getter) pour récupérer le port saisi
    def set_text(self, text):
        self.__message_recu.setText(text)

    # Accesseur (setter) pour récupérer le message envoyé par le client
    def __message(self):
        entered_text = self.get_message().strip()
        if entered_text:
            self.set_text(f"{entered_text}")


    # Définition des actions des boutons
    def fonction__demmarrage_serv(self):
            server_socket = socket.socket()
            print("ouverture de la socket ok")
            time.sleep(1)

            server_socket.bind(("0.0.0.0", 4200))
            print('port ouvert')
            time.sleep(1)

            server_socket.listen(1)
            print('Attente du connexion clients')
            time.sleep(1)

            conn, address = server_socket.accept()
            print("le client est connecté")
            time.sleep(1)
            
            self.__message = conn.recv(1024).decode() #1024 correspond à la taille en bytes (buffer overflow)
            print(f"Reception du message :{self.__message}")
            time.sleep(1)

            return self.__message
    
            reply = "Message bien reçu"
            conn.send(reply.encode())
            time.sleep(1)
            print("Envoi d'un message")

            conn.close()
            print("Déconnexion")

            server_socket.close
            print("Fermture du socket")

    def __action_quit(self):
        reply = QMessageBox.question(
            self,
            "Confirmer la fermeture",
            "Voulez-vous vraiment quitter ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()