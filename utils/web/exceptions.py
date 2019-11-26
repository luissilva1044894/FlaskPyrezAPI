
class CustomException(Exception):
	"""
	@app.route('/foo')
	def get_foo():
		raise CustomException('This view is gone', status_code=410)
	"""
	status_code = 404

	def __init__(self, message, status_code=None, payload=None, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
		self.message = message
		if status_code:
			self.status_code = status_code
		self.payload = payload
	def jsonify(self):
		from . import is_async
		if is_async():
			from flask import jsonify
		else:
			from quart import jsonify
		response = jsonify(self.to_dict())
		response.status_code = self.status_code
		return response
	def to_dict(self):
		rv = dict(self.payload or ())
		rv['message'] = self.message
		return rv

class ChampRequired(CustomException):
	pass
class NoDeck(CustomException):
	pass
class NoChamp(CustomException):
	pass
class PlayerRequired(CustomException):
	pass
