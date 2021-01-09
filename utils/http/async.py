import aiohttp

from ..num import try_int

async def get_page(url: str):
  """https://github.com/matcool/schezo-bot/blob/rewrite/cogs/utils/http.py"""
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      return await response.read()

async def get_headers(url: str):
  async with aiohttp.ClientSession() as session:
    async with session.head(url) as response:
      return response.headers

async def get_file_size(url: str) -> int:
  headers = await get_headers(url)
  return try_int(headers.get('Content-Length'), -1)

async def get_file_type(url: str) -> str:
  headers = await get_headers(url)
  return headers.get('Content-Type')

async def post_request(url, data, headers):
  resp = await client.loop.run_in_executor(None, functools.partial(requests.post, url, json=data, headers=headers))
  if not resp:
    logging.error(f'Posting stats failed with {resp.status_code} because {resp.content}')
