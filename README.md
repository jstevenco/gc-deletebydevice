# gc-deletebydevice

A tool for deleting data from Garmin Connect for a specified device.  This is primarily useful in the event
that you have a device with old data from a previous user, or shared the device in a context that created 
data in your account that should not be associated with you.

## Usage
```
usage: gc-deletebydevice.py [-h] [--version] [--username [GARMIN_USERNAME]] [--password [GARMIN_PASSWORD]] [--deviceid [DEVICE_ID]] [--fromdate [DATE]] [--todate [DATE]] [--dry-run]

A tool for deleting activities with optional date range associated with a specified Garmin device ID. The intended use is to purge unwanted data from a previous device user.

options:
  -h, --help            show this help message and exit
  --version             print version and exit
  --username [GARMIN_USERNAME], -u [GARMIN_USERNAME]
                        your Garmin Connect username (otherwise, you will be prompted)
  --password [GARMIN_PASSWORD], -p [GARMIN_PASSWORD]
                        your Garmin Connect password (otherwise, you will be prompted)
  --deviceid [DEVICE_ID], -id [DEVICE_ID]
                        the device ID for activities to delete (otherwise, you will be prompted)
  --fromdate [DATE], -f [DATE]
                        the date of the first activity to delete (e.g. 2018-09-30) (otherwise, you will be prompted)
  --todate [DATE], -t [DATE]
                        the date of the last activity to delete (e.g. 2018-10-30) (otherwise, you will be prompted)
  --dry-run, -n         show what would be deleted
```

## Notes

There are a couple of ways to get the necessary device ID. The most straightforward is via the watch itself, via the Settings->System->About menu option. The number is described as the Unit ID. Another method that I have not tried is described in willnorthyork's original garmin forum post [here](https://forums.garmin.com/apps-software/mobile-apps-web/f/garmin-connect-web/165851/can-i-delete-just-the-activities-from-a-single-garmin-device-from-my-garmin-connect-account).

## Credits / Authors
* Based on a post by willnorthyork in the Garmin forums at the URL [above](https://forums.garmin.com/apps-software/mobile-apps-web/f/garmin-connect-web/165851/can-i-delete-just-the-activities-from-a-single-garmin-device-from-my-garmin-connect-account).
* Revised by Reddit user Additional-Point-824 which [removed urllib-based logic](https://www.reddit.com/r/Garmin/comments/1de5mbj/deletejusttheactivitiesfromasinglegarmindevicefrom/) and replaced it with Python [garminconnect package support](https://github.com/cyberjunky/python-garminconnect/tree/master).
