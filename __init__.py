import requests
import json

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG


def kodi_post(kodi_url, jsonrpc_payload, json_header={'content-type': 'application/json'}):
    """
    Post a request to Kodi jsonrpc
    For more information, https://kodi.wiki/view/JSON-RPC_API/
    and/or https://kodi.wiki/view/JSON-RPC_API/Examples
    or http://ip:port/jsonrpc?request={"jsonrpc": "2.0", "id": 1, "method": "JSONRPC.Introspect", "params": {"getdescriptions" : true, "getmetadata": true}}
    jsonrpc_payload: full json request to send
    Returns the response as is
    """
    assert isinstance(jsonrpc_payload, dict), 'jsonrpc_payload is not a dict: %r' % jsonrpc_payload
    assert isinstance(kodi_url, str), 'kodi_url is not a string: %r' % kodi_url
    try:
        LOG.debug('Sending request to Kodi: %r' % jsonrpc_payload)
        response = requests.post(kodi_url, data=json.dumps(jsonrpc_payload), headers=json_header)
        LOG.debug('Kodi responded with: %r' % response.text)
        return response
    except Exception as e:
        LOG.error('Kodi request/response error with: %r' % e)


class SkillKodiRemote(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        # default init line
        super(SkillKodiRemote, self).__init__(name="SkillKodiRemote")
        # Initialize working variables used within the skill.
        self.on_websettings_changed_count = 0
        self.kodi = None
        self.json_payload = ''
        self.json_response = ''
        
    
    def initialize(self):
        self.settings.set_changed_callback(self.on_websettings_changed)
    
    
    def on_websettings_changed(self):
        self.on_websettings_changed_count += 1
        LOG.info('on_websettings_changed was activated for the ' + str(self.on_websettings_changed_count) + 'th time')
        # get the new settings
        ip, port = self.settings.get('ip'), self.settings.get('port')
        # construct kodi's url
        self.kodi = "http://" + ip + ":" + port + "/jsonrpc"
        LOG.info('Kodi at %r' % self.kodi)
    

    @intent_handler(IntentBuilder("").require("PauseResume").require("Kodi"))
    def handle_pause_kodi_intent(self, message):
        LOG.info('Pausing/Resuming Kodi')
        kodi_post(
            self.kodi, 
            {"jsonrpc": "2.0", "method": "Player.PlayPause", "params": { "playerid": 1 }, "id": 1}
        )
        LOG.info('Paused/Resumed Kodi')

    
    @intent_handler(IntentBuilder("").require("Stop").require("Kodi"))
    def handle_resume_kodi_intent(self, message):
        LOG.info('Stopping Kodi')
        kodi_post(
            self.kodi, 
            {"jsonrpc": "2.0", "method": "Player.Stop", "params": { "playerid": 1 }, "id": 1}
        )
        LOG.info('Stopped Kodi')


    @intent_handler(IntentBuilder("").require("Volume").require("VolumeLevels").require("Kodi"))
    def handle_volume_kodi_intent(self, message):
        LOG.info('Setting Kodi volume level')
        level = message.data.get('VolumeLevels', None)
        LOG.info('Requested Kodi volume level: %r' % level)
        try:
            level = int(level) * 10 # e.g. 7 -> 70 for Kodi's own volume settings
            assert 0 <= level <= 100, "volume level not between 0 and 100: %r" % level
            kodi_post(
                self.kodi, 
                {"jsonrpc": "2.0", "method": "Application.SetVolume", "params": { "volume": level }, "id": 1}
            )
            LOG.info('Set Kodi volume level completed, level set to: %r' % level)
        except Exception as e:
            LOG.error('Error in Kodi volume setting: %r' % e)


# The "create_skill()" method is outside the class itself.
def create_skill():
    return SkillKodiRemote()

