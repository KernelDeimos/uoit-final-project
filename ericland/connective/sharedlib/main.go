package main

import (
	"C"
	"sync"

	"github.com/sirupsen/logrus"
)

const (
	ModeNormal = 0
	ModeDebug  = 1
)

type DebugInfo struct {
	Message string
}

//export elconn_init
func elconn_init(mode int32) LibSharedID {
	if mode == ModeDebug {
		logrus.SetLevel(logrus.DebugLevel)
	}

	globalLock = &sync.Mutex{}
	sharedItems = map[LibSharedID]LibSharedItem{}

	return logDebug("elconn_init() called in debug mode")
}

func main() {}
