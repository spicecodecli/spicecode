# Ruby sample for function counting
def func1
end

class MyClass
  def method1
  end

  def self.class_method
  end
end

def func2(a, b)
  a + b
end

# def commented_out
# end

lambda_func = lambda { |x| x * 2 }

proc_func = Proc.new { |y| y + 1 }

def func_with_block(&block)
  yield if block_given?
end

MyClass.new.method1

