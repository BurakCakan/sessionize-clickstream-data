import pandas as pd
import requests
import json as j
from dateutil import parser


def parse(url: str):
    # used for get data from a web api and parsing a JSON object with multiple arrays
    r = requests.get(url, stream=True)

    raw_data = []
    for line in r.iter_lines():
        raw_data.append(j.loads(line.decode("utf-8")))
    return raw_data


def to_dataframe(raw_list) -> pd.DataFrame:
    # used for transforming list of dictionaries into pandas dataframe
    event_keys = set()
    for i in raw_list:
        if "event" in i.keys():
            for j in i["event"].keys():
                event_keys.add(j)
    all_keys = event_keys.copy()
    all_keys.add("id")
    all_keys.add("type")
    # all_keys store all possible column names come in derived data. It will be so important in building dataframe.

    _id = [e["id"] if "id" in e.keys() else None for e in raw_list]
    _type = [e["type"] if "type" in e.keys() else None for e in raw_list]
    customerId = [
        e["event"]["customer-id"]
        if ("event" in e.keys() and "customer-id" in e["event"].keys())
        else None
        for e in raw_list
    ]
    page = [
        e["event"]["page"]
        if ("event" in e.keys() and "page" in e["event"].keys())
        else None
        for e in raw_list
    ]
    position = [
        e["event"]["position"]
        if ("event" in e.keys() and "position" in e["event"].keys())
        else None
        for e in raw_list
    ]
    product = [
        e["event"]["product"]
        if ("event" in e.keys() and "product" in e["event"].keys())
        else None
        for e in raw_list
    ]
    query = [
        e["event"]["query"]
        if ("event" in e.keys() and "query" in e["event"].keys())
        else None
        for e in raw_list
    ]
    referrer = [
        e["event"]["referrer"]
        if ("event" in e.keys() and "referrer" in e["event"].keys())
        else None
        for e in raw_list
    ]
    timestamp = [
        parser.parse(e["event"]["timestamp"])
        if ("event" in e.keys() and "timestamp" in e["event"].keys())
        else None
        for e in raw_list
    ]
    userAgent = [
        e["event"]["user-agent"]
        if ("event" in e.keys() and "user-agent" in e["event"].keys())
        else None
        for e in raw_list
    ]
    ip = [
        e["event"]["ip"]
        if ("event" in e.keys() and "ip" in e["event"].keys())
        else None
        for e in raw_list
    ]

    df = pd.DataFrame(
        dict(
            _id=_id,
            _type=_type,
            customerId=customerId,
            page=page,
            position=position,
            product=product,
            query=query,
            referrer=referrer,
            timestamp=timestamp,
            userAgent=userAgent,
            ip=ip,
        )
    )

    return df


def validation(raw_df):
    # if customerId is null, records are eliminated here, and all records are sorted with timestamp

    raw_df.dropna(subset='customerId', inplace=True)
    raw_df.sort_values(by=['timestamp'], inplace=True)
    raw_df.insert(0, 'rn', range(0, 0 + len(raw_df)))
    raw_df.set_index("rn", inplace=True)


def calculate_sessionid(df):
    # assumption is that 30-min of unavailability means another session could start
    # That's why, I grouped events which have not more than 30 min between as a session for a customerId

    cs = []
    cust_info = {}
    last_session_all = 0
    for i in range(len(df)):
        if df['customerId'][i] not in cust_info.keys():
            cust_info[df['customerId'][i]] = [df['timestamp'][i], last_session_all + 1]
            last_session_all += 1
            cs.append(last_session_all)
        else:
            td = df['timestamp'][i] - cust_info[df['customerId'][i]][0]
            td_mins = int(round(td.total_seconds() / 60))
            if td_mins > 30: 
                cust_info[df['customerId'][i]] = [df['timestamp'][i], last_session_all + 1]
                last_session_all += 1
                cs.append(last_session_all)
            else:
                cust_info[df['customerId'][i]][0] = df['timestamp'][i]
                cs.append(cust_info[df['customerId'][i]][1])
    df['sessionId'] = cs
