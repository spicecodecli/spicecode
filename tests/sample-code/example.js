// ==============================================================================
// Complex Javascript Example
// This file demonstrates various Javascript language features, syntax, and constructs
// for testing lexers, parsers, and code analyzers.
// ==============================================================================

// Constants
const PI = Math.PI;
const E = Math.E;
const C = 299792458; // Speed of light (m/s)
const G = 6.67430e-11; // Gravitational constant (m^3 kg^-1 s^-2)

// Trigonometric Functions
function trigDemo(x) {
    console.log('sin:', Math.sin(x));
    console.log('cos:', Math.cos(x));
    console.log('tan:', Math.tan(x));
}

// Matrix Operations
function matrixDemo() {
    let A = [
        [1, 2],
        [3, 4]
    ];
    let B = [
        [5, 6],
        [7, 8]
    ];
    let C = [
        [A[0][0] + B[0][0], A[0][1] + B[0][1]],
        [A[1][0] + B[1][0], A[1][1] + B[1][1]]
    ];
    console.log('Matrix A:', A);
    console.log('Matrix B:', B);
    console.log('A + B:', C);
}

// Factorial
function factorial(n) {
    if (n === 0) return 1;
    return n * factorial(n - 1);
}

// Fibonacci
function fibonacci(n) {
    if (n <= 0) return [];
    if (n === 1) return [0];
    if (n === 2) return [0, 1];
    let seq = [0, 1];
    for (let i = 2; i < n; i++) {
        seq.push(seq[i - 1] + seq[i - 2]);
    }
    return seq;
}

// Prime Number Checker
function isPrime(n) {
    if (n <= 1) return false;
    for (let i = 2; i <= Math.sqrt(n); i++) {
        if (n % i === 0) return false;
    }
    return true;
}

// Sum of Primes
function sumOfPrimes(limit) {
    let sum = 0;
    for (let n = 2; n < limit; n++) {
        if (isPrime(n)) sum += n;
    }
    return sum;
}

// Quadratic Solver
function solveQuadratic(a, b, c) {
    let discriminant = b * b - 4 * a * c;
    if (discriminant < 0) return null;
    let root1 = (-b + Math.sqrt(discriminant)) / (2 * a);
    let root2 = (-b - Math.sqrt(discriminant)) / (2 * a);
    return [root1, root2];
}

// Einstein's Mass-Energy Equivalence
function massEnergy(mass) {
    return mass * C ** 2;
}

// Newton's Law of Gravitation
function gravitationalForce(m1, m2, r) {
    return G * m1 * m2 / (r ** 2);
}

// DNA Replication Probability (simplified)
function dnaReplicationProbability(successRate, attempts) {
    return 1 - Math.pow(1 - successRate, attempts);
}

// Enzyme Kinetics (Michaelis-Menten Equation)
function enzymeKinetics(Vmax, Km, substrateConcentration) {
    return (Vmax * substrateConcentration) / (Km + substrateConcentration);
}

// Radioactive Decay (Half-life)
function radioactiveDecay(initialAmount, halfLife, time) {
    return initialAmount * Math.pow(0.5, time / halfLife);
}

// Mandelbrot Set Calculation
function mandelbrotSetDemo(size) {
    let maxIterations = 100;
    for (let x = -2; x <= 2; x += 4 / size) {
        for (let y = -2; y <= 2; y += 4 / size) {
            let zx = x, zy = y;
            let iterations = 0;
            while (zx * zx + zy * zy < 4 && iterations < maxIterations) {
                let xtemp = zx * zx - zy * zy + x;
                zy = 2 * zx * zy + y;
                zx = xtemp;
                iterations++;
            }
            if (iterations === maxIterations) console.log('Belongs to Mandelbrot set:', [x, y]);
        }
    }
}

// Taylor Series for e^x
function taylorExp(x, terms = 10) {
    let sum = 0;
    for (let n = 0; n < terms; n++) {
        sum += Math.pow(x, n) / factorial(n);
    }
    return sum;
}

// Main
function main() {
    trigDemo(PI / 4);
    matrixDemo();
    console.log('Factorial of 5:', factorial(5));
    console.log('Fibonacci (10 terms):', fibonacci(10));
    console.log('Sum of primes up to 100:', sumOfPrimes(100));
    console.log('Quadratic roots:', solveQuadratic(1, -3, 2));
    console.log('E=mc^2 for m=1kg:', massEnergy(1));
    console.log('Gravitational force:', gravitationalForce(5.972e24, 1.989e30, 1.496e11));
    console.log('DNA replication probability:', dnaReplicationProbability(0.99, 10));
    console.log('Enzyme kinetics:', enzymeKinetics(100, 5, 10));
    console.log('Radioactive decay:', radioactiveDecay(100, 5730, 1000));
    mandelbrotSetDemo(50);
    console.log('Taylor series of e^1:', taylorExp(1));
}

main();