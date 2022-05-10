Application is able to open DICOM file and display it

Applciation uses pyside6 for GUI

**To install:** 
pip install -r requirements.txt

**To run:** 
python src/main.py

**Design:**
main.py --> creates instances of model, view, controller
views --> Display windows
models --> Stores program data and state
    --> In our case, we need to track the current open file and its data.
    --> Track directory that we are using too.
controller --> performs logic. Links view to model (should not directly talk)
    --> In our case:
        -check for default directory in config DB
        -Get/set default config. (default directory)
        -set/get dicom directory
        -set/get current file
        -Navigate through files

**References:**
https://doc.qt.io/qt-5/model-view-programming.html#handling-selections-of-items
https://stackoverflow.com/questions/26698628/mvc-design-with-qt-designer-and-pyqt-pyside