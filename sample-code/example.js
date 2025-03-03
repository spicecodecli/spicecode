// Weird Math Program in JavaScript

// Function to calculate the sum of squares
function sumOfSquares(n) {
    let sum = 0;
    for (let i = 1; i <= n; i++) {
        sum += i * i; // Squaring the number and adding to sum
    }
    return sum;
}

// Function to calculate factorial
function factorial(n) {
    let result = 1;
    for (let i = 1; i <= n; i++) {
        result *= i; // Multiplying each number to get factorial
    }
    return result;
}

// Random number generator to mess things up
function randomize(n) {
    return Math.floor(Math.random() * n);
}

// Main function
function main() {
    let num = 10;
    let randomNum = randomize(num);

    console.log("Random Number:", randomNum);
    console.log("Sum of squares up to", num, ":", sumOfSquares(num));
    console.log("Factorial of", num, ":", factorial(num));

    // Using random number to generate some weird results
    let weirdResult = sumOfSquares(randomNum) + factorial(randomNum);
    console.log("Weird result using random number:", weirdResult);
}

// Call main function
main();