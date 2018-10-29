from ctypes import cdll, c_int, c_ulonglong

# === load library
ll = cdll.LoadLibrary("../sharedlib/elconn.so")

# === set return types
ll.elconn_get_type.restype = c_int
ll.elconn_init.restype = c_ulonglong

initMsg = ll.elconn_init(1)
ll.elconn_display_info(initMsg)
