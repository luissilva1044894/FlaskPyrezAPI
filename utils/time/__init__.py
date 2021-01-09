#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import (
  datetime,
  timedelta,
)
try:
  import arrow
except ImportError:
  arrow = None
import re
from dateutil.relativedelta import relativedelta

from typing import (
  Tuple,
  Union,
)

def convert_delta(duration='3 hours, 17 minutes, 6 seconds'.replace(',', '')):
  parser = re.compile(
    r"((?P<years>\d+?) ?(years|year|Y|y) ?)?"
    r"((?P<months>\d+?) ?(months|month|m) ?)?"
    r"((?P<weeks>\d+?) ?(weeks|week|W|w) ?)?"
    r"((?P<days>\d+?) ?(days|day|D|d) ?)?"
    r"((?P<hours>\d+?) ?(hours|hour|H|h) ?)?"
    r"((?P<minutes>\d+?) ?(minutes|minute|M) ?)?"
    r"((?P<seconds>\d+?) ?(seconds|second|S|s))?"
  )

  '''
  #https://github.com/IAmTomahawkx/xlydn/blob/b8fdb0694bd74d5529d5a9417cc3a2db515f92ec/utils/time.py#L54
  re.compile("""(?:(?P<years>[0-9])(?: years?|y))?             # e.g. 2y
    (?:(?P<months>[0-9]{1,2})(?: months?|mo))?     # e.g. 2months
    (?:(?P<weeks>[0-9]{1,4})(?: weeks?|w))?        # e.g. 10w
    (?:(?P<days>[0-9]{1,5})(?: days?|d))?          # e.g. 14d
    (?:(?P<hours>[0-9]{1,5})(?: hours?|h))?        # e.g. 12h
    (?:(?P<minutes>[0-9]{1,5})(?: minutes?|m))?    # e.g. 10m
    (?:(?P<seconds>[0-9]{1,5})(?: seconds?|s))?    # e.g. 15s
  """, re.VERBOSE)
  '''
  match = parser.fullmatch(duration)
  if match:
    return relativedelta(**{unit: int(amount) for unit, amount in match.groupdict(default=0).items()})#{'years':0,'months':0,'weeks':0,'days':0,'hours':3,'minutes':17,'seconds':6}
    #return relativedelta(hours=+3, minutes=+17, seconds=+6)

def format_dt(date, date_format=None):
  if not date_format or hasattr(date, 'isoformat'):
    return date.isoformat()
  return get_timestamp(date_format, date)

def format_timestamp(timestamp, date_format='MMMM D, YYYY'):
  if arrow:
    try:
      _timestamp = arrow.get(timestamp, date_format)
    except (arrow.parser.ParserMatchError, arrow.parser.ParserError):
      pass
    else:
      return _timestamp.isoformat()#2019-11-18T18:36:32+00:00
      #_timestamp.format('DD-MMM-YYYY HH:mm:SS ZZ') # 2019-11-12T23:31Z

def get_timestamp(date_format='%Y-%m-%d %H:%M:%S', date=None):
  if not date:
    return datetime.now().strftime(date_format)
  return date.strftime(date_format)

def to_local_time(date, tzinfo=None):
  if not tzinfo:
    return date
  return date.astimezone(tzinfo).replace(tzinfo=None)

def last_seen(locale, date):
  if arrow:
    c = arrow.utcnow() - date
    if c.days:
      return arrow.utcnow().shift(days=-c.days, seconds=c.seconds, microseconds=c.microseconds).humanize(locale=locale)
    if c.seconds:
      return arrow.utcnow().shift(seconds=-c.seconds).humanize(locale=locale)
    return arrow.utcnow().shift(microseconds=c.microseconds).humanize(locale=locale)
  delta = datetime.utcnow() - date
  hours, remainder = divmod(int(delta.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)
  years, days = divmod(days, 365)
  fmt = '{y}y, {d}d' if years else '{d}d, {h}h' if days else '{h}h, {m}m' if hours else '{m}m, {s}s'
  return fmt.format(y=years, d=days, h=hours, m=minutes, s=seconds)

def format_time(delta_time: Union[timedelta, float]):
  """https://github.com/Naxesss/Aiess/blob/db66427c589e46a5d0619ed789f6e6468d6c351e/bot/formatter.py#L381"""
  if hasattr(delta_time, 'total_seconds'):
    total_ms = delta_time.total_seconds() * 1000
  else:
    total_ms = delta_time * 1000

  years, total_ms = divmod(total_ms, 365*24*60*60*1000)
  months, total_ms = divmod(total_ms, 30*24*60*60*1000)
  weeks, total_ms = divmod(total_ms, 7*24*60*60*1000)
  days, total_ms = divmod(total_ms, 24*60*60*1000)
  hours, total_ms = divmod(total_ms, 60*60*1000)
  minutes, total_ms = divmod(total_ms, 60*1000)
  seconds, total_ms = divmod(total_ms, 1000)
  milliseconds, total_ms = divmod(total_ms, 1)
  microseconds, total_ms = divmod(total_ms, 0.001)

  return {'years':years,'months':months,'weeks':weeks,'days':days,'hours':hours,'minutes':minutes,'seconds':seconds,'milliseconds':milliseconds,'microseconds':microseconds}
