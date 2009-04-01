import pyggel, os
from pyggel import *

import net
from twisted.internet import reactor, threads, error

import ui

def load_config():
    if pyggel.misc.test_safe("data/config.txt")[0]:
        exec open("data/config.txt", "rU")
        return locals()
    else:
        raise ImportWarning("Warning, config file is not safe! Make sure no function calls or importing are present!!!")

class Game(net.Client):
    def __init__(self):
        self.config = load_config()
        pyggel.init(screen_size=self.config["resolution"],
                    screen_size_2d=(640, 480)) #keep 2d at 640x480
        pyggel.view.set_background_color((.75,.75,.75))

        if self.config["fullscreen"]:
            pyggel.view.toggle_fullscreen()
        pyggel.view.set_title(self.config["name"])

        self.game_state = ui.MainMenu(self)

        net.Client.__init__(self, "localhost", 44444, "test!")

    def sendMessage(self, line):
        """Callback for sending out a finished line of input."""
        if len(line) > 0 and self.avatar:
            self.avatar.callRemote("sendMessage", line)

    def update(self):
        self.game_state.update()        

    def errHandler(self, failure):
        e = failure.trap(error.ConnectionRefusedError)
        print e
        if not self.config["verbose_logging"]:
            if e == error.ConnectionRefusedError:
                self.game_state.get_errorMessage("Could not connect to host! :(")
        else:
            self.game_state.get_errorMessage(repr(e))

    def remote_getMessage(self, message):
        self.game_state.get_netMessage(message)

def play():
    g = Game()
##    g.connect()