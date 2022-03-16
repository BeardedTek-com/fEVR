#!/usr/bin/python3


selectors={"count":"10","order":"","camera":"backyard","type":"animal","time":"","score":""}

sql = "SELECT * FROM events"
wheres = []
where = ""
sort = """ ORDER BY id DESC"""
for key in selectors:
    value=selectors[key]
    if value:
        if key == "count":
            limit = value
        elif key == "sort":
            if value == "newest":
                sort = """ ORDER BY id DESC"""
            elif value == "oldest":
                sort = """ ORDER BY id ASC"""
        elif key == "score":
            wheres.append(f"""{key}>{value}""")
        elif key == "time":
            import datetime
            time = datetime.datetime.fromtimestamp(value)
            if value[-1] == "d":
                time = time - datetime.timedelta(days=int(value.replace(value[-1],'')))
            elif value[-1] == "h":
                time = time - datetime.timedelta(hours=int(value.replace(value[-1],'')))
            elif value[-1] == "w":
                time = time - datetime.timedelta(weeks=int(value.replace(value[-1],'')))
            elif value[-1] == "y":
                days = int(value.replace(value[-1],'')) * 365
                time = time - datetime.timedelta(days=days)
                wheres.append(f"""{key}>{time}""")
        else:
            wheres.append(f"""{key}='{value}'""")
if wheres:
    x = 0
    for n in wheres:
        if x == 0:
            where = "WHERE "
        else:
            where += " AND "
        where += n
        x+=1
if int(limit) > 0:
    where += f"{sort} LIMIT {limit}"
else:
    where += f"{sort} LIMIT 10"
sql = f"""SELECT * FROM events {where};"""
print(sql)
