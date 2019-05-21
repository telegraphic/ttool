#!/usr/bin/env python
"""
# tz_convert.py

Command line utility toonvert between timezones, julian dates, and the like.
"""
import sys
from astropy.time import Time
from datetime import datetime
import dateparser
import pytz
from tzwhere.tzwhere import tzwhere
import tzlocal
from geopy import geocoders
import re
import ephem

try:
    time_str      = sys.argv[1].strip()
    loc_in_str    = sys.argv[2].lower().strip()
except IndexError:
    print("USAGE: tconv TIME [LOCATION] [LOCATION2] ...")
    sys.exit()


def convert_time(tval, format_in, format_out='iso'):
    """ Convert a time value in a given input format to output format 
    
    Args:
        tval (str or float): time value to convert
        format_in (str): time format for given time value
        format_out (str): time format for output. Defaults to ISO
    
    Returns:
        tval_out (str or float): Time after conversion into format_out

    Notes:
        Format codes are as defined in Astropy's Time() class:
        http://docs.astropy.org/en/stable/time/#time-format
    
    Format      Class	                    Example argument
    --------------------------------------------------------------------
    byear       TimeBesselianEpoch          1950.0
    byear_str   TimeBesselianEpochString    'B1950.0'
    cxcsec      TimeCxcSec                  63072064.184
    decimalyear TimeDecimalYear             2000.45
    fits        TimeFITS                    '2000-01-01T00:00:00.000(TAI)'
    gps         TimeGPS                     630720013.0
    iso         TimeISO                     '2000-01-01 00:00:00.000'
    isot        TimeISOT                    '2000-01-01T00:00:00.000'
    jd          TimeJD                      2451544.5
    jyear       TimeJulianEpoch             2000.0
    jyear_str   TimeJulianEpochString       'J2000.0'
    mjd         TimeMJD                     51544.0
    plot_date   TimePlotDate                730120.0003703703
    unix        TimeUnix                    946684800.0
    yday        TimeYearDayTime	            2000:001:00:00:00.000
    --------------------------------------------------------------------
    
    """
    t = Time(tval, format=format_in)
    tval_out = getattr(t, format_out)
    return tval_out

################
## Simple conversions to UTC
###############

decimal_fmts  = ('mjd', 'jd', 'unix', 'jyear', 'gps', 'decimalyear', 'cxcsec', 'byear')
string_fmts   = ('iso', 'isot', 'fits', 'byear_str', 'jyear_str')
local_strings = ('local', 'here', 'me')
    
is_format_conversion = False

if loc_in_str in decimal_fmts:
    tval = float(time_str)
    is_format_conversion = True

if loc_in_str in string_fmts:
    tval = time_str
    is_format_conversion = True
    
if is_format_conversion:
    print("%16s: %s" % (loc_in_str, tval))
    
    if len(sys.argv) == 3:
        format_out = 'iso'
        convert_time(tval, loc_in_str, format_out)
    else:
        for ii in range(3, len(sys.argv)):
            format_out = sys.argv[ii]
            tval_out = convert_time(tval, loc_in_str, format_out)
            print("%16s: %s" % (format_out, tval_out))
        format_out = sys.argv[3]

    sys.exit()

else:
    
    ################
    ## Location info 
    ###############

    # Load these at first run
    #G = geocoders.GoogleV3()
    G = geocoders.Nominatim()
    W = tzwhere()

    def get_timezone(location_str, print_loc=True):
        """ Get the timezone for a given string 
    
        Does a geopy search for the string and returns 
        the corresponding timezone match.
    
        Args:
            location_str (str): Location as plaintext string
            print_loc (bool): Print interpreted location
        """
        place, (lat, lng) = G.geocode(location_str)
        tz_str = W.tzNameAt(lat, lng)
        if print_loc:
            print("Location:  %s" % place)
            print("Timezone:  %s" % tz_str)
            print("Latitude:  %s" % lat)
            print("Longitude: %s" % lng)
        return tz_str, place, lat, lng 

    def get_sidereal_time(lat, lng, dt):
        """ Get sidereal time for a given lat, long, datetime """
        obs = ephem.Observer()
        obs.long = str(lng)
        obs.lat  = str(lat)
        obs.date = dt.astimezone(pytz.utc)
        return obs.sidereal_time()

    # Get the timezone for the input location
    if loc_in_str in local_strings:
        tz_in = tzlocal.get_localzone()
    else:
        tz_in_str, place_in, lat_in, lng_in = get_timezone(loc_in_str)
        tz_in       = pytz.timezone(tz_in_str)

    # Parse the date/time string
    # Catch HH:MM before attempting auto date parse
    match = re.search('^(?P<hr>\d+):(?P<min>\d+)', time_str)
    if match:
        d = match.groupdict()
        hh, mm = int(d['hr']), int(d['min'])
        # assume it's today's time
        now = datetime.now()
        t     = datetime(now.year, now.month, now.day, hh, mm)
        t     = tz_in.localize(t)
    else:
        t = dateparser.parse(time_str)
        #tz_local = tzlocal.get_localzone()     # Need to attach local timezone!
        t = tz_in.localize(t)

        t_in  = t.astimezone(tz_in)
    print("Time:      %s" % t_in)
    if not loc_in_str in local_strings:
        print("LST:       %s" % get_sidereal_time(lat_in, lng_in, t_in))
    print("\n")
    
    ################
    ## Do conversion into new timezone
    ###############

    for ii in range(3, len(sys.argv)):
        loc_out_str = sys.argv[ii]
        
        tz_out_str, place_out, lat_out, lng_out   = get_timezone(loc_out_str)
        tz_out      = pytz.timezone(tz_out_str) 
        t_out = t_in.astimezone(tz_out)
        print("Time:      %s" % t_out)
        print("LST:       %s" % get_sidereal_time(lat_out, lng_out, t_out))
        print("\n")
    sys.exit()

