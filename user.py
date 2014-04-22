__author__ = 'Zachary Zydron'

MIN_PASS_LENGTH = 7
ADMIN_CODE = '1234'

class user:

    def __init__(self):
        self.user_id = ''
        self.password = ''
        self.admin = 0
        self.directory = ''
        self.space_used = 0

    def set_password(self,password):
        blacklist = ['password','guest',self.user_id,'admin']
        if len(password) < MIN_PASS_LENGTH:
            message = 'Password must be greater than or equal ' + str(MIN_PASS_LENGTH) + ' characters'
            return (0, message)
        elif password in blacklist:
            message = 'Password cannot be' + password
            return (0, message)
        else:
            self.password = password
            return (1, 'Password Acceptable')

    def set_admin(self,ver_code):
        if (self.admin == 0):
            if ver_code == ADMIN_CODE:
                self.admin = 1
                return (1, 'Code Accepted, Granting Admin Rights')
            else:
                self.admin = 0
                return (0, 'Code Not Accepted, Admin Rights Not Granted')
        else:
            if ver_code == ADMIN_CODE:
                self.admin = 0
                return (1, 'Code Accepted, Admin Rights Removed')
            else:
                return (0, 'Code Not Accepted, Admin Rights Not Changed')

    def set_user_id(self,username):
        self.user_id = username

    def set_directory(self,location):
        self.directory = location

    def get_password(self,other):
        if (other.admin == 0):
            return (0, 'Admin Rights Not Present')
        else:
            return (1, self.password)

    def get_directory(self):
        return self.directory

    def get_user_id(self):
        return self.user_id

    def is_user_id(self,string):
        if (string == self.user_id):
            return True
        else:
            return False