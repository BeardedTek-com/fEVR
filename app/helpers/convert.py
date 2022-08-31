import pytz

class convert:
    def convertTZ(time,clockFmt=12,Timezone="America/Anchorage"):
        dt_utc = time.replace(tzinfo=pytz.UTC)
        dt = dt_utc.astimezone(pytz.timezone(Timezone))
        if clockFmt == 12:
            outformat = "%-m/%-d/%y %-I:%M:%S %p"
        else:
            outformat = "%-m/%-d/%y %H:%M:%S"
        tzString = dt.strftime(outformat).lower()
        return tzString