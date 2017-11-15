class CsvModel:
    pointer = None

    @staticmethod
    def get_members():
        raise NotImplemented('Override this method by returning all member names')

    @classmethod
    def parse_csv_row(cls, row, line_number):
        cls_object = cls()
        i = 0
        for member in cls.get_members():
            cls_object.__setattr__(member, row[i])
            i += 1
        cls_object.pointer = line_number
        return cls_object
