from app.math_utils import factorial, is_prime
from app.data_processor import DataProcessor

def main():
    print("Factorial of 5:", factorial(5))
    print("Is 13 prime?", is_prime(13))

    data = [10, 20, 30, 40]
    processor = DataProcessor(data)
    print("Normalized data:", processor.normalize())

if __name__ == "__main__":
    main()
