package main

import (
	"C"
	"encoding/json"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"

	"github.com/KernelDeimos/anything-gos/interp_a"
)

//export elconn_serve_remote
func elconn_serve_remote(addr *C.char, opID LibSharedID) int32 {
	// Obtain caller inputs
	opInterface, okay := GetSharedItem(LibSharedTypeAPI, opID)
	if !okay {
		logrus.Error("call operation: invalid value")
		return 0
	}
	addrStr := C.GoString(addr)

	// Dereference caller inputs
	op := interp_a.Operation(
		(*opInterface).(func([]interface{}) ([]interface{}, error)),
	)

	router := gin.Default()
	router.POST("/call", func(c *gin.Context) {
		listStr := c.PostForm("list")
		list := []interface{}{}

		err := json.Unmarshal([]byte(listStr), &list)
		if err != nil {
			logrus.Error(err)
			c.AbortWithError(http.StatusInternalServerError, err)
		}

		result, err := op(list)
		if err != nil {
			logrus.Error(err)
			c.AbortWithError(http.StatusInternalServerError, err)
		}
		c.JSON(http.StatusOK, result)

	})

	go func() {
		err := router.Run(addrStr)
		if err != nil {
			logrus.Error(err)
		}
	}()

	return 0
}

//export elconn_connect_remote
func elconn_connect_remote(addr *C.char) LibSharedID {
	// Obtain caller inputs
	addrStr := C.GoString(addr) + "/call"

	// Create HTTP client
	client := http.Client{}

	// Define operation to send request
	op := func(args []interface{}) ([]interface{}, error) {
		list, err := json.Marshal(args)
		if err != nil {
			logrus.Error(err)
			return nil, err
		}

		// Create form data
		form := url.Values{}
		form.Add("list", string(list))

		// Create request object (and encode form to do so)
		req, err := http.NewRequest("POST", addrStr, strings.NewReader(
			form.Encode(),
		))
		req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
		if err != nil {
			logrus.Error(err)
			return nil, err
		}

		// Perform request
		resp, err := client.Do(req)
		if err != nil {
			logrus.Error(err)
			return nil, err
		}

		// Read response
		// -- read response as bytes
		defer resp.Body.Close()
		responseBytes, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			logrus.Error(err)
			return nil, err
		}
		// -- parse response bytes as JSON
		responseList := []interface{}{}
		err = json.Unmarshal(responseBytes, &responseList)
		if err != nil {
			logrus.Error(err)
			return nil, err
		}

		return responseList, nil
	}

	var opInterface interface{}
	opInterface = op

	id := AddSharedItem(LibSharedTypeAPI, &opInterface)
	return id
}
