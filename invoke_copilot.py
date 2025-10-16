#!/usr/bin/env python3
"""
Simple example demonstrating how to invoke GitHub Copilot functionality.
This script shows the basic structure for interacting with AI-powered code completion.
"""

def main():
    """
    Main function that demonstrates invoking Copilot-like functionality.
    """
    print("Invoking Copilot...")
    
    # Example: Request code completion
    prompt = "Write a function to calculate factorial"
    print(f"Prompt: {prompt}")
    
    # Simulated response (in a real scenario, this would call the Copilot API)
    response = generate_factorial_function()
    print(f"\nGenerated code:\n{response}")
    
    print("\nCopilot invocation completed successfully!")


def generate_factorial_function():
    """
    Simulated Copilot response for factorial function.
    In a real implementation, this would call the GitHub Copilot API.
    """
    return """def factorial(n):
    \"\"\"Calculate the factorial of a number.\"\"\"
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)"""


if __name__ == "__main__":
    main()
