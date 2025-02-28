# Function to calculate the sum of squares
def sum_of_squares(n)
    sum = 0
    (1..n).each do |i|
      sum += i * i  # Squaring the number and adding to sum
    end
    sum
  end
  
  # Function to calculate factorial
  def factorial(n)
    result = 1
    (1..n).each do |i|
      result *= i  # Multiplying each number to get factorial
    end
    result
  end
  
  # Random number generator function
  def randomize(n)
    rand(n)  # Generate a random number between 0 and n-1
  end
  
  # Main program
  num = 10
  random_num = randomize(num)
  
  puts "Random Number: #{random_num}"
  puts "Sum of squares up to #{num}: #{sum_of_squares(num)}"
  puts "Factorial of #{num}: #{factorial(num)}"
  
  # Using random number to generate a weird result
  weird_result = sum_of_squares(random_num) + factorial(random_num)
  puts "Weird result using random number: #{weird_result}"
  