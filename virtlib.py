from ctypes import *
from ctypes.wintypes import *
import time
LPOVERLAPPED = LPVOID


class SECURITY_DESCRIPTOR(Structure): pass

OPEN_ATTEMPTS_MAX = 5
PSECURITY_DESCRIPTOR = POINTER(SECURITY_DESCRIPTOR)
LPSECURITY_ATTRIBUTES = LPVOID
ULONGLONG = c_ulonglong
PWSTR = c_wchar_p
MAX_PATH = 260
INVALID_HANDLE_VALUE = -1

virtlib_dll = WinDLL("virtdisk.dll")
k32_dll = WinDLL("kernel32.dll")


class Win32_GUID(Structure):
    _fields_ = [("Data1", DWORD),
                ("Data2", WORD),
                ("Data3", WORD),
                ("Data4", BYTE * 8)]


class Win32_STORAGE_DEVICE_NUMBER(Structure):
    _fields_ = [("DeviceType", DWORD),
                ("DeviceNumber", DWORD),
                ("PartitionNumber", DWORD),
                ]


def get_WIN32_VIRTUAL_STORAGE_TYPE_VENDOR_MICROSOFT():
    guid = Win32_GUID()
    guid.Data1 = 0xec984aec
    guid.Data2 = 0xa0f9
    guid.Data3 = 0x47e9
    ByteArray8 = BYTE * 8
    guid.Data4 = ByteArray8(0x90, 0x1f, 0x71, 0x41, 0x5a, 0x66, 0x34, 0x5b)
    return guid


class _ANON__ANON__OPEN_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1_SUB_STRUCTURE_1(Structure):
    _fields_ = [
        ("RWDepth", ULONG),
    ]


class _ANON__ANON__OPEN_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1_SUB_STRUCTURE_2(Structure):
    _fields_ = [
        ("GetInfoOnly", BOOL),
        ("ReadOnly", BOOL),
        ("ResiliencyGuid", Win32_GUID),
    ]


class _ANON__ANON__OPEN_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1_SUB_STRUCTURE_3(Structure):
    _fields_ = [
        ("GetInfoOnly", BOOL),
        ("ReadOnly", BOOL),
        ("ResiliencyGuid", Win32_GUID),
        ("SnapshotId", Win32_GUID),
    ]


class _ANON__OPEN_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1(Union):
    _anonymous_ = ("Version1", "Version2", "Version3")
    _fields_ = [
        ("Version1", _ANON__ANON__OPEN_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1_SUB_STRUCTURE_1),
        ("Version2", _ANON__ANON__OPEN_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1_SUB_STRUCTURE_2),
        ("Version3", _ANON__ANON__OPEN_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1_SUB_STRUCTURE_3),
    ]


class _ANON__ANON__ATTACH_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1_SUB_STRUCTURE_1(Structure):
    _fields_ = [
        ("Reserved", ULONG),
    ]


class _ANON__ANON__ATTACH_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1_SUB_STRUCTURE_2(Structure):
    _fields_ = [
        ("RestrictedOffset", ULONGLONG),
        ("RestrictedLength", ULONGLONG),
    ]


class _ANON__ATTACH_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1(Union):
    _anonymous_ = ("Version1", "Version2")
    _fields_ = [
        ("Version1", _ANON__ANON__ATTACH_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1_SUB_STRUCTURE_1),
        ("Version2", _ANON__ANON__ATTACH_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1_SUB_STRUCTURE_2),
    ]


class Win32_ATTACH_VIRTUAL_DISK_PARAMETERS(Structure):
    _anonymous_ = ("anon_01",)
    _fields_ = [
        ("Version", ULONG),
        ("anon_01", _ANON__ATTACH_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1),
    ]


class Win32_OPEN_VIRTUAL_DISK_PARAMETERS(Structure):
    _anonymous_ = ("anon_01",)
    _fields_ = [
        ("Version", ULONG),
        ("anon_01", _ANON__OPEN_VIRTUAL_DISK_PARAMETERS_SUB_UNION_1),
    ]


class Win32_VIRTUAL_STORAGE_TYPE(Structure):
    _fields_ = [
        ('DeviceId', DWORD),
        ('VendorId', Win32_GUID)
    ]


# Virtual Disk Access Flags
VIRTUAL_DISK_ACCESS_NONE = 0x00000000
VIRTUAL_DISK_ACCESS_ATTACH_RO = 0x00010000
VIRTUAL_DISK_ACCESS_ATTACH_RW = 0x00020000
VIRTUAL_DISK_ACCESS_DETACH = 0x00040000
VIRTUAL_DISK_ACCESS_GET_INFO = 0x00080000
VIRTUAL_DISK_ACCESS_CREATE = 0x00100000
VIRTUAL_DISK_ACCESS_METAOPS = 0x00200000
VIRTUAL_DISK_ACCESS_READ = 0x000d0000
VIRTUAL_DISK_ACCESS_ALL = 0x003f0000

# Open Virtual Disk Flags
OPEN_VIRTUAL_DISK_FLAG_NONE = 0
OPEN_VIRTUAL_DISK_FLAG_NO_PARENTS = 1
OPEN_VIRTUAL_DISK_FLAG_BLANK_FILE = 2
OPEN_VIRTUAL_DISK_FLAG_BOOT_DRIVE = 3
OPEN_VIRTUAL_DISK_FLAG_CACHED_IO = 4
OPEN_VIRTUAL_DISK_FLAG_CUSTOM_DIFF_CHAIN = 5
OPEN_VIRTUAL_DISK_FLAG_PARENT_CACHED_IO = 6
OPEN_VIRTUAL_DISK_FLAG_VHDSET_FILE_ONLY = 7
OPEN_VIRTUAL_DISK_FLAG_IGNORE_RELATIVE_PARENT_LOCATOR = 8
OPEN_VIRTUAL_DISK_FLAG_NO_WRITE_HARDENING = 9

# Attach Virtual Disk Flags
ATTACH_VIRTUAL_DISK_FLAG_NONE = 0x00000000
ATTACH_VIRTUAL_DISK_FLAG_READ_ONLY = 0x00000001
ATTACH_VIRTUAL_DISK_FLAG_NO_DRIVE_LETTER = 0x00000002
ATTACH_VIRTUAL_DISK_FLAG_PERMANENT_LIFETIME = 0x00000004
ATTACH_VIRTUAL_DISK_FLAG_NO_LOCAL_HOST = 0x00000008
ATTACH_VIRTUAL_DISK_FLAG_NO_SECURITY_DESCRIPTOR = 0x00000010
ATTACH_VIRTUAL_DISK_FLAG_BYPASS_DEFAULT_ENCRYPTION_POLICY = 0x00000020
ATTACH_VIRTUAL_DISK_FLAG_NON_PNP = 0x00000040
ATTACH_VIRTUAL_DISK_FLAG_RESTRICTED_RANGE = 0x00000080
ATTACH_VIRTUAL_DISK_FLAG_SINGLE_PARTITION = 0x00000100
ATTACH_VIRTUAL_DISK_FLAG_REGISTER_VOLUME = 0x00000200

# Detach Virtual Disk Flags
DETACH_VIRTUAL_DISK_FLAG_NONE = 0x00000000

# Open Virtual Disk Versions
OPEN_VIRTUAL_DISK_VERSION_UNSPECIFIED = 0
OPEN_VIRTUAL_DISK_VERSION_1 = 1
OPEN_VIRTUAL_DISK_VERSION_2 = 2
OPEN_VIRTUAL_DISK_VERSION_3 = 3

# Attach Virtual Disk Versions
ATTACH_VIRTUAL_DISK_VERSION_UNSPECIFIED = 0
ATTACH_VIRTUAL_DISK_VERSION_1 = 1
ATTACH_VIRTUAL_DISK_VERSION_2 = 2

# Virtual Storage Types
VIRTUAL_STORAGE_TYPE_DEVICE_UNKNOWN = 0
VIRTUAL_STORAGE_TYPE_DEVICE_ISO = 1
VIRTUAL_STORAGE_TYPE_DEVICE_VHD = 2
VIRTUAL_STORAGE_TYPE_DEVICE_VHDX = 3
VIRTUAL_STORAGE_TYPE_DEVICE_VHDSET = 4

# IOCTL STUFF
FILE_DEVICE_DISK = 0x00000007
FILE_DEVICE_CD_ROM = 0x00000002


# Function Definitions

OpenVirtualDisk = virtlib_dll.OpenVirtualDisk
OpenVirtualDisk.restype = DWORD
OpenVirtualDisk.argtypes = [POINTER(Win32_VIRTUAL_STORAGE_TYPE), LPWSTR, ULONG, ULONG,
                            POINTER(Win32_OPEN_VIRTUAL_DISK_PARAMETERS), POINTER(HANDLE)]

AttachVirtualDisk = virtlib_dll.AttachVirtualDisk
AttachVirtualDisk.restype = DWORD
AttachVirtualDisk.argtypes = [HANDLE, PSECURITY_DESCRIPTOR, ULONG, ULONG, POINTER(Win32_ATTACH_VIRTUAL_DISK_PARAMETERS),
                              LPOVERLAPPED]

DetachVirtualDisk = virtlib_dll.DetachVirtualDisk
DetachVirtualDisk.restype = DWORD
DetachVirtualDisk.argtypes = [HANDLE, ULONG, ULONG]

GetVirtualDiskPhysicalPath = virtlib_dll.GetVirtualDiskPhysicalPath
GetVirtualDiskPhysicalPath.restype = DWORD
GetVirtualDiskPhysicalPath.argtypes = [HANDLE, PULONG, PWSTR]

DeleteVolumeMountPointW = k32_dll.DeleteVolumeMountPointW
DeleteVolumeMountPointW.restype = BOOL
DeleteVolumeMountPointW.argtypes = [LPWSTR]

FindFirstVolumeW = k32_dll.FindFirstVolumeW
FindFirstVolumeW.restype = HANDLE
FindFirstVolumeW.argtypes = [LPWSTR, DWORD]

FindNextVolumeW = k32_dll.FindNextVolumeW
FindNextVolumeW.restype = BOOL
FindNextVolumeW.argtypes = [HANDLE, LPWSTR, DWORD]

FILE_SHARE_READ = 1
FILE_SHARE_WRITE = 2
OPEN_EXISTING = 3

IOCTL_STORAGE_GET_DEVICE_NUMBER = 0x002D1080

CreateFileW = k32_dll.CreateFileW
CreateFileW.restype = HANDLE
CreateFileW.argtypes = [LPCWSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE]

CloseHandle = k32_dll.CloseHandle

DeviceIoControl = k32_dll.DeviceIoControl
DeviceIoControl.restype = BOOL
DeviceIoControl.argtypes = [HANDLE, DWORD, LPVOID, DWORD, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]

SetVolumeMountPointW = k32_dll.SetVolumeMountPointW
SetVolumeMountPointW.restype = BOOL
SetVolumeMountPointW.argtypes = [LPCWSTR, LPCWSTR]

IMAGE_PROFILE_MAP = {
    "VHD": {
        "access_mask":VIRTUAL_DISK_ACCESS_ALL,
        "storage_type_device":VIRTUAL_STORAGE_TYPE_DEVICE_VHD,
    },
    "VHDX":{
        "access_mask": VIRTUAL_DISK_ACCESS_ALL,
        "storage_type_device": VIRTUAL_STORAGE_TYPE_DEVICE_VHDX,
    },
    "ISO":{
        "access_mask":VIRTUAL_DISK_ACCESS_ATTACH_RO | VIRTUAL_DISK_ACCESS_GET_INFO,
        "storage_type_device":VIRTUAL_STORAGE_TYPE_DEVICE_ISO,
    },
    "UDF":{
        "access_mask":VIRTUAL_DISK_ACCESS_ATTACH_RO | VIRTUAL_DISK_ACCESS_GET_INFO,
        "storage_type_device":VIRTUAL_STORAGE_TYPE_DEVICE_ISO,
    }  
}


def open_virtual_disk(disk_path, image_type=None):
    storage_type_device=VIRTUAL_STORAGE_TYPE_DEVICE_VHDX
    access_mask=VIRTUAL_DISK_ACCESS_ALL
    if image_type is not None:
        access_mask = IMAGE_PROFILE_MAP[image_type]["access_mask"]
        storage_type_device = IMAGE_PROFILE_MAP[image_type]["storage_type_device"]
    storage_type = Win32_VIRTUAL_STORAGE_TYPE()
    storage_type.DeviceId = storage_type_device
    storage_type.VendorId = get_WIN32_VIRTUAL_STORAGE_TYPE_VENDOR_MICROSOFT()

    open_parameters = Win32_OPEN_VIRTUAL_DISK_PARAMETERS()
    open_parameters.Version = OPEN_VIRTUAL_DISK_VERSION_1

    h_vd = HANDLE()
    open_attempt_counter = 0
    while open_attempt_counter != OPEN_ATTEMPTS_MAX:
        result = OpenVirtualDisk(byref(storage_type), disk_path, access_mask, OPEN_VIRTUAL_DISK_FLAG_NONE, byref(open_parameters), byref(h_vd))
        open_attempt_counter += 1
        # If we're waiting for close, give it a sec.
        if result == 32:
            time.sleep(1)
            continue
        elif (result):
            print("OpenVirtualDisk Error: %d %d" % (result,GetLastError()))
            return False, h_vd
        else:
            break
    if (result):
        print("OpenVirtualDisk Error: %d %d" % (result,GetLastError()))
        return False, h_vd
    return True, h_vd


def close_virtual_disk(h_disk):
    CloseHandle(h_disk)


def mount_virtual_disk(h_disk, mount_path,mount_type="DISK", read_only=True):
    # Set Flags and Attach the Disk
    attach_flags = ATTACH_VIRTUAL_DISK_FLAG_NO_DRIVE_LETTER | ATTACH_VIRTUAL_DISK_FLAG_PERMANENT_LIFETIME


    if read_only is True:
        attach_flags |= ATTACH_VIRTUAL_DISK_FLAG_READ_ONLY

    attach_parameters = Win32_ATTACH_VIRTUAL_DISK_PARAMETERS()
    attach_parameters.Version = ATTACH_VIRTUAL_DISK_VERSION_1

    result = AttachVirtualDisk(h_disk, None, attach_flags, 0, byref(attach_parameters), 0)
    if (result):
        print("AttachVirtualDisk Error: %d %d" % (GetLastError(), result))
        return False

        # Get the Physical Path of the Disk
    physical_drive = create_unicode_buffer(MAX_PATH)
    buffer_size = ULONG(MAX_PATH)
    result = GetVirtualDiskPhysicalPath(h_disk, byref(buffer_size), physical_drive)
    if (result):
        print("GetVirtualDiskPhysicalPath Error: %d %d" % (GetLastError(), result))
        return False
    physical_path = physical_drive[:].rstrip("\x00")
    device_type = None
    if (mount_type == "DISK"):
        drive_index = int(physical_path.replace("\\\\.\\PhysicalDrive", ""))
        device_type = FILE_DEVICE_DISK
    elif (mount_type == "CDROM"):
        drive_index = int(physical_path.replace("\\\\.\\CDROM", ""))
        device_type = FILE_DEVICE_CD_ROM
        # Find The Volume Name
    volume_path = create_unicode_buffer(MAX_PATH)
    buffer_size = ULONG(MAX_PATH)
    h_volume = FindFirstVolumeW(volume_path, buffer_size)
    if (not h_volume):
        print("FindFirstVolumeW Failed: %d" % GetLastError())

    vpath = volume_path[:].rstrip('\x00')

    if (vpath.endswith("\\")):
        vpath = vpath[:-1]
    target_volume_found = False
    while not target_volume_found:
        c_vol = CreateFileW(vpath, 0, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None)
        if (c_vol > 0):
            sdn = Win32_STORAGE_DEVICE_NUMBER()
            bytes_returned = DWORD(0)
            res = DeviceIoControl(c_vol, IOCTL_STORAGE_GET_DEVICE_NUMBER, None, 0, byref(sdn), 12,
                                  byref(bytes_returned), None)
            CloseHandle(c_vol)
            if (res):
                if (sdn.DeviceType == device_type and sdn.DeviceNumber == drive_index):
                    target_volume_found = True
                    break

        if (not FindNextVolumeW(h_volume, volume_path, buffer_size)):
            break
        vpath = volume_path[:].rstrip('\x00')
        if (vpath.endswith("\\")):
            vpath = vpath[:-1]


    if (not target_volume_found):
        print("Error - Target Volume Not Found")
        return False

    if (not vpath.endswith("\\")):
        vpath += "\\"
    if (not mount_path.endswith("\\")):
        mount_path += "\\"
    if (not SetVolumeMountPointW(mount_path, vpath)):
        print("Error: SetVolumeMountPointW Failed: %d" % GetLastError())
        return False


    return True


def unmount_virtual_disk(h_disk, mount_path):
    if (not mount_path.endswith("\\")):
        mount_path += "\\"
    res = DeleteVolumeMountPointW(mount_path)

    if not res:
        return False

    res = DetachVirtualDisk(h_disk, DETACH_VIRTUAL_DISK_FLAG_NONE, 0)
    if res:
        print("DetachVirtualDisk Failed: %d" % GetLastError())
        return False

    return True


if __name__ == "__main__":

    image_path = "C:\\VX\\APP\\DigDug Deeper.vxapp\\content\\Dig Dug Deeper (USA).iso"
    mount_point = "C:\\VX\\TESTMNT"

    status, h_disk = open_virtual_disk(image_path,image_type="ISO")
    if (status is True):
        print("Open OK!")
        

    status = mount_virtual_disk(h_disk, mount_point,mount_type="CDROM")
    if (status is True):
        print("Mount OK!")
        
    wat = input("Check to See if It's Good... \n")
    status = unmount_virtual_disk(h_disk, mount_point)
    if (status is True):
        print("Unmount OK!")

    close_virtual_disk(h_disk)