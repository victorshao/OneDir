__author__ = 'Zachary Zydron'

import requests
import socket
import PyGithub

class Beacon:
    def __init__(self):
        self.username = 'zzydron'
        self.password = 'onedir555'

    def get_link(self):
        g = PyGithub.BlockingBuilder().Login(self.username, self.password).UserAgent('zzydron').Build()
        user = g.get_authenticated_user()
        r = user.get_repo('Project_Beacon')
        desc = r.description
        data = desc.split(' ')
        ipv4 = data[1].replace('\nPort:','')
        port = int(data[2].replace('\nstatus:',''))
        status = data[3]
        return (ipv4,port,status)

    def set_link(self,status):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        ipv4 = s.getsockname()[0]
        port = 80
        file_string = 'IPv4: ' + ipv4 + '\nPort: ' + str(port) + '\nstatus: ' + status
        g = PyGithub.BlockingBuilder().Login(self.username, self.password).UserAgent('zzydron').Build()
        user = g.get_authenticated_user()
        r = user.get_repo('Project_Beacon')
        r.edit(description=file_string)
        return (ipv4,port,status)


if __name__ == '__main__':
    test = Beacon()
    test.set_link('offline')
    print test.get_link()