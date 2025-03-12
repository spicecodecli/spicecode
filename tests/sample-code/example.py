# ==============================================================================
# Complex Python Example
# This file demonstrates various Python language features, syntax, and constructs
# for testing lexers, parsers, and code analyzers.
# ==============================================================================

import math
import numpy as np

# Constants
PI = math.pi
E = math.e
C = 299792458  # Speed of light (m/s)
G = 6.67430e-11 # Gravitational constant (m^3 kg^-1 s^-2)

# Trigonometric Functions
def trig_demo(x):
    print("sin:", math.sin(x))
    print("cos:", math.cos(x))
    print("tan:", math.tan(x))

# Matrix Operations
def matrix_demo():
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    print("Matrix A:", A)
    print("Matrix B:", B)
    print("A + B:", A + B)
    print("A - B:", A - B)
    print("A * B:", A @ B)
    print("Transpose of A:", A.T)

# Factorial
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Fibonacci
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    seq = [0, 1]
    for _ in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq

# Prime Number Checker
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Sum of Primes
def sum_of_primes(limit):
    return sum(n for n in range(2, limit) if is_prime(n))

# Euclidean Distance
def euclidean_distance(p1, p2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(p1, p2)))

# Matrix Determinant
def matrix_determinant(matrix):
    return np.linalg.det(matrix)

# Large Matrix and Inversion
def large_matrix_demo(size):
    matrix = np.random.rand(size, size)
    inv_matrix = np.linalg.inv(matrix)

# Quadratic Solver
def solve_quadratic(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    root1 = (-b + math.sqrt(discriminant)) / (2 * a)
    root2 = (-b - math.sqrt(discriminant)) / (2 * a)
    return root1, root2

# Einstein's Mass-Energy Equivalence
def mass_energy(mass):
    return mass * C**2

# Newton's Law of Gravitation
def gravitational_force(m1, m2, r):
    return G * m1 * m2 / r**2

# Fourier Transform Example
def fourier_transform_demo():
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2 * PI * 50 * t) + 0.5 * np.sin(2 * PI * 120 * t)
    freq = np.fft.fftfreq(len(t), d=(t[1] - t[0]))
    fft_values = np.fft.fft(signal)

# Complex Number Operations
def complex_operations():
    z1 = complex(2, 3)
    z2 = complex(1, -1)
    print("z1 + z2:", z1 + z2)
    print("z1 * z2:", z1 * z2)
    print("conjugate of z1:", z1.conjugate())

# Mandelbrot Set Example
def mandelbrot_set_demo(size):
    x = np.linspace(-2, 1, size)
    y = np.linspace(-1.5, 1.5, size)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    c = Z
    for _ in range(20):
        Z = Z**2 + c
    mandelbrot = np.abs(Z) < 2

# Taylor Series for e^x
def taylor_exp(x, terms=10):
    result = sum((x**n) / factorial(n) for n in range(terms))
    return result

# Matrix Eigenvalues and Eigenvectors
def eigen_demo():
    A = np.random.rand(3, 3)
    eigvals, eigvecs = np.linalg.eig(A)

# Main
if __name__ == "__main__":
    trig_demo(PI / 4)
    matrix_demo()
    print("Factorial of 5:", factorial(5))
    print("Fibonacci (10 terms):", fibonacci(10))
    print("Is 29 prime?", is_prime(29))
    print("Sum of primes up to 100:", sum_of_primes(100))
    print("Euclidean distance:", euclidean_distance((1, 2), (4, 6)))
    matrix = [[2, 3], [1, 4]]
    print("Determinant:", matrix_determinant(matrix))
    large_matrix_demo(3)
    print("Quadratic roots:", solve_quadratic(1, -3, 2))
    print("E=mc^2 for m=1kg:", mass_energy(1))
    print("Gravitational force (Earth-Sun):", gravitational_force(5.972e24, 1.989e30, 1.496e11))
    fourier_transform_demo()
    complex_operations()
    mandelbrot_set_demo(500)
    print("Taylor series of e^1:", taylor_exp(1))
    eigen_demo()

# Heavy computations to fill lines
for i in range(50):
    print(f"Factorial of {i} = {factorial(i)}")

for i in range(30):
    print(f"Fibonacci {i} terms: {fibonacci(i)}")

for i in range(100, 150):
    print(f"Is {i} prime? {is_prime(i)}")