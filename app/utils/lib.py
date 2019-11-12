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

def import_string(import_name, silent=False):
    """Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).
    If the `silent` is True the return value will be `None` if the import
    fails.
    :return: imported object
    """
    try:
        if ':' in import_name:
            module, obj = import_name.split(':', 1)
        elif '.' in import_name:
            module, _, obj = import_name.rpartition('.')
        else:
            return __import__(import_name)
        return getattr(__import__(module, None, None, [obj]), obj)
    except (ImportError, AttributeError):
        if not silent:
            raise
