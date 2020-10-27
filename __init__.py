from mycroft import MycroftSkill, intent_file_handler


class SassyBot(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('bot.sassy.intent')
    def handle_bot_sassy(self, message):
        self.speak_dialog('bot.sassy')


def create_skill():
    return SassyBot()

