
from ...utils import get_url
def patch_notes_func():
  _updates_posts = get_url('https://cms.paladins.com/wp-json/api/get-posts/1?&search=update%20notes')
  if _updates_posts and isinstance(_updates_posts, list) and len(_updates_posts) > 0:
    _title = _updates_posts[0]['title']
    _patch_notes = get_url(f'https://cms.paladins.com/wp-json/api/get-posts/1?&search={_title[:_title.rfind("update") - 1]}')
    if _patch_notes and isinstance(_patch_notes, list) and len(_patch_notes) > 0:
      _patch_notes = _patch_notes[-1]
      return f"{_patch_notes['title']} - https://paladins.com/news/{_patch_notes['slug']}"
