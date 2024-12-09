def time_string_to_seconds(time_string):
    """
    Converts a time string to seconds.
    Supported formats:
      - 'Xm' for minutes
      - 'Xh' for hours
      - 'Xd' for days
      - 'Xw' for weeks
      - 'XM' for months (30 days assumed per month)
    Example: '15m' -> 900 seconds
             '2h'  -> 7200 seconds
    """
    unit_conversions = {
        "m": 60,             
        "h": 60 * 60,       
        "d": 24 * 60 * 60,  
        "w": 7 * 24 * 60 * 60,
        "M": 30 * 24 * 60 * 60 
    }

    for unit, multiplier in unit_conversions.items():
        if time_string.endswith(unit):
            value = int(time_string[:-len(unit)]) 
            return value * multiplier

    raise ValueError("Invalid time format. Supported units: 'm', 'h', 'd', 'w', 'mo'.")
