# -*- coding: utf-8-*-
"""
A drop-in replacement for the Mic class that allows for all I/O to occur
over the terminal. Useful for debugging. Unlike with the typical Mic
implementation, Jasper is always active listening with local_mic.
"""
import crossbarconnect
import wit
import os
import jasperpath
import yaml

class Mic:
    prev = None

    def __init__(self,speaker,passive_stt_engine,active_stt_engine):
        self.client = crossbarconnect.Client("http://127.0.0.1:8080/publish")
	profile_path = jasperpath.config('profile.yml')
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = yaml.safe_load(f)
                if 'witai-stt' in profile:
                    if 'access_token' in profile['witai-stt']:
                        self.token = profile['witai-stt']['access_token']

    def passiveListen(self, PERSONA):
        return True, "JASPER"

    def activeListenToAllOptions(self, THRESHOLD=None, LISTEN=True,
                                 MUSIC=False):
        return [self.activeListen(THRESHOLD=THRESHOLD, LISTEN=LISTEN,
                                  MUSIC=MUSIC)]

    def activeListen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        if not LISTEN:
            return self.prev

        input = raw_input("YOU: ")
        self.prev = input
	wit.init()
	response = wit.text_query(input, self.token)
	wit.close()
        return response

    def say(self, phrase, OPTIONS=None):
        print("JASPER: %s" % phrase)
	self.client.publish("com.selfridges.speech",phrase)
