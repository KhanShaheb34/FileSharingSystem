import json
import sys
import os
import socket
import ntpath
import threading
from PySide2.QtWidgets import QApplication, QPushButton, QDialog, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout, QListWidget, QListWidgetItem, QMenu, QAction, QFileDialog
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from clientSocket import ClientSocket


class ClientUI(QDialog):

    def __init__(self, parent=None):
        super(ClientUI, self).__init__(parent)
        self.setWindowTitle("Client")
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 3458
        self.clientSocket = ClientSocket()
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

        self.startButton = QPushButton("Connect")
        self.startButton.clicked.connect(self.handleStart)

        self.mainLayout.addLayout(self.hostLayout)
        self.mainLayout.addLayout(self.portLayout)
        self.mainLayout.addWidget(self.startButton)

    def refreshList(self):
        self.fileListWidget.clear()

        for filename in self.files:
            listItem = QListWidgetItem(filename)
            listItem.setIcon(QIcon('file-yellow.png'))
            self.fileListWidget.addItem(listItem)

    def downloadItem(self, point):
        item = self.fileListWidget.itemAt(point)
        filename = item.text()
        message = json.dumps({'action': 'download', 'filename': filename})
        self.clientSocket.send_message(message)
        filepath = os.path.join(self.clientSocket.DATA_PATH, filename)
        thread = threading.Thread(
            target=self.clientSocket.recv_file, args=(filepath, ))
        thread.start()

    def deleteItem(self, point):
        item = self.fileListWidget.itemAt(point)
        filename = item.text()
        message = json.dumps({'action': 'delete', 'filename': filename})
        self.clientSocket.send_message(message)
        data = self.clientSocket.recv_message()
        print('==>', data['message'])
        self.files.remove(filename)
        self.refreshList()

    def uploadItem(self):
        fpath = QFileDialog.getOpenFileName(self, 'Upload File', '.')
        filename = ntpath.basename(fpath[0])
        message = json.dumps({'action': 'upload', 'filename': filename})
        self.clientSocket.send_message(message)
        data = self.clientSocket.recv_message()
        print('==>', data['message'])
        thread = threading.Thread(
            target=self.clientSocket.send_file, args=(fpath[0], ))
        thread.start()
        if filename not in self.files:
            self.files.append(filename)
            self.files.sort()
            self.refreshList()

    def myListWidgetContext(self, position):
        popMenu = QMenu()
        downAct = QAction("Download", self)
        delAct = QAction("Delete", self)

        popMenu.addAction(downAct)
        popMenu.addAction(delAct)

        downAct.triggered.connect(
            lambda pos=position: self.downloadItem(position))
        delAct.triggered.connect(
            lambda pos=position: self.deleteItem(position))
        popMenu.setStyleSheet("color: #FFFFFF;")
        popMenu.exec_(self.fileListWidget.mapToGlobal(position))

    def setupConnectedUI(self):
        self.resize(300, 300)
        self.messageLabel = QLabel(f"Connected: {self.HOST}:{self.PORT}")

        self.stopButton = QPushButton("Disconnect")
        self.stopButton.clicked.connect(self.handleStop)

        self.uploadButon = QPushButton("Upload")
        self.uploadButon.clicked.connect(self.uploadItem)

        self.fileListWidget = QListWidget()
        self.refreshList()

        self.fileListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileListWidget.customContextMenuRequested.connect(
            self.myListWidgetContext)
        self.fileListWidget.setStyleSheet(
            "color: #FFFFFF;")

        self.mainLayout.addWidget(self.messageLabel)
        self.mainLayout.addWidget(self.fileListWidget)
        self.mainLayout.addWidget(self.uploadButon)
        self.mainLayout.addWidget(self.stopButton)

    def handleStop(self):
        self.clientSocket.close()
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
        self.files = self.clientSocket.connectToServer(self.HOST, self.PORT)
        self.clearLayout(self.mainLayout)
        self.setupConnectedUI()

    def closeEvent(self, event):
        self.clientSocket.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    clientUi = ClientUI()
    with open("Combinear.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    clientUi.show()

    sys.exit(app.exec_())
