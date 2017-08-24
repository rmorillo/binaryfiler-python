class BinaryFileReaderContext:
    def __init__(self, file_name, file_info):
        self._file_info = file_info
        self._file_name = file_name
        self._file = None

    def __enter__(self):
        self._file = open(self._file_name, 'rb')
        byte_marker = self._file.read(8)
        marker = byte_marker.decode('ascii').strip()
        if marker != self._file_info.file_marker:
            raise Exception('Not a {} file!'.format(marker))

        row_size = int.from_bytes(self._file.read(4), byteorder='little')
        if row_size != self._file_info.header_format.row_size:
            raise Exception('Invalid row size!')

        header_size = int.from_bytes(self._file.read(4), byteorder='little')
        row_format = self._file.read(header_size)
        row_format_string = row_format.decode('ascii')
        if row_format_string != self._file_info.header_format.format:
            raise Exception('Invalid row format!')

        self._file_info.header_size = header_size
        self._file_info.rowSize = row_size

        current_position = self._file.tell()
        self._file.seek(0, 2)
        last_position = self._file.tell()
        self._file.seek(current_position)
        self._file_info.row_count = (last_position - current_position) / row_size

        self._is_file_open = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()
        self._is_file_open = False

    @property
    def reader(self):
        return self._file


class BinaryFileReader:
    def __init__(self, file_name, file_info):
        self._file_name = file_name
        self._file_info = file_info
        self._file = None
        self._is_file_open = False
        self._file_context = None

    def open(self):
        self._file_context = BinaryFileReaderContext(self._file_name, self._file_info)
        return self._file_context

    def _read(self):
        byte_data = self._file_context.reader.read(self._file_info.header_format.row_size)

        if len(byte_data) == 0:
            return None
        else:
            return struct.unpack(self._file_info.header_format.format, byte_data)

    def read(self):
        data = self._read()
        if data is None:
            return None
        else:
            return data

    def read_all(self):
        if not self._file_context._is_file_open:
            raise Exception("File is not open.")
        result = self._read()
        while result is not None:
            yield result
            result = self._read()

    def read_next(self, count):
        if not self._file_context._is_file_open:
            raise Exception("File is not open.")

        counter = 0
        result = self._read()
        while result is not None and counter < count:
            counter += 1
            yield result
            result = self._read()

    def close(self):
        if self._file_context._is_file_open:
            self._file_context.reader._file.close()
            self._file_context.reader._is_file_open = False
