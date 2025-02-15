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

script_version = '0.0.3'

def prompt_date(prompt, default_value):
    """get data range value interactively"""
    while True:
        targetDate = default_value if default_value else input(prompt)
        if not targetDate or type(targetDate) == datetime:
            break
        try:
            datetime.strptime(targetDate, '%Y-%m-%d')
        except ValueError:
            print('Invalid date.')
            continue
        break
    return targetDate

def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description = (
            "A tool for deleting activities with optional date range "
            "associated with a specified Garmin device ID. The intended "
            "use is to purge unwanted data from a previous device user."
            )
    )

    def date_parser(date_string):
        try:
            targetDate = datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            print('Invalid date.')
            exit(0)
        return targetDate

    parser.add_argument('--version',
                        help="print version and exit",
                        action="store_true")
    parser.add_argument('--username', '-u',
                        type=str,
                        metavar="GARMIN_USERNAME",
                        help="your Garmin Connect username (otherwise, \
                        you will be prompted)",
                        nargs='?')
    parser.add_argument('--password', '-p',
                        type=str,
                        metavar="GARMIN_PASSWORD",
                        help="your Garmin Connect password (otherwise, \
                        you will be prompted)",
                        nargs='?')
    parser.add_argument('--deviceid', '-d',
                        type=int,
                        metavar="DEVICE_ID",
                        help="the device ID for activities to delete (otherwise, \
                        you will be prompted)",
                        nargs='?')
    parser.add_argument('--fromdate', '-f',
                        type=date_parser,
                        help="the date of the first activity to delete \
                        (e.g. 2018-09-30) (otherwise, you will be prompted)",
                        metavar="DATE",
                        nargs='?')
    parser.add_argument('--todate', '-t',
                        type=date_parser,
                        help="the date of the last activity to delete \
                        (e.g. 2018-10-30) (otherwise, you will be prompted)",
                        metavar="DATE",
                        nargs='?')

    args = parser.parse_args()
    if args.version:
        print(argv[0] + ", version " + script_version )
        exit(0)

    return args

args = get_args()

print('Welcome to the Garmin Connect "Delete Activity by Device ID" Tool!')
print('')

username = ''
password = ''
device_id = ''

while not username:
    username = args.username if args.username else input('Username: ')
    if not username:
        print('Please enter a username.')
        print('')
while not password:
    password = args.password if args.password else getpass()
    if not password:
        print('Please enter a password.')
        print('')
while not device_id:
    device_id = args.deviceid if args.deviceid else input('Device ID: ')
    if not device_id:
        print('Please enter a device ID.')
        print('')
    try:
        device_id = int(device_id)
    except ValueError:
        print('Device ID must be an integer.')
        device_id = None

from_date = prompt_date('Start Date (e.g. 2018-09-30 or blank for oldest activity): ',
                       args.fromdate)
if not from_date:
    from_date = date.min
to_date = prompt_date('End Date (e.g. 2018-10-30 or blank for today): ',
                     args.todate)
if not to_date:
    to_date = date.today()

print(f'WARNING: Garmin Connect activities for device {device_id}'
      f' will be deleted forever!')
response = input('Type "YES" and press ENTER if you are absolutely sure: ')
if response != 'YES':
    sys.exit(0)
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
