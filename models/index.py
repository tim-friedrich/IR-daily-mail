class Index(dict):
    def __init__(self, file=None, **kwargs):
        super().__init__(**kwargs)
        self.file = file

    def get_file(self):
        if self.file:
            return self.file
