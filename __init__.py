import requests
import json

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG


def kodi_post(kodi_url, jsonrpc_payload, json_header={'content-type': 'application/json'}):
    """
    Post a request to Kodi jsonrpc
    For more information, https://kodi.wiki/view/JSON-RPC_API/
    jsonrpc_payload: full json request to send
    Returns the response as is
    """
    assert isinstance(jsonrpc_payload, dict), "jsonrpc_payload is not a dict: %r" % jsonrpc_payload
    assert isinstance(kodi_url, str), "kodi_url is not a string: %r" % kodi_url
    try:
        response = requests.post(kodi_url, data=json.dumps(jsonrpc_payload), headers=json_header)
        LOG.info('Kodi responded with :' + response.text)
        return response
    except Exception as e:
        LOG.error('Kodi request/response error with ' + e)


class SkillKodiRemote(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        # default init line
        super(SkillKodiRemote, self).__init__(name="SkillKodiRemote")
        # Initialize working variables used within the skill.
        self.on_websettings_changed_count = 0
        self.kodi = None
        self.json_payload = ""
        self.json_response = ""
        
    
    def initialize(self):
        self.settings.set_changed_callback(self.on_websettings_changed)
    
    
    def on_websettings_changed(self):
        self.on_websettings_changed_count += 1
        LOG.info('on_websettings_changed was activated' + str(self.on_websettings_changed_count) + 'th time')
        # get the new settings
        ip, port = self.settings.get('ip'), self.settings.get('port')
        # construct kodi's url
        self.kodi = "http://" + ip + ":" + port + "/jsonrpc"
        LOG.info('Kodi at " + self.kodi)
    

    # The "handle_xxxx_intent" function is triggered skill's intent is matched.
    # triggered when the user's utterance matches the pattern defined by the keywords
    # eg vocab/en-us/Kodi.voc
    @intent_handler(IntentBuilder("").require("Pause").require("Kodi"))
    def handle_pause_kodi_intent(self, message):
        LOG.info('Pausing Kodi')
        pass

    @intent_handler(IntentBuilder("").require("Resume").require("Kodi"))
    def handle_resume_kodi_intent(self, message):
        LOG.info('Resuming Kodi')
        pass


    @intent_handler(IntentBuilder("").require("Stop").require("Kodi"))
    def handle_resume_kodi_intent(self, message):
        """Should pass equivalent of 'x' to Kodi"""
        LOG.info('Stopping Kodi')
        pass


    @intent_handler(IntentBuilder("").optional("Set").require("Volume").require("Kodi"))
    def handle_volume_kodi_intent(self, message):
        LOG.info('Setting Kodi volume')
        pass


# The "create_skill()" method is outside the class itself.
def create_skill():
    return SkillKodiRemote()

