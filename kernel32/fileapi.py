import ctypes

# Defines
LPOVERLAPPED = ctypes.wintypes.LPVOID

# Bindings
k32_dll = ctypes.windll.kernel32

FlushFileBuffers = k32_dll.FlushFileBuffers
FlushFileBuffers.restype = ctypes.wintypes.BOOL
FlushFileBuffers.argtypes = [ctypes.wintypes.HANDLE]

WriteFile = k32_dll.WriteFile
WriteFile.restype = ctypes.wintypes.BOOL
WriteFile.argtypes = [ctypes.wintypes.HANDLE,ctypes.wintypes.LPCVOID,ctypes.wintypes.DWORD,ctypes.wintypes.LPDWORD,LPOVERLAPPED]

ReadFile = k32_dll.ReadFile
ReadFile.restype = ctypes.wintypes.BOOL
WriteFile.argtypes = [ctypes.wintypes.HANDLE,ctypes.wintypes.LPVOID,ctypes.wintypes.DWORD,ctypes.wintypes.LPDWORD,LPOVERLAPPED]

DeleteFileW = k32_dll.DeleteFileW
DeleteFileW.restype = ctypes.wintypes.BOOL
DeleteFileW.argtypes = [ctypes.wintypes.LPCWSTR]


def read_file(hFile,amount):
    read_data = (ctypes.c_ubyte * amount)()
    out_data = None
    cbRead = ctypes.c_ulong(0)
    res = ReadFile(hFile,read_data,amount, ctypes.byref(cbRead),None)
    if res:
        out_data = read_data[:cbRead.value]
    return res,out_data

def write_file(hFile,data):
    cbWritten = ctypes.c_ulong(0)
    res = WriteFile(hFile,data,len(data),ctypes.byref(cbWritten),None)
    return res,cbWritten

def flush_file_buffers(hFile):
    return FlushFileBuffers(hFile)

def delete_file(file_path):
    return DeleteFileW(file_path)

