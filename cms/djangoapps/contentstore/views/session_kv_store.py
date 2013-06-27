from xblock.runtime import KeyValueStore, InvalidScopeError

class SessionKeyValueStore(KeyValueStore):
    def __init__(self, request, model_data):
        self._model_data = model_data
        # self._session = request.session
        self._session = None

    def get(self, key):
        try:
            return self._model_data[key.field_name]
        except (KeyError, InvalidScopeError):
            self.why_sessions(key,caller="get")
            raise KeyError
            return None

    def set(self, key, value):
        try:
            self._model_data[key.field_name] = value
        except (KeyError, InvalidScopeError):
            self.why_sessions(key,value, caller="set")
            # self._session[tuple(key)] = value

    def delete(self, key):
        try:
            del self._model_data[key.field_name]
        except (KeyError, InvalidScopeError):
            self.why_sessions(key,caller="delete")
            del self._session[tuple(key)]

    def has(self, key):
        return key in self._model_data or key in self._session

    def why_sessions(self,key,value=None,caller=":("):
        # traceback.print_stack()
        fp = open('/Users/irh/Desktop/out.txt', 'a')
        msg = "\n<==== Key, Value from "+caller+" look like =====>\n"
        msg += str(tuple(key))+" - "+str(value) + "\n"
        # msg += str(self._session[tuple(key)])
        msg += "\n<========>\n"

        fp.write(msg)
        fp.close()
