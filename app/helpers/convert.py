import pytz

class convert:
    def convertTZ(time,clockFmt=12,Timezone="America/Anchorage",format="%m/%d/%y %I:%M:%S %p",purpose="display"):
        dt_utc = time.replace(tzinfo=pytz.UTC)
        dt = dt_utc.astimezone(pytz.timezone(Timezone))
        if clockFmt == 12:
            if purpose == "display":
                format = "%m/%d/%y %I:%M:%S %p"
            elif purpose == "filename":
                format = "%m-%d-%y_%I-%M-%S_%p"
        else:
            if purpose == "display":
                format = "%m/%d/%y %H:%M:%S"
            elif purpose == "filename":
                format = "%m-%d-%y_%H-%M-%S"
        tzString = dt.strftime(format).lower()
        return tzString