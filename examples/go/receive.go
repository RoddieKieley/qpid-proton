/*
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
*/

package main

import (
	"./util"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"qpid.apache.org/proton/amqp"
	"qpid.apache.org/proton/concurrent"
	"sync"
)

// Usage and command-line flags
func usage() {
	fmt.Fprintf(os.Stderr, `Usage: %s url [url ...]
Receive messages from all the listed URLs concurrently and print them.
`, os.Args[0])
	flag.PrintDefaults()
}

var count = flag.Uint64("count", 1, "Stop after receiving this many messages.")

func main() {
	flag.Usage = usage
	flag.Parse()

	urls := flag.Args() // Non-flag arguments are URLs to receive from
	if len(urls) == 0 {
		log.Println("No URL provided")
		usage()
		os.Exit(1)
	}

	messages := make(chan amqp.Message) // Channel for messages from goroutines to main()
	stop := make(chan struct{})         // Closing this channel means the program is stopping.
	var wait sync.WaitGroup             // Used by main() to wait for all goroutines to end.
	wait.Add(len(urls))                 // Wait for one goroutine per URL.

	container := concurrent.NewContainer("")
	connections := make(chan concurrent.Connection, len(urls)) // Connections to close on exit

	// Start a goroutine to for each URL to receive messages and send them to the messages channel.
	// main() receives and prints them.
	for _, urlStr := range urls {
		util.Debugf("Connecting to %s\n", urlStr)
		go func(urlStr string) { // Start the goroutine

			defer wait.Done()                 // Notify main() when this goroutine is done.
			url, err := amqp.ParseURL(urlStr) // Like net/url.Parse() but with AMQP defaults.
			util.ExitIf(err)

			// Open a new connection
			conn, err := net.Dial("tcp", url.Host) // Note net.URL.Host is actually "host:port"
			util.ExitIf(err)
			c, err := container.Connection(conn)
			util.ExitIf(err)
			util.ExitIf(c.Open())
			connections <- c // Save connection so we can Close() when main() ends

			// Create a Receiver using the path of the URL as the source address
			r, err := c.Receiver(url.Path)
			util.ExitIf(err)

			// Loop receiving messages and sending them to the main() goroutine
			for {
				rm, err := r.Receive()
				if err == concurrent.Closed {
					return
				}
				util.ExitIf(err)
				select { // Send m to main() or stop
				case messages <- rm.Message: // Send to main()
				case <-stop: // The program is stopping.
					return
				}
			}
		}(urlStr)
	}

	// All goroutines are started, we are receiving messages.
	fmt.Printf("Listening on %d connections\n", len(urls))

	// print each message until the count is exceeded.
	for i := uint64(0); i < *count; i++ {
		m := <-messages
		util.Debugf("%s\n", util.FormatMessage(m))
	}
	fmt.Printf("Received %d messages\n", *count)

	// Close all connections, this will interrupt goroutines blocked in Receiver.Receive()
	for i := 0; i < len(urls); i++ {
		c := <-connections
		c.Disconnect(nil) // FIXME aconway 2015-09-25: Close
	}
	close(stop) // Signal all goroutines to stop.
	wait.Wait() // Wait for all goroutines to finish.
	close(messages)
}