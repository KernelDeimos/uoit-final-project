from ctypes import cdll, c_int, c_ulonglong, c_char_p

import json

# === load library
ll = cdll.LoadLibrary("../sharedlib/elconn.so")

# === set return types
ll.elconn_get_type.restype = c_int
ll.elconn_init.restype = c_ulonglong
ll.elconn_list_from_json.restype = c_ulonglong
ll.elconn_make_interpreter.restype = c_ulonglong
ll.elconn_call.restype = c_ulonglong
ll.elconn_connect_remote.restype = c_ulonglong

# === set argument types
ll.elconn_list_from_json.argtypes = [c_char_p]
ll.elconn_serve_remote.argtypes = [c_char_p, c_ulonglong]


# == Manual Test 1 == Using the interpreter
initMsg = ll.elconn_init(0)
ll.elconn_display_info(initMsg)

testList = json.dumps(["format", "Hello, %s!", "World"])
listID = ll.elconn_list_from_json(testList.encode())
ll.elconn_list_print(listID)

interpID = ll.elconn_make_interpreter()
resultID = ll.elconn_call(interpID, listID)
ll.elconn_list_print(resultID)

# == Manual Test 2 == Connecting to remote interpreter
ll.elconn_serve_remote(b":3003", interpID)
remoteID = ll.elconn_connect_remote(b"http://localhost:3003")
rResultID = ll.elconn_call(remoteID, listID)
ll.elconn_list_print(rResultID)