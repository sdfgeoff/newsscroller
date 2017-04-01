import json

class SettingFile(object):
    def __init__(self, path, defaults):
        self._defaults = defaults
        self._path = path
        self._data = dict()
        self._callbacks = dict()
        for setting in defaults:
            self._callbacks[setting] = callback_assist()

        self.load()

    def load(self):
        '''Attempts to load the file'''
        try:
            new_data = json.load(open(self._path))
        except:
            json.dump(
                self._defaults,
                open(self._path, 'w'),
                indent=2,
                sort_keys=True
            )
            new_data = self._defaults.copy()

        for setting in self._defaults:
            if setting in new_data:
                self[setting] = new_data[setting]
            else:
                self[setting] = self._defaults[setting]

    def save(self):
        json.dump(
            self._data,
            open(self._path, 'w'),
            indent=2,
            sort_keys=True
        )

    def register_callback(self, setting_name, funct, args=None):
        self._callbacks[setting_name].add_callback(funct, args)

    def __getitem__(self, *args):
        return self._data.get(*args)

    def __setitem__(self, key, val):
        if key not in self._defaults:
            raise ValueError('Unknown Setting')
        else:
            self._data[key] = val
            self._callbacks[key].fire()
            self.save()

    def __str__(self):
        return "Settings in {}: {}".format(self._path, self._data)

    def __repr__(self):
        return "setting_file({}, {})".format(self._path, self._defaults)


class callback_assist(object):
    '''This class represents a function with arguments'''
    def __init__(self):
        self.callbacks = list()

    def add_callback(self, funct, args=None):
        '''Adds a new callback'''
        if args == None:
            args = list()
        self.callbacks.append((funct, args))

    def fire(self):
        '''Fires all the callbacks'''
        for funct, args in self.callbacks:
            funct(*args)

