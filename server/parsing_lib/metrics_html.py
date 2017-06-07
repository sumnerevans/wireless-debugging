
from datetime import datetime

class MetricsHTML(object):
    """ Handles device metrics from the Mobile API. """

    @staticmethod
    def to_html(message):
        return {"messageType":"deviceMetrics",
            "cpuUsage":message['cpuUsage'],
            "timeStamp":"11:00",
            "memUsage":(message['memUsage'])/1024.0,
            }
