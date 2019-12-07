
def get_timestamp(_format='%Y-%m-%d %H:%M:%S'):
  from datetime import datetime
  return datetime.now().strftime(_format)

def format_timestamp(timestamp, _format='MMMM D, YYYY'):
  try:
    import arrow
    try:
      _timestamp = arrow.get(timestamp, _format)
    except (arrow.parser.ParserMatchError, arrow.parser.ParserError):
      pass
    else:
      return _timestamp.isoformat()#2019-11-18T18:36:32+00:00
      #_timestamp.format('DD-MMM-YYYY HH:mm:SS ZZ') # 2019-11-12T23:31Z
  except importError:
    pass

def last_seen(locale, date):
  try:
    import arrow
  except ImportError:
    from datetime import datetime
    delta = datetime.utcnow() - date
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365)
    fmt = '{y}y, {d}d' if years else '{d}d, {h}h' if days else '{h}h, {m}m' if hours else '{m}m, {s}s'
    return fmt.format(y=years, d=days, h=hours, m=minutes, s=seconds)
  else:
    c = arrow.utcnow() - date
    if c.days:
      return arrow.utcnow().shift(days=-c.days, seconds=c.seconds, microseconds=c.microseconds).humanize(locale=locale)
    if c.seconds:
      return arrow.utcnow().shift(seconds=-c.seconds).humanize(locale=locale)
    return arrow.utcnow().shift(microseconds=c.microseconds).humanize(locale=locale)
