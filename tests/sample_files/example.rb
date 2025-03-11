# ==============================================================================
# Complex Ruby Example
# This file demonstrates various Ruby language features, syntax, and constructs
# for testing lexers, parsers, and code analyzers.
# ==============================================================================

# Module for mathematical operations
module MathUtils
  PI = 3.14159265358979323846
  E = 2.71828182845904523536
  
  # Convert degrees to radians
  def self.to_radians(degrees)
    degrees * PI / 180
  end
  
  # Convert radians to degrees
  def self.to_degrees(radians)
    radians * 180 / PI
  end
end

# Class for representing and manipulating complex numbers
class ComplexNumber
  attr_reader :real, :imaginary
  
  def initialize(real, imaginary)
    @real = real
    @imaginary = imaginary
  end
  
  # Operator overloading for addition
  def +(other)
    ComplexNumber.new(@real + other.real, @imaginary + other.imaginary)
  end
  
  # Operator overloading for multiplication
  def *(other)
    new_real = @real * other.real - @imaginary * other.imaginary
    new_imaginary = @real * other.imaginary + @imaginary * other.real
    ComplexNumber.new(new_real, new_imaginary)
  end
  
  def to_s
    "#{@real}#{@imaginary >= 0 ? '+' : ''}#{@imaginary}i"
  end
  
  # Calculate the modulus (absolute value) of the complex number
  def modulus
    Math.sqrt(@real**2 + @imaginary**2)
  end
end

# Base class for geometric shapes
class Shape
  def area
    raise NotImplementedError, "Subclasses must implement area method"
  end
  
  def perimeter
    raise NotImplementedError, "Subclasses must implement perimeter method"
  end
end

# Triangle class that inherits from Shape
class Triangle < Shape
  def initialize(a, b, c)
    @sides = [a, b, c]
    raise ArgumentError, "Invalid triangle sides" unless valid_triangle?
  end
  
  def valid_triangle?
    a, b, c = @sides
    (a + b > c) && (a + c > b) && (b + c > a)
  end
  
  def area
    # Heron's formula
    s = perimeter / 2.0
    Math.sqrt(s * (s - @sides[0]) * (s - @sides[1]) * (s - @sides[2]))
  end
  
  def perimeter
    @sides.sum
  end
end

# Duck typing example with a random polynomial generator
class PolynomialGenerator
  def self.random(degree, min_coef = -10, max_coef = 10)
    coefficients = Array.new(degree + 1) { rand(min_coef..max_coef) }
    coefficients[degree] = rand(1..max_coef) # Ensure leading coefficient is non-zero
    
    lambda do |x|
      result = 0
      coefficients.each_with_index do |coef, power|
        result += coef * (x ** power)
      end
      result
    end
  end
end

# Example of metaprogramming
class MetaProgrammingExample
  # Define methods dynamically
  %w[sin cos tan].each do |trig_function|
    define_method(trig_function) do |angle|
      Math.send(trig_function, MathUtils.to_radians(angle))
    end
  end
  
  # Method missing implementation
  def method_missing(method_name, *args)
    if method_name.to_s =~ /^compute_(.+)$/
      operation = $1
      case operation
      when "factorial"
        factorial(args[0])
      when "fibonacci"
        fibonacci(args[0])
      else
        super
      end
    else
      super
    end
  end
  
  private
  
  def factorial(n)
    # Recursive factorial implementation
    return 1 if n <= 1
    n * factorial(n - 1)
  end
  
  def fibonacci(n)
    # Iterative fibonacci implementation
    a, b = 0, 1
    n.times { a, b = b, a + b }
    a
  end
end

# Anonymous function (lambda) examples
square = ->(x) { x * x }
cube = ->(x) { x ** 3 }

# Demonstrate different variable types
local_var = "I'm a local variable"
$global_var = "I'm a global variable"
@instance_var = "I'm an instance variable"
@@class_var = "I'm a class variable"
CONSTANT = "I'm a constant"

=begin
This is a multi-line comment
It can span multiple lines
And is useful for documentation
=end

# Demonstrating different data structures
my_array = [1, 2, 3, "mixed", :types, [4, 5, 6]]
my_hash = {
  name: "Ruby",
  year: 1995,
  creator: "Yukihiro Matsumoto",
  is_oop: true,
  versions: [1.8, 1.9, 2.0, 2.5, 3.0]
}

# Exception handling
begin
  result = 10 / 0
rescue ZeroDivisionError => e
  puts "Caught error: #{e.message}"
rescue => e
  puts "Caught other error: #{e.message}"
ensure
  puts "This code always runs"
end

# Main program execution
if __FILE__ == $PROGRAM_NAME
  # Create and use a complex number
  z1 = ComplexNumber.new(3, 4)
  z2 = ComplexNumber.new(1, -2)
  puts "z1 = #{z1}, |z1| = #{z1.modulus}"
  puts "z1 + z2 = #{z1 + z2}"
  puts "z1 * z2 = #{z1 * z2}"
  
  # Create and use a triangle
  begin
    t = Triangle.new(3, 4, 5)
    puts "Triangle area: #{t.area}, perimeter: #{t.perimeter}"
  rescue ArgumentError => e
    puts "Error: #{e.message}"
  end
  
  # Generate a random polynomial and evaluate it
  poly = PolynomialGenerator.random(3)
  (-5..5).each do |x|
    puts "p(#{x}) = #{poly.call(x)}"
  end
  
  # Use the metaprogramming example
  math = MetaProgrammingExample.new
  puts "sin(30°) = #{math.sin(30)}"
  puts "cos(60°) = #{math.cos(60)}"
  puts "tan(45°) = #{math.tan(45)}"
  puts "5! = #{math.compute_factorial(5)}"
  puts "10th Fibonacci number = #{math.compute_fibonacci(10)}"
  
  # Using Enumerables with blocks
  numbers = (1..10).to_a
  sum = numbers.reduce(0) { |acc, n| acc + n }
  squares = numbers.map { |n| square.call(n) }
  evens = numbers.select { |n| n.even? }
  odds = numbers.reject { |n| n.even? }
  
  puts "Sum: #{sum}"
  puts "Squares: #{squares}"
  puts "Evens: #{evens}"
  puts "Odds: #{odds}"
end