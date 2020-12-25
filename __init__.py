from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.skills.context import adds_context, removes_context
from adapt.intent import IntentBuilder
from mycroft.util.parse import extract_number
from os.path import dirname, abspath
import sys
sys.path.append(abspath(dirname(__file__)))
import stepper

class SassyBot(MycroftSkill):

    MIN_SETTING = 0
    MAX_SETTING = 100

    def __init__(self):
        MycroftSkill.__init__(self)
        self.rocking = False
        self.humor_setting = 60
        self.baby = 'Niam'
        

    @staticmethod
    def __bound_setting(setting):
        if setting > SassyBot.MAX_SETTING:
            setting = SassyBot.MAX_SETTING
        elif setting < SassyBot.MIN_SETTING:
            setting = SassyBot.MIN_SETTING
        return setting

    def start_rocker(self, message):
        if self.rocking == False:
            # add GPIO start code here
            self.speak_dialog("started", data={"baby" : self.baby})
            self.rocking = True
            stepper.start()
        else:
            self.speak_dialog("status", data={"status" : "started", "baby": self.baby})

    @intent_handler(IntentBuilder("SetHumor").require("humor.setting")
                    .optionally("increase").optionally("decrease")
                    .require("to").optionally("percent"))
    def handle_set_humor_absolute(self, message):
        percent = extract_number(message.data['utterance'].replace('%', ''))
        self.humor_setting = self.__bound_setting(int(percent))
        self.speak_dialog('humor.setting', data={'humor_level': percent})

    @intent_handler(IntentBuilder("QueryHumor").require("query")
                .require("humor.setting"))
    def handle_query_humor_setting(self, message):
        settings = self.humor_setting
        self.speak_dialog('humor.setting', data={'humor_level': settings})
    
    @intent_handler(IntentBuilder("RockerStatus").require("status").build())
    def handle_rocker_status(self, message):
        if self.rocking == True:
            self.speak("Rocking is on")
        else:
            self.speak("Rocker in stopped state.")

    @intent_handler(IntentBuilder("SassyBot").require("start").build())
    def handle_sassy_bot(self, message):
        if self.humor_setting >= 85:
            self.speak_dialog('high.humor')
        elif 75 <= self.humor_setting < 85:
            self.speak_dialog('medium.humor')
        elif 60 <= self.humor_setting < 75:
            self.speak_dialog('low.humor')
        else:
            self.start_rocker(message)
        self.set_context('start_resp')

    @intent_handler(IntentBuilder("StartRocker").require("start_resp").require("please").build())
    #@intent_handler('start.intent')
    def handle_start(self, message):
        self.speak("Fine.")
        self.start_rocker(message)

    @intent_handler(IntentBuilder("StopRocker").require("stop").build())
    #@intent_handler('stop.intent')
    def handle_stop(self, message):
        if self.rocking == True:
            # add GPIO stop code here
            self.rocking = False
            self.speak_dialog("stopped", data={"baby" : self.baby})
            stepper.stop()
        else:
            self.speak_dialog("status", data={"status" : "stopped", "baby": self.baby})

    def initialize(self):
        self.log.info("Baby name: %s" % self.baby)
    
    def stop(self):
        # GPIO to stop rocker
        self.rocking = False
        self.speak_dialog("stopped", data={"baby" : self.baby})
        stepper.stop()
        
def create_skill():
    return SassyBot()
