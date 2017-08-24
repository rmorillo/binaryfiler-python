from enum import Enum

class BinaryFileColumnType(Enum):
    Integer = 'i'
    Float = 'f'
    Bool = '?'

class BinaryFileColumn:
    def __init__(self, name, item_type):
        self._name = name
        self._item_type = item_type

    @property
    def name(self):
        return self._name

    @property
    def item_type(self):
        return self._item_type

class BinaryFileColumns:
    def __init__(self):
        self.column_info = []

    def append(self, custom_item_name=None, custom_item_type=None, custom_item=None):
        if (custom_item is None):
            self.column_info.append(BinaryFileColumn(custom_item_name, custom_item_type))
        else:
            self.column_info.append(custom_item)

    @property
    def items(self):
        return self.column_info
