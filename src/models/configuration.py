import sqlite3
import os
from pathlib import Path

def create_hidden_dir():
    """
    Create the hidden directory
    """
    # Path.home() will return a path object for the user's home directory, its cross-platform
    # .joinpath will construct new path using the home directory as the foundation
    path = Path.home().joinpath('Secret')
    # check if path actually exists
    if not os.path.exists(path):
        print(path)
        # creates new directory
        os.mkdir(path)
        # Sets hidden attribute to hide (+h hide -h reveal)
        #os.system("attrib +h " + str(path))
    return path


# Singleton allows you to create only one instance of a class through the lifetime of a program
# (metaclass=Singleton):will add later as you need to install package that isn't included in requirements
class Configuration():

    def __init__(self, db_path ='', db_file ='.dicom.db'):
        self.db_path = create_hidden_dir().joinpath(db_file)
        self.set_up_db()

    def set_up_db(self):
        """
        Create database within the hidden directory
        """
        # Connection object to represent database
        conn = sqlite3.connect(self.db_path)# either pass file or create an in memory database
        # creates database if it doesn't already exist
        conn.execute("""
                CREATE TABLE IF NOT EXISTS CONFIGURATION (
                    id INTEGER PRIMARY KEY,
                    default_dir TEXT
                )
            """)
        conn.commit()
        conn.close()

    def get_default_dir(self):
        """
        Retrieves default directory from database
        """
        # Connection object to represent database
        conn = sqlite3.connect(self.db_path)
        # creates cursor
        cursor = conn.cursor()
        # Gets default directory
        cursor.execute("SELECT default_dir FROM CONFIGURATION WHERE id = 1")
        # stores directory path, if there is no directory path it will store "None"
        path = cursor.fetchone()
        conn.close()
        return path

    def update_default_dir(self, new_dir):
        """
        Adds/updates default directory
        """
        # Connection object to represent database
        conn = sqlite3.connect(self.db_path)
        # creates cursor
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM CONFIGURATION;")
        # check if file exists
        if cursor.fetchone()[0]==0:
            # if no files exist than it will insert the default path
            conn.execute("""INSERT INTO configuration (id, default_dir) 
                                VALUES (1, "%s");""" % new_dir)
        else:
            # if files exist than it will update the default path
            conn.execute("""UPDATE CONFIGURATION
                            SET default_dir = "%s"
                            WHERE id = 1;""" % new_dir)
        conn.commit()
        conn.close()





