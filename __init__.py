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
    #    vocab/en-us/XXX.voc
    #    vocab/en-us/YYY.voc
    #    vocab/en-us/ZZZ.voc
    @intent_handler(IntentBuilder("").require("XXX").require("YYY").optional('ZZZ'))
    def handle_hello_world_intent(self, message):
        # Mycroft to respond by simply speaking a canned response randomly from
        #    dialogs/en-us/abcde.gfde.dialog
        self.speak_dialog("abcde.gfde")


    # The "stop" method defines what Mycroft does when told to stop during skill's execution
    # the skill's execution. In this case, since the skill's functionality
    # If you DO need to implement stop, you should return True to indicate you handled it.
    # def stop(self):
    #    return False


# The "create_skill()" method is outside the class itself.
def create_skill():
    return TemplateSkill()

