import ctypes

from .handleapi import close_handle
from .fileapi import flush_file_buffers
from .fileapi import write_file
from .fileapi import read_file

# Bindings
k32_dll = ctypes.windll.kernel32

# Defines
PIPE_ACCESS_DUPLEX    = 0x00000003
PIPE_TYPE_MESSAGE     = 0x00000004
PIPE_READMODE_MESSAGE = 0x00000002
PIPE_WAIT = 0
PIPE_UNLIMITED_INSTANCES = 0x000000FF
NMPWAIT_USE_DEFAULT_WAIT = 0
INVALID_HANDLE_VALUE = -1
ERROR_PIPE_CONNECTED = 535

# DataTypes
LPSECURITY_ATTRIBUTES = ctypes.wintypes.LPVOID
LPOVERLAPPED = ctypes.wintypes.LPVOID

# Functions
CreateNamedPipeW = k32_dll.CreateNamedPipeW
CreateNamedPipeW.restype = ctypes.wintypes.HANDLE
CreateNamedPipeW.argtypes = [ctypes.wintypes.LPCWSTR,ctypes.wintypes.DWORD,ctypes.wintypes.DWORD,ctypes.wintypes.DWORD,ctypes.wintypes.DWORD,ctypes.wintypes.DWORD,ctypes.wintypes.DWORD,LPSECURITY_ATTRIBUTES ]

ConnectNamedPipe = k32_dll.ConnectNamedPipe
ConnectNamedPipe.restype = ctypes.wintypes.BOOL
ConnectNamedPipe.argtypes = [ctypes.wintypes.HANDLE, LPOVERLAPPED]

DisconnectNamedPipe = k32_dll.DisconnectNamedPipe
DisconnectNamedPipe.restype = ctypes.wintypes.BOOL
DisconnectNamedPipe.argtypes = [ctypes.wintypes.HANDLE]

SetDllDirectoryW = k32_dll.SetDllDirectoryW
SetDllDirectoryW.restype = ctypes.wintypes.BOOL
SetDllDirectoryW.argtypes = [ctypes.wintypes.LPCWSTR]

CreateSymbolicLinkW = k32_dll.CreateSymbolicLinkW
CreateSymbolicLinkW.restype = ctypes.wintypes.BOOL
CreateSymbolicLinkW.argtypes = [ctypes.wintypes.LPCWSTR,ctypes.wintypes.LPCWSTR,ctypes.wintypes.DWORD]




def create_message_pipe(pipe_name,nMaxInstances=PIPE_UNLIMITED_INSTANCES, nOutBufferSize=0x800,nInBufferSize=0x800,nDefaultTimeOut=NMPWAIT_USE_DEFAULT_WAIT):
    lpName = pipe_name
    dwOpenMode = PIPE_ACCESS_DUPLEX
    dwPipeMode = PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT
    hPipe = CreateNamedPipeW(r'\\.\pipe\%s' % lpName, dwOpenMode, dwPipeMode, nMaxInstances, nOutBufferSize, nInBufferSize, nDefaultTimeOut, None)

    if hPipe == INVALID_HANDLE_VALUE:
        print("[CreatePipeW] Failed to Create Pipe")
        return False,None

    return True,hPipe


def connect_named_pipe(hPipe):
    return ConnectNamedPipe(hPipe,None)


# -- Helpers
def write_pipe(hPipe,data):
    return write_file(hPipe,data)

def read_pipe(hPipe,amount):
    res,data = read_file(hPipe,amount)
    if res:
        return data
    return b""

def close_pipe(hPipe):
    return close_handle(hPipe)

def write_pipe_string(hPipe,data,encoding='utf-8'):
    return write_pipe(hPipe,data.encode(encoding))

def read_pipe_string(hPipe,buffer_max, encoding='utf-8'):
    res,data = read_file(hPipe,buffer_max)
    if not res:
        return ""
    return bytes(data[:]).decode(encoding)    

def set_dll_directory(dll_path):
    return SetDllDirectoryW(dll_path)

def create_symlink(src_path,dest_path,is_directory=False):
    flags = 0
    if is_directory:
        flags = 1
    return CreateSymbolicLinkW(src_path,dest_path,flags)