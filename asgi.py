
def create_app(name=None):
	from quart import Quart
	return Quart(name or __name__)

app = create_app()

@app.route('/')
async def hello():
    return 'Hello World!'

if __name__ == '__main__':
  app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])
