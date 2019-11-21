
class CustomException(Exception):
  pass
class ChampRequired(CustomException):
    pass
class NoDeck(CustomException):
	pass
class NoChamp(CustomException):
	pass
class PlayerRequired(CustomException):
	pass
