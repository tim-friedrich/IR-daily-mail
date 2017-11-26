class Index(dict):
    def __init__(self, file=None, **kwargs):
        super().__init__(**kwargs)
        self.file = file

    def get_file(self):
        if self.file:
            return self.file

    def get_starts_with(self, key_part):
        for key in [key.startswith(key_part) for key in self]:
            yield self.get(key)
