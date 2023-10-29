from typing import List
import requests as _requests
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout

import bs4 as _bs4
from fake_useragent import UserAgent

def urlopen(url: str):
    """
    Request url

    Parameters
    ----------
    url :   str
        URL

    Returns
    -------
    response or 0   :
        requests
    """
    result = 0
    ua = UserAgent()
    header = {'user-agent':ua.chrome}
    response = _requests.get(url, headers=header, timeout=3)
    try:
        response.raise_for_status()
    except ConnectionError as ce:
        print('Connection Error:', ce)
        return result
    except HTTPError as he:
        print('HTTP Error:', he)
        return result
    except Timeout as te:
        print('Timeout:', te)
        return result
    except RequestException as re:
        print('Error:', re)
        return result
    else:
        return response
