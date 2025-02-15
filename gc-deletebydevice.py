#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Revision 2025-02-13 by jstevenco
# - Add back in support for date range from original Pastebin script
# - make code more Pythonic
# - Put script into Github where revisions can be tracked
#
# Revision 2024-06-12 by Additional-Point-824
# https://www.reddit.com/r/Garmin/comments/1de5mbj/deletejusttheactivitiesfromasinglegarmindevicefrom/

# Initial version and revisions (2021-02-27) by WillNorthYork
# https://pastebin.com/WwsUauH1
# https://forums.garmin.com/apps-software/mobile-apps-web/f/garmin-connect-web/165851/can-i-delete-just-the-activities-from-a-single-garmin-device-from-my-garmin-connect-account

"""
Garmin Connect Python API:

Package: garminconnect
Author: Ron Klinkien (https://github.com/cyberjunky/)
Pypi: https://pypi.org/project/garminconnect/
Requires: Python >= 3.10
"""

def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press ENTER to exit.")
    sys.exit(-1)

import sys
sys.excepthook = show_exception_and_exit

# ##############################################

from datetime import date, datetime
from getpass import getpass
from sys import argv

import argparse

from garminconnect import Garmin

SCRIPT_VERSION = '0.0.2'

PARSER = argparse.ArgumentParser()

# TODO: Implement verbose and/or quiet options.
# PARSER.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
PARSER.add_argument('--version', help="print version and exit", action="store_true")
PARSER.add_argument('--username', help="your Garmin Connect username (otherwise, you will be \
    prompted)", nargs='?')
PARSER.add_argument('--password', help="your Garmin Connect password (otherwise, you will be \
    prompted)", nargs='?')

PARSER.add_argument('--deviceid', help="the device ID for activities to delete (otherwise, you will be \
    prompted)", nargs='?')

ARGS = PARSER.parse_args()

if ARGS.version:
    print(argv[0] + ", version " + SCRIPT_VERSION)
    exit(0)


print('Welcome to the Garmin Connect "Delete Activity by Device ID" Tool!')
print('')
USERNAME=''
PASSWORD=''
DEVICEID=''
while not USERNAME:
        USERNAME = ARGS.username if ARGS.username else input('Username: ')
        if not USERNAME:
                print("Please enter a username.")
                print("")
while not PASSWORD:
        PASSWORD = ARGS.password if ARGS.password else getpass()
        if not PASSWORD:
                print("Please enter a password.")
                print("")

while not DEVICEID:
        DEVICEID = ARGS.deviceid if ARGS.deviceid else input('Device ID: ')
        if not DEVICEID:
                print("Please enter a device ID.")
                print("")

DEVICEID=int(DEVICEID)

# Maximum # of activities you can search for at once (URL_GC_LIST)
LIMIT_ACTIVITY_LIST = 9999


print('')
print('WARNING: GARMIN CONNECT ACTIVITIES FOR DEVICE ' + str(DEVICEID) + " WILL BE DELETED FOREVER!")
RESPONSE = input('Type "YES" and press ENTER if you are absolutely sure: ')
if RESPONSE != 'YES':
        sys.exit(0)


print("Logging in...")

garmin = Garmin(email=USERNAME, password=PASSWORD, is_cn=False)
garmin.login()

JSON_LIST = garmin.get_activities(start=0, limit=LIMIT_ACTIVITY_LIST)

if len(JSON_LIST) == 0:
        print("No activities found for the given date range.")
else:
        print("Found " + str(len(JSON_LIST)) + " activities.")

for a in JSON_LIST:
        print('Activity: ' + a['startTimeLocal'] + (' | ' + a['activityName'] if a['activityName'] else ''))

        print('  Activity device ID = ' + str(a['deviceId']))
        if a['deviceId'] == DEVICEID:
                print('  Deleting activity!')
                garmin.delete_activity(activity_id=str(a["activityId"]))
        else:
                print('  Device ID does not match. Not deleting activity.')

print('')
print('Done!')

input('Press ENTER to quit');
