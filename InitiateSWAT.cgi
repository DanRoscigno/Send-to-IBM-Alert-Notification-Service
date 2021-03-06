#!/opt/IBM/netcool/python27/bin/python
import cgitb
cgitb.enable()
print "Content-type: text/html"
print

print """
<html>

<head><title>Post to AlertNotification</title></head>

<body>

  <h3>Post to AlertNotification </h3>
<br><br>
  <pre>
"""

import json
import requests

"""
Put your AlertNotification url, and API key / value into a config file
AlertNotification.ini in this format:

[Production]
URI: https://ibmnotify.mybluemix.net/api/alerts/v1
username: '11blahblahblahblahblahblahblahdf/foobarblatos'
password: 'foobarblafoobarblafoobarblaxyzzy'

"""

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("/opt/IBM/netcool/gui/omnibus_webgui/etc/cgi-bin/AlertNotification.ini")

import os, sys
from cgi import escape

keys = os.environ.keys()

import urlparse
SWAT_info = {}
SWAT_info = dict(urlparse.parse_qsl(os.environ['QUERY_STRING']))

"""
This gives me these keys:
    Key				          Description
  SWAP_opsteam      Ops team to page
  SWAT_issue        Issue reported by customer
  SWAT_customer     Customer name and environment
  WEBTOP_USER       Username in Netcool
"""

import time
session        = SWAT_info['SWAT_session']
issue          = SWAT_info['SWAT_issue']
customer       = SWAT_info['SWAT_customer']
opsteam        = SWAT_info['opsteam']
Identifier     = 'Initiate SWAT Tool' + str(time.time()) + opsteam
Where          = customer + ' ' + SWAT_info['SWAT_environment']
What           = 'SWAT Needed for ' + opsteam + ' Customer: ' + customer + ' CARE Session: ' + session + ' Reported at: ' + SWAT_info['SWAT_TimeRaised'] + ' Issue: ' + issue
When           = ''
Severity       = 'Critical'
Type           = '2'
Source         = 'Initiate SWAT Tool'

# Up top we read the config, now we will lookup the username and password for Alert Notification
URI        = Config.get('Production', 'URI')
username   = Config.get('Production', 'username')
password   = Config.get('Production', 'password')

alertNotification_data = {
  "Identifier": "%s" % Identifier,
  "What": "%s" % What,
  "Where": "%s" % Where,
  "Severity": "%s" % Severity,
  "Type": "Problem",
  "Source": "Initiate SWAT Tool",
}

print 'This is what was sent to Alert Notification:'
print json.dumps(alertNotification_data, sort_keys=False, indent=4, separators=(',', ': '))
print '</pre>'

alertNotificationResponse = requests.post(
    URI, auth=(username,password), json=alertNotification_data
)


if alertNotificationResponse.status_code != 200:
    raise ValueError(
        'There was an error (%s) during posting the message to Alert Notification, the response is:\n%s'
        % (alertNotificationResponse.status_code, alertNotificationResponse.text)
    )
else:
    print "Successfully posted to Alert Notification"

print """

<br>
<b>Note: Please close this tab before initiating another SWAT.</b>

</body>

</html>
"""

