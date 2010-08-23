"""Server and client for the server-game-server"""


import net, urllib

main_server_host = 'localhost' #change to real server later!
main_server_port = 54321

def get_my_server_ip():
    f = urllib.urlopen("http://checkip.dyndns.com")
    s = f.read()
    f.close()

    return s[s.find('<body>')+6:s.find('</body>')].split(":")[1].strip()

class Game(object):
    def __init__(self, name):
        self.name = name
        self.scenario = "" #todo - make base scenario

class Server(net.Server):
    def __init__(self):
        net.Server.__init__(self)

        self.games_list = {}

    def join(self, avatar):
        self.avatars.append(avatar)

    def leave(self, avatar):
        self.avatars.remove(avatar)

    def requestNewAvatar(self):
        return SLGAvatar

    def registerGameServer(self, avatar, name, port, ip):
        self.server_list[avatar] = (name, port, ip)

    def getGameServerList(self, avatar):
        self.remote(avatar, 'sendGameServerList', self.server_list.values())

class SLGAvatar(net.BaseAvatar):
    def perspective_registerServer(self, name, port):
        ip = get_my_server_ip()
        self.server.registerGameServer(self, name, port, ip)

class Client(net.Client):
    def remote_sendGameServerList(self, _list):
        pass
