package main

import (
	"flag"
	"fmt"
	"github.com/chzyer/readline"
	"io"
	"os"

	"github.com/sirupsen/logrus"
)

var logo = `
[31;1m______ _                      _      
| ___ \ |                    (_)     
| |_/ / |__   ___   ___ _ __  ___  __
|  __/| '_ \ / _ \ / _ \ '_ \| \ \/ /
| |   | | | | (_) |  __/ | | | |>  < 
\_|   |_| |_|\___/ \___|_| |_|_/_/\_\
[33;1m                        Phoenix Shell
[0m`

var help = `
Usage:
	phsh [-file=FILE]
`

func main() {

	argPtrFile := flag.String("file", "", "A script file")
	argPtrDebug := flag.Bool("debug", false, "Enable debug mode")

	fmt.Fprintln(os.Stderr, logo)

	flag.Parse()

	if *argPtrDebug {
		logrus.Warn("Debug mode is on")
	}

	if *argPtrFile != "" {
		logrus.Fatal("Script execution not supported yet")
	}

	l, err := readline.NewEx(&readline.Config{
		Prompt:          "ERROR SETTING PROMPT",
		HistoryFile:     "/tmp/phsh_history_file.tmp",
		InterruptPrompt: "^SIGINT",
	})
	defer l.Close()
	if err != nil {
		logrus.Error(err)
		os.Exit(1)
	}

	statEndl := "-\033[0m-\n"

	for {
		statExit := "\033[32;1mOK\033[0m"
		statLoc := "/"
		fmt.Println(statEndl)
		l.SetPrompt(
			statExit + ":" + statLoc + "$ ",
		)
		input, err := l.Readline()
		if err == nil {
			// No action
		} else if err == readline.ErrInterrupt {
			break
		} else if err == io.EOF {
			break
		} else {
			logrus.Error(err)
		}
		input = fmt.Sprintf("%s", input)
		fmt.Println("user input: ", input)
	}

}
