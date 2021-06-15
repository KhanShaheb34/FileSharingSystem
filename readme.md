# File Sharing System

Share files through TCP socket in a network. Built using Python and Qt.

## Install Required Packages

Install the `PySide2` package for Qt. Open terminal and run:

```sh
pip install PySide2
```

## Running Server

Open a terminal in this folder and run:

```sh
python serverMain.py
```

This will open the ui for server. Enter the Host address and Port and press the `Start Server` button. Then server will start in the given host and port.

## Running Client

Open a terminal in this folder and run:

```sh
python clientMain.py
```

At first a ui will start that is same as the server. You have to enter the host address and port of the server. Then press the `Connect` button.

Then the window will open with the list of the files that is in the `data` folder of the server. From here you can:

- Download any file
  - Right click on a file from the list
  - Select `Download`
  - Downloaded files will be saved in the `downloads` folder
- Delete any file
  - Right click on a file from the list
  - Select `Delete`
- Upload a file
  - Select the `Upload` button from the bottom of the file list
  - A file dialogue will open, then select a file to upload
  - Uploaded files will be saved in the `data` folder in the server

## Additional Information

- The server handles each client in a different thread, so the multiple client can be connected at the same time
- A client can download multiple file at the same time
- The file list from client ui will be automatically upadted everytime a file gets uploaded or deleted from the client ui

## Developers

- Shakirul Hasan Khan
- Nishat Tasniya Rahman
