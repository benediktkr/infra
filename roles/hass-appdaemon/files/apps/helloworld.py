import hassapi

#
# Hello World App
#
# Args:
#

class HelloWorld(hassapi.Hass):
    def initialize(self):
        self.log("init: helloworld")
