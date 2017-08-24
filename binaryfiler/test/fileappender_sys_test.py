from binaryfiler import BinaryFileAppender, BinaryFileInfo, BinaryFileColumnType
import tempfile

def test_write():
        fileName= createFile()
        assert(True)

def createFile():
    tempFile = tempfile.mktemp()
    print(tempFile)
    file_info = BinaryFileInfo('xyz')
    file_info._columns.append("entry_price", BinaryFileColumnType.Float)
    file_info.refresh_header()

    appender = BinaryFileAppender(tempFile, file_info)
    appender.open()
    for x in range(1, 100):
        appender.append(2)
    appender.close()
    return tempFile
