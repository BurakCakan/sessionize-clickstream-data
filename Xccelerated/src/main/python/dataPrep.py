import pandas as pd
import requests
import json as j
from dateutil import parser


def parse(url):
    r = requests.get(url, stream=True)

    raw_data = []
    for line in r.iter_lines():
        raw_data.append(j.loads(line.decode("utf-8")))
    return raw_data


def to_dataframe(raw_list) -> pd.DataFrame:
    event_keys = set()
    for i in raw_list:
        if "event" in i.keys():
            for j in i["event"].keys():
                event_keys.add(j)
    all_keys = event_keys.copy()
    all_keys.add("id")
    all_keys.add("type")

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
    df.set_index("_id", inplace=True)

    return df


def validation(raw_df):
    raw_df.dropna(subset='customerId', inplace=True)
    raw_df.sort_values(by=['timestamp'], inplace=True)


def calculate_sessionid(df):
    df['sessionId'] = df.groupby(['customerId', pd.Grouper(key='timestamp', freq='0.5H')], sort=False).ngroup()

    return df
