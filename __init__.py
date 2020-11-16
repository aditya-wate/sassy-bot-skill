from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.skills.context import adds_context, removes_context
from adapt.intent import IntentBuilder
from mycroft.util.parse import extract_number

class SassyBot(MycroftSkill):

    MIN_SETTING = 0
    MAX_SETTING = 100

    def __init__(self):
        MycroftSkill.__init__(self)
        self.rocking = False

    @staticmethod
    def __bound_setting(setting):
        if setting > SassyBot.MAX_SETTING:
            setting = SassyBot.MAX_SETTING
        elif setting < SassyBot.MIN_SETTING:
            setting = SassyBot.MIN_SETTING
        return setting

    def __update_setting(self, delta=0):
        """
            Update humor setting
            Args:
                delta (int): +n or -n; the change in percent
            Returns: tuple(new setting int(0..100),
                        setting changed flag (boolean))
        """
        old_setting = self.humor_setting
        new_setting = self.__bound_setting(old_setting + delta)
        self.humor_setting = new_setting
        return new_setting, new_setting != old_setting

    def __ack_humor_update(self, message, new_setting, changed):
        if changed:
            self.speak_dialog('humor.setting', data={'humor_level': new_setting})
        else:
            self.speak_dialog('already.max.setting', data={'humor_level': new_setting})

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
            self.rocking = True
            self.speak_dialog("status", data={"status" : "started", "baby": self.baby})

    @intent_handler(IntentBuilder("StopRocker").require("stop").build())
    #@intent_handler('stop.intent')
    def handle_stop(self, message):
        if self.rocking == True:
            # add GPIO stop code here
            self.speak_dialog("stopped", data={"baby" : self.baby})
        else:
            self.rocking = False
            self.speak_dialog("status", data={"status" : "stopped", "baby": self.baby})

    def initialize(self):
        self.humor_setting = self.settings.get('humor_level', 60)
        self.baby = self.settings.get('baby_name', 'Niam')

def create_skill():
    return SassyBot()

