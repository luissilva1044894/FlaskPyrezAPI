
def func(champ_name, player_id, _api, lang=1, nodeck_exc=Exception, nochamp_exc=Exception):
  from utils import get_champ_names, fix_champ_name
  champ_name, __champs__ = fix_champ_name(champ_name), get_champ_names()
  if not champ_name in __champs__:
    raise nochamp_exc
  from utils.flask import get_lang_id
  p_loadouts = _api.getPlayerLoadouts(player_id, get_lang_id(int(lang)))
  if len(p_loadouts) <= 1:
    raise nodeck_exc
  cds = ''
  loadouts = [p_loadout for p_loadout in p_loadouts if fix_champ_name(p_loadout.godName) == champ_name]
  for loadout in loadouts:
    cardStr = '{}{}: {}'.format (' ' if len(cds) == 0 else ' · ', loadout.deckName, ['{0} {1}'.format(card.itemName, card.points) for card in loadout.cards]).replace("'", "")
    if len(cds + cardStr) <= 400: cds += cardStr
  if cds != '':
    return cds
  raise nodeck_exc
