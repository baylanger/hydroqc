#!/usr/bin/env python
"""
This code is just meant as an example / how-to use the lib

It's voluntarily very verbose :)
"""
import logging
import json
from hydroqc.hydro_api.services import Services
from hydroqc.winter_credit.winter_credit import WinterCredit
from hydroqc.winter_credit.event import Event

myFormatter = logging.Formatter("%(asctime)s - %(name)s [%(levelname)s] : %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(myFormatter)

logging.basicConfig(level=logging.DEBUG, handlers=[handler])
log = logging.getLogger(__name__)


def LowLevelExample():
    s = Services()
    print("WINTER CREDIT SUMMARY")
    print(json.dumps(s.get_winter_credit(), indent=True))
    print("\n\nTODAY CONSUMPTION")
    print(json.dumps(s.get_today_hourly_consumption(), indent=True))
    print("\n\nDAILY CONSUMPTION")
    print(json.dumps(s.get_daily_consumption("2022-01-04", "2022-01-05"), indent=True))


def HighLevelExample():
    w = WinterCredit()
    next_event_object = w.get_next_event()
    if not isinstance(next_event_object, Event):
        next_event = dict()
    else:
        next_event = next_event_object.to_dict()
    print(json.dumps(next_event))
    print(json.dumps(w.get_current_state(), indent=True))
    print(json.dumps(w.get_future_events(), indent=True))


if __name__ == "__main__":
    print("This demo application shows how to use the low level and high level APIs")

    HighLevelExample()
