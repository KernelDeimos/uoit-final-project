package main

import (
	"C"

	"encoding/json"
	"github.com/sirupsen/logrus"
)

//export elconn_list_from_json
func elconn_list_from_json(jsonInputC *C.char) LibSharedID {
	jsonInput := C.GoString(jsonInputC)

	outList := []interface{}{}
	err := json.Unmarshal([]byte(jsonInput), &outList)
	if err != nil {
		logrus.Error(err)
		return 0
	}

	var outListInterface interface{}
	outListInterface = outList

	id := AddSharedItem(LibSharedTypeList, &outListInterface)
	return id
}

//export elconn_list_print
func elconn_list_print(listID LibSharedID) int32 {
	listInterface, okay := GetSharedItem(LibSharedTypeList, listID)
	if !okay {
		logrus.Error("could not print list: invalid value")
		return -1
	}

	result, err := json.Marshal(*listInterface)
	if err != nil {
		logrus.Error(err)
		return -1
	}

	logrus.Info(string(result))
	return 0
}
