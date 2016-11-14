class Contact:

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be str, not '%s'" % name)
        self._name = name


    def __repr__(self):
        return "<Contact: %s>" % self._name


    def name(self):
        return self._name
