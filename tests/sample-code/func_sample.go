// Go sample for function counting
package main

import "fmt"

func func1() {}

func func2(a int, b int) int {
	return a + b
}

type MyStruct struct{}

func (s MyStruct) method1() {}

func (s *MyStruct) method2() {}

// func commentedOut() {}

var funcVar = func() {}

func main() {
	fmt.Println("Main func")
	go func() { // Goroutine literal
		fmt.Println("Goroutine")
	}()
}

