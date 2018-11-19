package main

import (
	"errors"
	"github.com/KernelDeimos/anything-gos/interp_a"
)

/*
	This file contains data strictures which can by used via the interpreter.
*/

func makeDataStructureFactory() interp_a.Operation {
	makeFunctions := interp_a.InterpreterFactoryA{}.MakeEmpty()

	// A "directory" is internally referred to as a map. It is just an empty
	// interpreter instance on which other data structures can be applied with
	// a name. For example, "sensors" will be a directory containing request
	// queues.
	makeFunctions.AddOperation("directory", makeDSMap)

	// Making the type "requests" will create an interpreter instance with
	// the following functions:
	// - flush   -> report a list of requests and clear queue
	// - block   -> report the oldest request with blocking wait
	// - check   -> report the oldest request or nil
	// - enque   -> add some data to the request queue (blocking if full queue)
	makeFunctions.AddOperation("requests", makeDSQueue)

	return interp_a.Operation(makeFunctions.OpEvaluate)
}

func makeDSMap(args []interface{}) ([]interface{}, error) {
	empty := interp_a.InterpreterFactoryA{}.MakeEmpty()
	return []interface{}{interp_a.Operation(empty.OpEvaluate)}, nil
}

func makeDSQueue(args []interface{}) ([]interface{}, error) {
	size := 100
	if len(args) > 0 {
		var ok bool
		size, ok = args[0].(int)
		if !ok {
			return nil, errors.New("request queue size must be integer")
		}
	}

	// Create empty interpreter for request queue functions
	empty := interp_a.InterpreterFactoryA{}.MakeEmpty()

	// Make request queue
	ch := make(chan interface{}, size)
	queue := RequestQueue{
		Chan: ch,
	}

	// Bind request queue functions to interpreter
	queue.Bind(empty)

	return []interface{}{interp_a.Operation(empty.OpEvaluate)}, nil
}

type RequestQueue struct {
	Chan chan interface{}
}

func (rq RequestQueue) Bind(destination interp_a.HybridEvaluator) {
	destination.AddOperation("enque", rq.OpEnqueue)
	destination.AddOperation("block", rq.OpDequeueBlk)
}

func (rq RequestQueue) OpEnqueue(args []interface{}) ([]interface{}, error) {
	for _, arg := range args {
		rq.Chan <- arg
	}
	return nil, nil
}

func (rq RequestQueue) OpDequeueBlk(args []interface{}) ([]interface{}, error) {
	value := <-rq.Chan
	return []interface{}{value}, nil
}
