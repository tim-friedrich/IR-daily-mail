class CsvItem:
    pointer = None
    length = None

    @staticmethod
    def get_members():
        raise NotImplemented('Override this method by returning all member names')

    @classmethod
    def parse_csv_row(cls, row, pointer=None, length=None):
        cls_object = cls()
        i = 0
        for member in cls.get_members():
            cls_object.__setattr__(member, row[i])
            i += 1
        cls_object.pointer = pointer
        cls_object.length = length
        return cls_object
