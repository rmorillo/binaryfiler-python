import struct

class BinaryFileHeaderFormat:
    def __init__(self):
        self.format = None
        self.row_size = None

    def update_format(self, struct_format):
        self.format = struct_format
        self.row_size = struct.calcsize(struct_format)