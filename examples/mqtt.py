#!/usr/bin/env python
"""
MQTT test publisher

This will publish only once and exit
"""

import paho.mqtt.client as paho
import datetime
import time
from hydroqc.winter_credit.winter_credit import WinterCredit
from hydroqc.winter_credit.event import Event

broker = 'YOUR_MQTT_SERVER'
port = 1883
user = 'MQTT_USERNAME'
password = 'MQTT_PASSWORD'
base_topic = 'hydroqc' # Or whatever suits you

w = WinterCredit()
contract_id = w.api.auth.contract_id

def on_publish(client,userdata,result):             #create function for callback
    print("data published [#%s]" % result)
    pass

mqtt_client= paho.Client("HydroQC")
mqtt_client.on_publish = on_publish
if user and password:
    mqtt_client.username_pw_set(username=user, password=password)
mqtt_client.connect(broker,port)
mqtt_client.loop_start()
next_event_object = w.get_next_event()
if not isinstance(next_event_object,Event):
    next_event = dict()
else:
    next_event = next_event_object.to_dict()


if next_event:
    for key in next_event.keys():
        ret= mqtt_client.publish("%s/%s/winterpeaks/next/critical/%s" % (base_topic, contract_id,key), next_event[key], qos=1, retain=True)

state = w.get_current_state()
if state:
    for key in state['state'].keys():
        ret = mqtt_client.publish("%s/%s/winterpeaks/state/%s" % (base_topic, contract_id,key), state['state'][key], qos=1, retain=True)
    for topic in state['next'].keys():
        for key in state['next'][topic].keys():
            ret = mqtt_client.publish("%s/%s/winterpeaks/next/%s/%s" % (base_topic,contract_id, topic, key), state['next'][topic][key], qos=1, retain=True)
    for topic in state['anchor_periods'].keys():
        for key in state['anchor_periods'][topic].keys():
            ret = mqtt_client.publish("%s/%s/winterpeaks/today/anchor_periods/%s/%s" % (base_topic,contract_id, topic, key), state['anchor_periods'][topic][key], qos=1, retain=True)
    for topic in state['peak_periods'].keys():
        for key in state['peak_periods'][topic].keys():
            ret = mqtt_client.publish("%s/%s/winterpeaks/today/peak_periods/%s/%s" % (base_topic,contract_id, topic, key), state['peak_periods'][topic][key], qos=1, retain=True)



    # Last update timestamp, should probably be in the winter_credit.py
    # TODO: Replace with proper LWT https://www.hivemq.com/blog/mqtt-essentials-part-9-last-will-and-testament/
    now = datetime.datetime.now()
    last_update = now.strftime("%Y-%m-%d %H:%M:%S")
    ret = mqtt_client.publish("%s/%s/winterpeaks/last_update" % (base_topic, contract_id), payload=last_update, qos=1, retain=True)

mqtt_client.loop_stop()
mqtt_client.disconnect()
