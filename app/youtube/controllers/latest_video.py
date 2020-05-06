
#import requests
from bs4 import BeautifulSoup
from ...utils import get_url
def latest_video_func(channel_id):
  try:
    #soup = BeautifulSoup(requests.get(f'http://www.youtube.com/channel/{channel_id}/videos').content, 'html.parser').select_one('.yt-lockup-title a')
    soup = BeautifulSoup(get_url(f'http://www.youtube.com/channel/{channel_id}/videos'), 'html.parser').select_one('.yt-lockup-title a')
    _title, _url = soup['title'], soup['href']
  except Exception:
   pass
  else:
    return f'{_title} - https://youtu.be/{_url.replace("/watch?v=", "")}'
  return requests.get(f'https://api.crunchprank.net/youtube/latest_video?id={channel_id}').text
