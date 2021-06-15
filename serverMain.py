import sys
import socket
import threading
from PySide6.QtWidgets import QApplication, QPushButton, QDialog, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from serverSocket import ServerSocket


class ServerUI(QDialog):

    def __init__(self, parent=None):
        super(ServerUI, self).__init__(parent)
        self.setWindowTitle("Server")
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 3458
        self.serverSocket = ServerSocket()
        self.setupStartUi()

    def setupStartUi(self):
        self.hostLabel = QLabel("Host")
        self.hostEdit = QLineEdit(f"{self.HOST}")
        self.hostLayout = QHBoxLayout()
        self.hostLayout.addWidget(self.hostLabel)
        self.hostLayout.addWidget(self.hostEdit)

        self.portLabel = QLabel("Port ")
        self.portEdit = QLineEdit(f"{self.PORT}")
        self.portLayout = QHBoxLayout()
        self.portLayout.addWidget(self.portLabel)
        self.portLayout.addWidget(self.portEdit)

        self.startButton = QPushButton("Start Server")
        self.startButton.clicked.connect(self.handleStart)

        
        self.mainLayout.addLayout(self.hostLayout)
        self.mainLayout.addLayout(self.portLayout)
        self.mainLayout.addWidget(self.startButton)

    def setupRunningUi(self):
        self.messageLabel = QLabel(f"Server started on: {self.HOST}:{self.PORT}")

        self.stopButton = QPushButton("Stop Server")
        self.stopButton.clicked.connect(self.handleStop)

        self.mainLayout.addWidget(self.messageLabel)
        self.mainLayout.addWidget(self.stopButton)

    def handleStop(self):
        self.serverSocket.close()
        self.clearLayout(self.mainLayout)
        self.setupStartUi()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def handleStart(self):
        self.HOST = self.hostEdit.text()
        self.PORT = int(self.portEdit.text())
        thread = threading.Thread(target=self.serverSocket.start_server, args=(self.HOST, self.PORT))
        thread.start()
        self.clearLayout(self.mainLayout)
        self.setupRunningUi()
    
    def closeEvent(self, event):
        self.serverSocket.close()
        event.accept()


if __name__=='__main__':
    app = QApplication(sys.argv)

    server_ui = ServerUI()
    with open("Combinear.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    server_ui.show()

    sys.exit(app.exec())