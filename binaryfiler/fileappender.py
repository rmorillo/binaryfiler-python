import struct

class BinaryFileAppender:
    def __init__(self, file_name, file_info):
        self._file_name = file_name
        self._file_info = file_info
        self._file = None

    def append(self, *args):
        row_data = struct.pack(self._file_info.header_format.format, *args)
        self._file.write(row_data)

    def open(self):
        self._file = open(self._file_name, 'wb')
        file_marker = self._file_info.file_marker.ljust(8, ' ')
        byte_marker = bytes(file_marker, 'ascii')
        self._file.write(byte_marker)
        header_size = len(self._file_info.header_format.format)
        header = struct.pack('ii' + str(header_size) + 's', self._file_info.header_format.row_size, header_size,
                             bytes(self._file_info.header_format.format, 'ascii'))
        self._file.write(header)

    def close(self):
        self._file.close()
