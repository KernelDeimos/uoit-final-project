package main

import (
	"C"
	"github.com/KernelDeimos/anything-gos/interp_a"
	"github.com/sirupsen/logrus"
)

//export elconn_make_interpreter
func elconn_make_interpreter() LibSharedID {
	evaluator := interp_a.InterpreterFactoryA{}.MakeExec()

	// Evaluate function must by in an empty interface to take reference
	var op interface{}
	op = interp_a.Operation(evaluator.OpEvaluate)

	// Share evaluate function with library caller
	id := AddSharedItem(LibSharedTypeAPI, &op)
	return id
}

//export elconn_call
func elconn_call(inOpID LibSharedID, inListID LibSharedID) LibSharedID {
	// Obtain caller inputs
	opInterface, okay := GetSharedItem(LibSharedTypeAPI, inOpID)
	if !okay {
		logrus.Error("call operation: invalid value")
		return 0
	}
	listInterface, okay := GetSharedItem(LibSharedTypeList, inListID)
	if !okay {
		logrus.Error("call list: invalid value")
		return 0
	}

	// Dereference caller inputs
	inOp := (*opInterface).(interp_a.Operation)
	inList := (*listInterface).([]interface{})

	// Run the specified operation with the specified input list
	result, err := inOp(inList)
	if err != nil {
		logrus.Error(err)
		return 0
	}

	// Share result list with caller
	var resultInterface interface{}
	resultInterface = result
	id := AddSharedItem(LibSharedTypeList, &resultInterface)
	return id
}
