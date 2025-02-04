SQL_SESSIONS = """
    select distinct ts from times
"""


# the ‘？’ placeholders are called parameterized values.
# After making the queries compatible with MariaDB, we need to change the placeholders '?' to ‘%s’.

SQL_SWIMMERS_BY_SESSION = """
    select distinct swimmers.name, swimmers.age  
    from times, swimmers 
    where date(times.ts) = %s and     
    times.swimmer_id = swimmers.id 
    order by name
"""

# below there is a date function, that converts timestamps to YYYY-MM-DD format.
SQL_SWIMMERS_EVENTS_BY_SESSION = """  
    select distinct events.distance, events.stroke
    from swimmers, events, times
    where times.swimmer_id = swimmers.id and
    times.event_id = events.id and
    (swimmers.name = %s and swimmers.age = %s) and
    date(times.ts) = %s
"""

# date(times.ts) = %s means the input date is compared to the date of the timestamp in the times table.
SQL_CHART_DATA_BY_SWIMMER_EVENT_SESSION = """
    select times.time
    from swimmers, events, times
    where (swimmers.name = %s and swimmers.age = %s) and
    (events.distance = %s and events.stroke = %s) and 
    swimmers.id = times.swimmer_id and
    events.id = times.event_id and
    date(times.ts) = %s
"""