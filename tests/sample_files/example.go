// ==============================================================================
// Complex Go Example
// This file demonstrates various Go language features, syntax, and constructs
// for testing lexers, parsers, and code analyzers.
// ==============================================================================

package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
)

// MathUtils provides mathematical utility functions.
type MathUtils struct{}

// Constants for mathematical operations.
const (
	PI = 3.14159265358979323846
	E  = 2.71828182845904523536
)

// ToRadians converts degrees to radians.
func (m MathUtils) ToRadians(degrees float64) float64 {
	return degrees * PI / 180
}

// ToDegrees converts radians to degrees.
func (m MathUtils) ToDegrees(radians float64) float64 {
	return radians * 180 / PI
}

// ComplexNumber represents a complex number with real and imaginary parts.
type ComplexNumber struct {
	real      float64
	imaginary float64
}

// NewComplexNumber creates a new ComplexNumber.
func NewComplexNumber(real, imaginary float64) ComplexNumber {
	return ComplexNumber{real: real, imaginary: imaginary}
}

// Add performs addition of two complex numbers.
func (c ComplexNumber) Add(other ComplexNumber) ComplexNumber {
	return NewComplexNumber(c.real+other.real, c.imaginary+other.imaginary)
}

// Multiply performs multiplication of two complex numbers.
func (c ComplexNumber) Multiply(other ComplexNumber) ComplexNumber {
	newReal := c.real*other.real - c.imaginary*other.imaginary
	newImaginary := c.real*other.imaginary + c.imaginary*other.real
	return NewComplexNumber(newReal, newImaginary)
}

// Modulus calculates the modulus (absolute value) of the complex number.
func (c ComplexNumber) Modulus() float64 {
	return math.Sqrt(c.real*c.real + c.imaginary*c.imaginary)
}

// String returns the string representation of the complex number.
func (c ComplexNumber) String() string {
	return fmt.Sprintf("%.2f%+.2fi", c.real, c.imaginary)
}

// Shape is the base interface for geometric shapes.
type Shape interface {
	Area() float64
	Perimeter() float64
}

// Triangle represents a triangle with three sides.
type Triangle struct {
	a, b, c float64
}

// NewTriangle creates a new Triangle.
func NewTriangle(a, b, c float64) (Triangle, error) {
	if !isValidTriangle(a, b, c) {
		return Triangle{}, fmt.Errorf("invalid triangle sides: %f, %f, %f", a, b, c)
	}
	return Triangle{a: a, b: b, c: c}, nil
}

// isValidTriangle checks if the sides form a valid triangle.
func isValidTriangle(a, b, c float64) bool {
	return (a+b > c) && (a+c > b) && (b+c > a)
}

// Area calculates the area of the triangle using Heron's formula.
func (t Triangle) Area() float64 {
	s := t.Perimeter() / 2.0
	return math.Sqrt(s * (s - t.a) * (s - t.b) * (s - t.c))
}

// Perimeter calculates the perimeter of the triangle.
func (t Triangle) Perimeter() float64 {
	return t.a + t.b + t.c
}

// PolynomialGenerator generates random polynomials.
type PolynomialGenerator struct{}

// Random generates a random polynomial of a given degree.
func (pg PolynomialGenerator) Random(degree int, minCoef, maxCoef float64) func(float64) float64 {
	coefficients := make([]float64, degree+1)
	for i := range coefficients {
		coefficients[i] = minCoef + rand.Float64()*(maxCoef-minCoef)
	}
	coefficients[degree] = 1 + rand.Float64()*(maxCoef-1) // Ensure leading coefficient is non-zero

	return func(x float64) float64 {
		result := 0.0
		for power, coef := range coefficients {
			result += coef * math.Pow(x, float64(power))
		}
		return result
	}
}

// MetaProgrammingExample demonstrates dynamic method creation and method missing.
type MetaProgrammingExample struct{}

// Factorial calculates the factorial of a number.
func (m MetaProgrammingExample) Factorial(n int) int {
	if n <= 1 {
		return 1
	}
	return n * m.Factorial(n-1)
}

// Fibonacci calculates the nth Fibonacci number.
func (m MetaProgrammingExample) Fibonacci(n int) int {
	a, b := 0, 1
	for i := 0; i < n; i++ {
		a, b = b, a+b
	}
	return a
}

// Main program execution.
func main() {
	rand.Seed(time.Now().UnixNano())

	// Create and use a complex number
	z1 := NewComplexNumber(3, 4)
	z2 := NewComplexNumber(1, -2)
	fmt.Printf("z1 = %s, |z1| = %.2f\n", z1, z1.Modulus())
	fmt.Printf("z1 + z2 = %s\n", z1.Add(z2))
	fmt.Printf("z1 * z2 = %s\n", z1.Multiply(z2))

	// Create and use a triangle
	t, err := NewTriangle(3, 4, 5)
	if err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Printf("Triangle area: %.2f, perimeter: %.2f\n", t.Area(), t.Perimeter())
	}

	// Generate a random polynomial and evaluate it
	pg := PolynomialGenerator{}
	poly := pg.Random(3, -10, 10)
	for x := -5; x <= 5; x++ {
		fmt.Printf("p(%d) = %.2f\n", x, poly(float64(x)))
	}

	// Use the MetaProgrammingExample
	math := MetaProgrammingExample{}
	fmt.Printf("5! = %d\n", math.Factorial(5))
	fmt.Printf("10th Fibonacci number = %d\n", math.Fibonacci(10))

	// Demonstrating different data structures
	myArray := []interface{}{1, 2, 3, "mixed", true, []int{4, 5, 6}}
	myMap := map[string]interface{}{
		"name":    "Go",
		"year":    2009,
		"creator": "Robert Griesemer, Rob Pike, Ken Thompson",
		"is_oop":  true,
		"versions": []float64{1.0, 1.1, 1.2, 1.3, 2.0},
	}
	fmt.Println("Array:", myArray)
	fmt.Println("Map:", myMap)

	// Exception handling
	func() {
		defer func() {
			if r := recover(); r != nil {
				fmt.Println("Recovered from panic:", r)
			}
		}()
		panic("This is a panic!")
	}()
}