from web import create_app

app = create_app()

if __name__ == '__main__':
  app.app_context().push()
  import sys
  if sys.argv and len(sys.argv) > 1:
  	from web import create_manager
  	create_manager(app).run()
  app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])
