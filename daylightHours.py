import datetime as _dt
from zoneinfo import ZoneInfo

from typing import Dict

from fake_useragent import UserAgent
import ephem as _ephem

def get_daylightHours(lon: float, lat: float, elevation: int, date: _dt.date) -> Dict:
    """
    Hours of from sunrise to sunset

    Parameters
    ----------
    lon :   float
        東経
    lat :   float
        北緯
    elevation :   int
        高度
    date :  datetime
        日付

    Returns
    -------
    Hours   :   float
        Dict()
    """
    JST = ZoneInfo('Asia/Tokyo')        # タイムゾーン(日本)
    UTC = ZoneInfo('UTC')               # タイムゾーン(標準時間)

    location = _ephem.Observer()        # 観測値を美山観測所
    location.lon = str(lon)             # 東経
    location.lat = str(lat)             # 北緯
    location.elevation = elevation      # 高度
    location.date = _dt.datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=JST)

    sun = _ephem.Sun()                  # 太陽をインスタンス化
    sunrise = _ephem.to_timezone(location.next_rising(sun), JST)   # 次の日昇時刻(時刻は世界時)
    sunset = _ephem.to_timezone(location.next_setting(sun), JST)   # 次の日没時刻(時刻は世界時)
    td = sunset - sunrise               # 差分(可照時間)

    return round(td.seconds/3600, 1)
