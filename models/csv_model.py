class CsvItem:
    pointer = None
    length = None
    token_position = None

    @staticmethod
    def get_members():
        raise NotImplemented('Override this method by returning all member names')

    @classmethod
    def parse_csv_row(cls, row, pointer=None, length=None, token_position=None):
        cls_object = cls()
        i = 0
        for member in cls.get_members():
            cls_object.__setattr__(member, row[i])
            i += 1
        cls_object.pointer = pointer
        cls_object.length = length
        cls_object.token_position = token_position
        return cls_object

    def get_dict(self):
        object_dict = {}
        for member in self.__class__.get_members():
            object_dict[member] = self.__getattribute__(member)
        return object_dict
