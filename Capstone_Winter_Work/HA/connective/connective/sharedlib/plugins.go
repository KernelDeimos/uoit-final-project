package main

import (
	"encoding/json"
	"errors"
	"github.com/satori/go.uuid"
	"github.com/sirupsen/logrus"
	"sync"
	"time"

	"github.com/KernelDeimos/anything-gos/interp_a"
)

func makePluginFactory() interp_a.Operation {
	makeFunctions := interp_a.InterpreterFactoryA{}.MakeEmpty()

	// The "device" plugin addes the add-device operation to a parent
	// operation. This makes it possible to add device entries which each have
	// their own thread-safe queue for property updates, as well as including
	// objects for meta information and Mozilla Web-of-Things definition.
	// See sub-commands of device plugin for more documentation.
	makeFunctions.AddOperation("device", makePlugDevice)

	return interp_a.Operation(makeFunctions.OpEvaluate)
}

type DevicePluginUpdateEvent map[string]interface{}

func makePlugDevice(args []interface{}) ([]interface{}, error) {
	//::gen verify-args makePlugDevice op interp_a.Operation
	if len(args) < 1 {
		return nil, errors.New("makePlugDevice requires at least 1 arguments")
	}

	var op interp_a.Operation
	{
		var ok bool
		op, ok = args[0].(interp_a.Operation)
		if !ok {
			return nil, errors.New("makePlugDevice: argument 0: op; must be type interp_a.Operation")
		}
	}
	//::end

	// Create UUID for the device
	deviceUUID := uuid.Must(uuid.NewV4()).String()
	logrus.Debug("Device id will be:", deviceUUID)

	// var result []interface{}
	var err error

	// Add empty dirctory for device node registry
	deviceMap := interp_a.InterpreterFactoryA{}.MakeEmpty()

	//::run : testout (store (DATA))
	{
		r, e := op([]interface{}{"__debug_listmethods"})
		if e != nil {
			logrus.Error(e)
		}
		logrus.Debug(r)
	}
	//::end

	_, err = op([]interface{}{":", "on",
		interp_a.Operation(deviceMap.OpEvaluate)})
	if err != nil {
		return nil, err
	}

	//::gen testout
	{
		r, e := op([]interface{}{"__debug_listmethods"})
		if e != nil {
			logrus.Error(e)
		}
		logrus.Debug(r)
	}
	//::end

	// Invoke "set" (:) operation to add add-device operation to operation
	// Usage: add-device <Mozilla definition> <user-defined meta information>
	_, err = op([]interface{}{":", "add-device", interp_a.Operation(func(
		args []interface{}) ([]interface{}, error) {
		//::gen verify-args add-device mozmeta interface{} usermeta interface{}
		if len(args) < 2 {
			return nil, errors.New("add-device requires at least 2 arguments")
		}

		var mozmeta interface{}
		var usermeta interface{}
		{
			var ok bool
			mozmeta, ok = args[0].(interface{})
			if !ok {
				return nil, errors.New("add-device: argument 0: mozmeta; must be type interface{}")
			}
			usermeta, ok = args[1].(interface{})
			if !ok {
				return nil, errors.New("add-device: argument 1: usermeta; must be type interface{}")
			}
		}
		//::end

		// DECLARE struct for Mozilla web-thing definition
		var mozmetaStruct MozThingDefinition

		// DECLARE internal mutex for queue-properties interaction
		mutexProperties := &sync.RWMutex{}

		// Process Mozilla IoT definition
		{
			mozmetaBytes, err := json.Marshal(mozmeta)
			if err != nil {
				return nil, err
			}

			err = json.Unmarshal(mozmetaBytes, &mozmetaStruct)
			if err != nil {
				return nil, err
			}
		}

		// Create device node object
		deviceNode := interp_a.InterpreterFactoryA{}.MakeEmpty()

		// --- device node operation to get Mozilla definition
		deviceNode.AddOperation("get-moz", func(
			args []interface{}) ([]interface{}, error) {
			return []interface{}{mozmetaStruct}, nil
		})

		// --- device node operation to get user-defined meta
		deviceNode.AddOperation("get-meta", func(
			args []interface{}) ([]interface{}, error) {
			return []interface{}{usermeta}, nil
		})

		// Create a directory for properties
		{
			result, err := makeDSMap([]interface{}{})
			o := result[0].(interp_a.Operation)
			if err != nil {
				return nil, err
			}
			deviceNode.AddOperation("properties", o)
			// TODO: optimize properties by creating separate
			//       data-storage backend
		}

		// Create a queue for device updates
		{
			result, err := makeDSQueue([]interface{}{})
			o := result[0].(interp_a.Operation)
			if err != nil {
				return nil, err
			}
			deviceNode.AddOperation("update-queue", o)
		}

		// Start goroutine for queue-properties interaction
		go func() {
			// Custom error handler for this goroutine
			handleErrorInHere := func(err error) {
				// Log error to stderr
				logrus.Error(err)
				// Wait 20 seconds to prevent heavy log output
				<-time.After(20 * time.Second)
			}
			for {
				// Perform blocking wait for update queue event
				result, err := deviceNode.OpEvaluate(
					[]interface{}{"update-queue", "block"})
				if err != nil {
					handleErrorInHere(err)
				}

				if len(result) < 1 {
					logrus.Warnf("device '%s' received an empty event",
						deviceUUID,
					)
					continue
				}

				// Use intermediate JSON representation to normalize and
				// validate input event
				var event DevicePluginUpdateEvent
				{
					resultBytes, err := json.Marshal(result[0])
					if err != nil {
						handleErrorInHere(err)
						continue
					}

					err = json.Unmarshal(resultBytes, &event)
					if err != nil {
						handleErrorInHere(err)
						continue
					}
				}

				// Perform the update
				mutexProperties.Lock()
				for key, val := range event {
					logrus.Debugf("Updating %s/%s with %v",
						deviceUUID, key, val,
					)
					// Update property using set (:) operation
					result, err := deviceNode.OpEvaluate([]interface{}{
						"properties", ":", key, interp_a.Operation(
							// Use anonymous function to wrap data;
							// this is a temporary solution until the hashmap
							// storage backend is implemented in interp_a
							func(_ []interface{}) ([]interface{}, error) {
								return []interface{}{val}, nil
							},
						)})
					if err != nil {
						logrus.Error(err)
						logrus.Debug(result)
						continue
					}
				}

				mutexProperties.Unlock()

			}
		}()

		deviceMap.AddOperation(deviceUUID, deviceNode.OpEvaluate)

		return nil, nil
	})}) // geez this is starting to look like Javascript
	if err != nil {
		return nil, err
	}

	return nil, nil
}
