# Ruby sample for comment ratio
# Full comment line 1

require 'json' # Inline comment

# Full comment line 2

def calculate(x)
  # Full comment line 3
  x * 2 # Inline comment
end

=begin
This is a multi-line comment block
but the current analyzer might not handle it correctly.
=end

puts calculate(5) # Another inline

