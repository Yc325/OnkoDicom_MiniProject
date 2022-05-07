#import Libraries

#Some of the functions is used from open sourced code
#link https://amirkoblog.wordpress.com/2018/07/26/using-pyside2-and-pydicom-to-display-dicom-header-information/

from display_func import *


class MainWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.w = True  # No external window yet.
        #set window Title
        self.setWindowTitle('OnkoDicom')
        #Create 2 Buttons
        button_suc = QPushButton("Open Dicom File")
        button_close = QPushButton("Force Quit",self)
        #Assign Buttons
        button_suc.clicked.connect(self.Window_to_browse_DICOM_files)
        button_close.clicked.connect(QApplication.instance().quit)

        label = QLabel("InkoDICOM")
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # set aligment

        #Create LOGO of DICOM
        pixmap = QPixmap('img/logo.png')
        pixmap = pixmap.scaled(200,200, Qt.KeepAspectRatio)
        label.setPixmap(pixmap)  # add img

        #Create Grid layout to properly locate the buttons and other widgets
        layout = QGridLayout()
        layout.addWidget(label, 0, 0, 3, 5, Qt.AlignCenter ) #Add label
        layout.addWidget(button_suc, 3, 0) #Add button
        layout.addWidget(button_close, 3, 4) #Add button

        #Create Container and add layout to it.
        container = QWidget()
        container.setLayout(layout)

        #Run it
        self.setCentralWidget(container)


    #Button to close window
    """
    This function alllows you to set notification to close window
    
    """
    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(
            self,
            'Message',
            'Are you sure you want to quit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    #Window Dicom File
    """
    Function that allows you to  open Directory of your PC and choose DICOM File
    """
    def Window_to_browse_DICOM_files(self):
        self.browseButton = self.createButton("&Browse...", self.browse) #Bar where you can type Path
        self.directoryComboBox = self.createComboBox(QDir.currentPath()) #Display current path

        directoryLabel = QLabel("In directory:")
        self.filesFoundLabel = QLabel()

        self.createFilesTable()

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()

        #Create GRID LAYOUT
        mainLayout = QGridLayout()
        mainLayout.addWidget(directoryLabel, 2, 0)
        mainLayout.addWidget(self.directoryComboBox, 2, 1)
        mainLayout.addWidget(self.browseButton, 2, 2)
        mainLayout.addWidget(self.filesTable, 3, 0, 1, 3)
        mainLayout.addWidget(self.filesFoundLabel, 4, 0)
        mainLayout.addLayout(buttonsLayout, 5, 0, 1, 3)


        container = QWidget()
        container.setLayout(mainLayout)
        self.setWindowTitle("Explore DICOM Files")
        self.resize(1200, 800)
        self.setCentralWidget(container)

    """
    Function Browse:
    Open Directory and allow you to choose Folder with DICOM format Files
    Then Function is looking for DICOM FILES by calling function "find()"
    """
    def browse(self):
        directory = QFileDialog.getExistingDirectory(self, "Find Files",
                                                               QDir.currentPath())

        if directory:
            if self.directoryComboBox.findText(directory) == -1:
                self.directoryComboBox.addItem(directory)

            self.directoryComboBox.setCurrentIndex(self.directoryComboBox.findText(directory))
            self.find()

    @staticmethod
    def updateComboBox(comboBox):
        if comboBox.findText(comboBox.currentText()) == -1:
            comboBox.addItem(comboBox.currentText())

    """
    Function is looking for all dcm files in a folder
    """
    def find(self):
        self.filesTable.setRowCount(0)

        path = self.directoryComboBox.currentText()

        self.updateComboBox(self.directoryComboBox)

        self.currentDir = QDir(path)
        fileName = "*.dcm"
        files = self.currentDir.entryList([fileName],
                                          QDir.Files | QDir.NoSymLinks)

        self.showFiles(files)

    """
    Function prepare window with all found DICOM files
    """
    def showFiles(self, files):
        for fn in files:
            file = QFile(self.currentDir.absoluteFilePath(fn))
            size = QFileInfo(file).size()

            fileNameItem = QTableWidgetItem(fn)
            fileNameItem.setFlags(fileNameItem.flags() ^ Qt.ItemIsEditable)
            sizeItem = QTableWidgetItem("%d KB" % (int((size + 1023) / 1024))) #Caluclate size
            sizeItem.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            sizeItem.setFlags(sizeItem.flags() ^ Qt.ItemIsEditable)

            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, fileNameItem)
            self.filesTable.setItem(row, 1, sizeItem)

        self.filesFoundLabel.setText("%d file(s) found (Double click on a file to open it)" % len(files))

    def createButton(self, text, member):
        button = QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, text=""):
        comboBox = QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QSizePolicy.Expanding,
                               QSizePolicy.Preferred)
        return comboBox

    def createFilesTable(self):
        self.filesTable = QTableWidget(0, 2)
        self.filesTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.filesTable.setHorizontalHeaderLabels(("File Name", "Size"))
        self.filesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(False)
        self.filesTable.cellActivated.connect(self.openFileOfItem)

    """
    Function opens choosen file and call function to disaply this file in
    a new window
    """

    #Open Chosen file
    def openFileOfItem(self, row, column):
        item = self.filesTable.item(row, 0)
        path = self.directoryComboBox.currentText() + "/" + item.text()
        dataset = pydicom.dcmread(path)

        all_tags = ''
        for elem in dataset:
            tag = str(elem) + '\n'
            all_tags += tag

        displayDicomImage(self,dataset,all_tags) #Takes DICOM File



app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()