def factorial(n: int) -> int:
    if n == 0:
        return 1
    return n * factorial(n - 1)

def is_prime(n: int) -> bool:
    """判断数字是否为质数"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
