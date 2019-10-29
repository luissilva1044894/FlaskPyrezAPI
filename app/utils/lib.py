def import_from(module, name=None):
    """Generalized importer."""
    try:
    	import importlib
    	return importlib.import_module(module)
    except ImportError:
    	module = __import__(module, fromlist=[name])
    	print(f'Loaded: {module}.{name}')
    	if name:
    		return getattr(module, name)
    	return module
