__author__ = 'Zachary Zydron'


import sqlite3
import os
import user


class Bouncer:

    def __init__(self, db_loc):
        self.admin_challenge = '1234'
        self.user_db_loc = db_loc
        self.user_cache = []

    """ def get_user_info(self):
        - Reads in all current users from the database. Places list of user objects in
         the 'self.user_cache' field"""
    def get_user_info(self):
        database = sqlite3.connect(self.user_db_loc)
        c = database.cursor()
        temp_list = []
        for row in c.execute('SELECT * FROM user_info'):
            temp = user.user()
            if (temp.set_password(str(row[1]))[0] == False):
                print temp.set_password(str(row[1]))[1]
            temp.set_user_id(str(row[0]))
            temp.admin = row[2]
            temp.set_directory(str(row[3]))
            temp_list.append(temp)
        database.close()
        self.user_cache = temp_list

    """ def add_user(self,t_user):
    - adds user object data to the database of users"""
    def add_user(self,t_user):
        print 'Adding User: ' + t_user.user_id
        database = sqlite3.connect(self.user_db_loc)
        c = database.cursor()
        c.execute("INSERT INTO user_info VALUES (?,?,?,?)", (t_user.user_id, t_user.password , t_user.admin, t_user.directory))
        database.commit()
        database.close()

    """ def register_user(self, username, password, verification):
        - adds user to the database of users, is unsuccessful then an error message is returned"""
    def register_user(self, username, password, verification):
        temp = user.user()
        username_f = ''
        if('admin_' in username):
            username_f = username.replace('admin_', '', 1)
            temp.set_admin(verification)
        else:
            username_f = username
            temp.set_admin('0')

        self.get_user_info()
        if self.in_user_cache(username_f):
            return (False, 'User ID ' + username_f + ' already exists')
        else:
            temp.set_user_id(username_f)

        if (temp.set_password(password)[0] == 0):
            return (False, temp.set_password(password)[1])

        temp.set_directory('/users/' + username_f)

        self.add_user(temp)
        return (True, 'User ' + username_f + ' Added to Database Successful')


    """ def get_user_profile(self,username):
        - returns user object from user cache given the user_id"""
    def get_user_profile(self,username):
        user_cache = self.get_user_info()
        for i in range(0, len(self.user_cache)):
            if self.user_cache[i].is_user_id(username):
                return self.user_cache[i]
        return False

    """ def in_user_cache(self,username):
        - determines if the user object exists in the user_cache"""
    def in_user_cache(self,username):
        if not self.get_user_profile(username):
            return False
        else:
            return True

    """ def login_user(self, username, password):
        - returns user object of user given correct credentials, returns error message if unsuccessful"""
    def login_user(self, username, password):
        self.get_user_info()
        if (self.in_user_cache(username)):
            temp = self.get_user_profile(username)
            if (password == temp.password):
                return temp
            else:
                return (False, 'Password Incorrect')
        else:
            return (False, 'User Does Not Exist')

    """ def get_users(self,t_user):
        - returns list of user objects if an admin is present"""
    def get_users(self,t_user):
        if (t_user.admin == 1):
            self.get_user_info()
            return self.user_cache
        else:
            return (False, 'You are not an admin')

    """ def del_user(self,t_user):
        - Deletes record of user from the database"""
    def del_user(self,t_user):
        database = sqlite3.connect(self.user_db_loc)
        c = database.cursor()
        c.execute("DELETE FROM user_info WHERE username = (?)", (t_user.user_id,))
        database.commit()
        c.close()
        print 'Deleting User: ' + t_user.user_id

    """ def change_user_password(self,t_user):
        - Deletes old instance of the user from the database, changes the password,
          then updates database with the new user information. This method will return
          error messages if the password change cannot take place."""
    def change_user_password(self,admin,t_username,password):
        if not self.in_user_cache(t_username):
            return (False, 'User ' + t_username + ' does not exist')
        elif (admin.admin == 0):
            return (False, 'You are not an admin')

        t_user = self.get_user_profile(t_username)
        self.del_user(t_user)
        if (t_user.set_password(password)[0] == False):
            return (False, t_user.set_password(password)[1])
        self.add_user(t_user)
        return (True, 'Password Changed Successfully')

# --- THESE ARE TESTING METHODS FOR THE CLASS ---
    def test_table(self):
        self.create_table()
        self.load_test_users()
        return self.get_user_info()

    def create_table(self):
        if (os.path.isfile(self.user_db_loc) == False):
            open(self.user_db_loc, 'a').close()
        database = sqlite3.connect(self.user_db_loc)
        c = database.cursor()
        c.execute('''DROP TABLE IF EXISTS user_info''')
        c.execute('''CREATE TABLE user_info
          (username text, password text, admin int, file_directory text)''')
        c.close()

    def load_test_users(self):
        database = sqlite3.connect(self.user_db_loc)
        c = database.cursor()
        c.execute("INSERT INTO user_info VALUES ('admin','1234567A',1,'admin_location')")
        database.commit()
        c.execute("INSERT INTO user_info VALUES ('Bob','45678910',0,'Bob_location')")
        database.commit()
        c.execute("INSERT INTO user_info VALUES ('Zach','789dfdkfnv0',1,'Zach_location')")
        database.commit()
        c.close()


def print_list(list):
    for i in range(0,len(list)):
        string = 'User ID: ' + list[i].user_id
        string += ' Password: ' + list[i].password
        string += ' Admin: ' + str(list[i].admin)
        string += ' Directory: ' + list[i].directory
        print string


if __name__ == '__main__':
    test = Bouncer('user_info.db')
    test.create_table()
    test.load_test_users()
    test.get_user_info()
    admin = user.user()
    admin.user_id = 'Zachary'
    admin.password = 'abcdefghi'
    admin.admin = 1
    admin.directory = 'users/admin/'
    test.add_user(admin)
    print_list(test.get_users(admin))
    print '            --              '
    test.del_user(admin)
    test.get_user_info()
    print_list(test.user_cache)
    print '            --              '
    test.add_user(admin)
    print_list(test.user_cache)
    print '            --              '
    if (test.change_user_password(admin,'Bob','Bobs_new_password')[0] == False):
        print test.change_user_password(admin,'Bob','Bobs_new_password')[1]
    print_list(test.user_cache)
    print '            --              '

