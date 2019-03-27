package main

import (
	"os"
	"exec"
	"io"
	"ioutil"
	"github.com/sirupsen/logrus"
)

func main() {
	if len(os.Args) < 2 {
		logrus.Fatal("oof")
	}
	args := []string{"load"}
	exeCmd := exec.Command("docker", args)

	var a *io.PipeReader
	var b *io.PipeWriter
	a, b = io.Pipe()

	data, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		logrus.Fatal(startErr)
	}

	exeCmd.Stdin = a
	exeCmd.Stdout = os.Stdout
	exeCmd.Stderr = os.Stderr
	startErr := exeCmd.Start()
	if startErr != nil {
		logrus.Fatal(startErr)
	}

	//

	err := exeCmd.Wait()
	if err != nil {
		logrus.Fatal(startErr)
	}
}


