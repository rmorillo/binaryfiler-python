from binaryfiler import BinaryFileColumns, BinaryFileHeaderFormat

class BinaryFileInfo:
    def __init__(self, file_marker):
        self.header_format = BinaryFileHeaderFormat()
        self.file_marker = file_marker
        self.header_size = 0
        self.row_size = 0
        self.row_count = 0
        self.file_marker = file_marker
        self._columns = BinaryFileColumns()

    def refresh_header(self):
        self.header_format.update_format(''.join(list(map(lambda item: item.item_type.value,
                                                                self._columns.column_info))))
