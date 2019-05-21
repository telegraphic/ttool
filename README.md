# ttool
Tool for converting between astronomical time formats and between timezones.

This is a simple utility for:
1) Converting between different time formats. For example, to convert from mjd (modified julian date) to regular ISO date, run `./ttool.py 57000 mjd iso`. 
2) Doing timezone transformations between different cities / locations. The tool uses `geopy` to search for the location, 
   and will display the latitude, longitude, and local sidereal time for the location. For example, to convert a local time 
   in Sydney Australia to the local time in Berkeley California, run `./ttool.py "2017-08-01 20:00" Sydney Berkeley`.

Install via

```
pip install git+https://github.com/telegraphic/ttool
```

### Converting time formats

For converting between different time formats, run:

```
ttool [time] [input_format] [output_format] [output_format2] ...
```

Where you can have as many output formats as you like on the command line. For example:

```
dan@hadouken:ttool$ ttool 2017-01-01 iso mjd jd
             iso: 2017-01-01
             mjd: 57754.0
              jd: 2457754.5
```

The tool uses astropy, so the [supported output formats](http://docs.astropy.org/en/stable/time/#time-format) are:

```
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
```


### Timezone conversions

For converting between different timezones, run:

```
ttool [TIME] [LOCATION] [LOCATION2] ...
```

For example, to convert 07:00AM at Berkeley (today) to Melbourne time:

```
dan@hadouken:ttool$ ./ttool.py "07:00" Berkeley Melbourne
Location:  Berkeley, CA 94720, USA
Timezone:  America/Los_Angeles
Latitude:  37.8718992
Longitude: -122.2585399
Time:      2017-08-07 07:00:00-07:00
LST:       2:56:05.58


Location:  Melbourne VIC, Australia
Timezone:  Australia/Melbourne
Latitude:  -37.8136276
Longitude: 144.9630576
Time:      2017-08-08 00:00:00+10:00
LST:       20:44:58.77
```

The tool will do its best to parse the time as a string (using the `dateparse` module), so you do things like:

```
./ttool.py "08:00 tomorrow" Sydney "San Francisco"
./ttool.py "2017-01-01 09:30" local Chicago
./ttool.py now here berkeley 
```

The terms `here`, `local` and `me` are special locations you can use for conversion from local time (where your computer is) to a different timezone.

__Be careful if using vague statements like "now" that use your system clock__. If you want to know what the time is in zanzibar, type `now here zanzibar`, or `now local zanzibar`, as otherwise the code assumes the computer is in zanzibar, and your system clock will be wrong (unless you and your PC are, in fact, in zanzibar).

#### What is the local time at location X?

If you want to convert from your local timezone a shorthand is:

```
./ttool.py now berkeley
./ttool.py now here berkeley     <--- Identical output
```



### Install requirements

This package depends on:

```
pip install re            # Regular expression matching
pip install astropy       # For astronomical conversion
pip install pytz          # Timezone tool
pip install dateparser    # Cleverer date parsing
pip install tzwhere       # For converting lat/long to timezone IDs
pip install geopy         # For geo lookup of locations
pip install ephem         # For local sidereal time calculations
```
