Application is able to open DICOM file and display it

Applciation uses pyside6 for GUI

**To install:** 
pip install -r requirements.txt

**To run:** 
WARNING: It must be run from this location (ie. in the root directory) to avoid some issues at the moment.
```python src/main.py```

**Design:**
1. main.py: 
-creates instances of model, view, controller
2. views 
-Display windows
3. models: 
-Stores program data and state
    --> In our case, we need to track the current open file and its data.
    --> Track directory that we are using too.
4. controller --> performs logic. Links view to model (should not directly talk)
    --> In our case:
        -check for default directory in config DB
        -Get/set default config. (default directory)
        -set/get dicom directory
        -set/get current file
        -Navigate through files

**Contributions**
Run:
```pytest```
```pylint --extension-pkg-whitelist=PyQt6,PySide6 src/```
```pycodestyle --show-source --show-pep8 src/```

To check what coverage we have on our project with testing we can run:
```pytest --cov=src```

-Ideally we would like to maintain minimum 85% coverage, so as you add code, try add tests.


**References:**
https://doc.qt.io/qt-5/model-view-programming.html#handling-selections-of-items
https://stackoverflow.com/questions/26698628/mvc-design-with-qt-designer-and-pyqt-pyside