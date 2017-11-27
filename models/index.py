class Index(dict):
    def __init__(self, file=None, **kwargs):
        super().__init__(**kwargs)
        self.file = file

    def get_file(self):
        if self.file:
            return self.file

    def get_starts_with(self, key_part):
        postings = []
        for key in [key for key in self if key.startswith(key_part)]:
            postings.append(self.get(key))
        return postings
