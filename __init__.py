from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

class SkillKodiRemote(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        # default init line
        super(SkillKodiRemote, self).__init__(name="SkillKodiRemote")
        # Initialize working variables used within the skill.
        self.on_websettings_changed_count = 0
        self.kodi = None
        self.json_header = {'content-type': 'application/json'}
        self.json_payload = ""
        self.json_response = ""
        
    
    def initialize(self):
        self.settings.set_changed_callback(self.on_websettings_changed)
    
    
    def on_websettings_changed(self):
        self.on_websettings_changed_count += 1
        LOG.info('on_websettings_changed was activated' + str(self.on_websettings_changed_count) + 'th time')
        # get the new settings
        (ip, port, uname, passwd) = (self.settings.get('ip')
                                     , self.settings.get('port')
                                     , self.settings.get('uname')
                                     , self.settings.get('passwd')
        # construct kodi's url
        self.kodi = "http://" + uname + ":" + passwd + "@" + ip + ":" + port + "/jsonrpc"
    

    # The "handle_xxxx_intent" function is triggered skill's intent is matched.
    # triggered when the user's utterance matches the pattern defined by the keywords
    # the match occurs when one word is found from each of the files:
    #    vocab/en-us/Pause.voc
    #    vocab/en-us/Kodi.voc
    @intent_handler(IntentBuilder("").require("Pause").require("Kodi"))
    def handle_pause_kodi_intent(self, message):
        # Mycroft to respond by simply speaking a canned response randomly from
        #    dialogs/en-us/abcde.gfde.dialog
        # self.speak_dialog("abcde.gfde")
        pass


    @intent_handler(IntentBuilder("").require("Resume").require("Kodi"))
    def handle_resume_kodi_intent(self, message):
        pass


    @intent_handler(IntentBuilder("").require("Stop").require("Kodi"))
    def handle_resume_kodi_intent(self, message):
        """Should pass equivalent of 'x' to Kodi"""
        pass


    @intent_handler(IntentBuilder("").optional("Set").require("Volume").require("Kodi"))
    def handle_volume_kodi_intent(self, message):
        pass


# The "create_skill()" method is outside the class itself.
def create_skill():
    return SkillKodiRemote()

