/**
 * Copilot Demonstration - Utility Functions
 * This file demonstrates common programming patterns that GitHub Copilot can assist with
 */

/**
 * Calculate the sum of an array of numbers
 * @param {number[]} numbers - Array of numbers to sum
 * @returns {number} The sum of all numbers
 */
function sum(numbers) {
  return numbers.reduce((acc, num) => acc + num, 0);
}

/**
 * Calculate the average of an array of numbers
 * @param {number[]} numbers - Array of numbers
 * @returns {number} The average value
 */
function average(numbers) {
  if (numbers.length === 0) return 0;
  return sum(numbers) / numbers.length;
}

/**
 * Check if a string is a palindrome
 * @param {string} str - String to check
 * @returns {boolean} True if palindrome, false otherwise
 */
function isPalindrome(str) {
  const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
  return cleaned === cleaned.split('').reverse().join('');
}

/**
 * Capitalize the first letter of each word in a string
 * @param {string} str - Input string
 * @returns {string} String with capitalized words
 */
function capitalizeWords(str) {
  return str.split(' ').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
  ).join(' ');
}

/**
 * Generate a random integer between min and max (inclusive)
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {number} Random integer
 */
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Export functions for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    sum,
    average,
    isPalindrome,
    capitalizeWords,
    randomInt
  };
}

// Demonstration usage
console.log('Copilot Demonstration:');
console.log('Sum of [1,2,3,4,5]:', sum([1, 2, 3, 4, 5]));
console.log('Average of [10,20,30]:', average([10, 20, 30]));
console.log('Is "racecar" a palindrome?', isPalindrome('racecar'));
console.log('Capitalize "hello world":', capitalizeWords('hello world'));
console.log('Random number between 1-10:', randomInt(1, 10));
