from ctypes import cdll, c_int, c_ulonglong, c_char_p

import json

# === load library
ll = cdll.LoadLibrary("../sharedlib/elconn.so")

# === set return types
ll.elconn_get_type.restype = c_int
ll.elconn_init.restype = c_ulonglong
ll.elconn_list_from_json.restype = c_ulonglong

# === set argument types
ll.elconn_list_from_json.argtypes = [c_char_p]

initMsg = ll.elconn_init(1)
ll.elconn_display_info(initMsg)

testList = json.dumps(["format", "Hello, %s!", "World"])
listID = ll.elconn_list_from_json(testList.encode())
ll.elconn_list_print(listID)
