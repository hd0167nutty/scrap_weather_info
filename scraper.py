import datetime as _dt
import json as _json

from typing import Dict, List
import bs4 as _bs4

import daylightHours as _daylight
import urlopen as _urlopen

def _generate_forecasts_url(area: str) -> str:
    url = f"https://weather.tsukumijima.net/api/forecast/city/{area}"
    return url

def _generate_rainFlag_url(tag_id: str) -> str:
    url = f"https://tenki.jp/forecast/6/29/6110/26213/3hours.html{tag_id}"
    return url
def _edit_json_contents(json_data: _json) -> Dict:
    contents = dict()

    contents["date"] = json_data["date"] #日付
    contents["weather"] = json_data['image']["title"] # 天気
    contents["weatherURL"] = json_data['image']["url"] # 天気画像
    contents["weatherDetail"] = json_data["detail"]['weather'] #天気詳細
    contents["maxTemp"] = json_data['temperature']["max"]['celsius'] # 最高気温
    contents["minTemp"] = json_data['temperature']["min"]['celsius'] # 最高気温
    return contents

def _scraping_info_forecasts() -> Dict:
    area = "260020" # 詳細の予報エリア番号 - 舞鶴観測所
    url = _generate_forecasts_url(area)
    response = _urlopen.urlopen(url)
    if ('forecasts' in response.json())==True:
        # jsonData = response.json()['forecasts'][1]
        jsonData = _edit_json_contents(response.json()['forecasts'][1])
    else:
        jsonData = "Error"
    return jsonData

def _scraping_info_rainFlag() -> List:
    tag_id = '#forecast-point-3h-tomorrow'
    url = _generate_rainFlag_url(tag_id)
    response = _urlopen.urlopen(url)
    if response != 0:
        html = response.text.encode(response.encoding)
        soup = _bs4.BeautifulSoup(html, "lxml")
        # 降水量(3時間ごと 3,6,9,12,15,18,21,24時)
        # id:#forecast-point-3h-tomorrow, 子要素class:precipitation, 子要素td
        elements = soup.select(f'{tag_id} > .precipitation > td')
        rainFlag = []
        for i, element in enumerate(elements):
            j = int(element.text.strip())
            rainFlag.append(0 if j <2 else 0)
        # rainFlag = dict()
        # for i, element in enumerate(elements):
        #     time_3h = 0+3*i
        #     j = int(element.text.strip())
        #     rainFlag[time_3h] = 0 if j <2 else 0
    else:
        rainFlag = "Error"

    return rainFlag

def create_forecasts_dict():
    date = _dt.date.today() + _dt.timedelta(days=1)
    forecasts = dict()
    forecasts['forecasts'] = _scraping_info_forecasts()
    forecasts['rainFlag'] = _scraping_info_rainFlag()
    forecasts['daylightHours'] = _daylight.get_daylightHours(135.550, 35.275, 200, date)
    return forecasts

if __name__ == "__main__":
    forecasts = create_forecasts_dict()
    with open("forecasts.json", mode="w", encoding='utf-8') as file:
        _json.dump(forecasts, file, ensure_ascii=False)
