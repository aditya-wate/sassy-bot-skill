from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.skills.context import adds_context, removes_context


class SassyBot(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.rocking = False

    # @intent_handler('bot.sassy.intent')
    # def handle_bot_sassy(self, message):
    #     self.speak_dialog('bot.sassy')

    @intent_handler(IntentBuilder("RockerStatus").require("status").build())
    def handle_rocker_status(self, message):
        if self.rocking == True:
            self.speak("Rocking is on")
        else:
            self.speak("Rocker in stopped state.")

    @intent_handler(IntentBuilder("StartRocker").require("start").build())
    #@intent_handler('start.intent')
    def handle_start(self, message):
        if self.rocking == False:
            # add GPIO start code here
            self.speak_dialog("started", data={"baby" : self.baby})
        else:
            self.speak_dialog("status", data={"status" : "started", "baby": self.baby})

    @intent_handler(IntentBuilder("StopRocker").require("stop").build())
    #@intent_handler('stop.intent')
    def handle_stop(self, message):
        if self.rocking == True:
            # add GPIO stop code here
            self.speak_dialog("stopped", data={"baby" : self.baby})
        else:
            self.speak_dialog("status", data={"status" : "stopped", "baby": self.baby})

    def initialize(self):
        self.humor_setting = self.settings.get('humor_level')
        self.baby = self.settings.get('baby_name')

def create_skill():
    return SassyBot()

