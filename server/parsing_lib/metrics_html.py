
from datetime import datetime

class MetricsHTML(object):
    """ Handles device metrics from the Mobile API. """

    @staticmethod
    def to_html(message):
        return {"messageType":"deviceMetrics",
            "cpuUsage":message['cpuUsage'],
            "memUsage":(message['memUsage'])/1024.0,
            "netSentPerSec":  message['netSentPerSec'],
            "netReceivePerSec": message["netReceivePerSec"],
            "timeStamp":"11:00",
            }
