from typing import Callable
from typing import Iterator
import re

"""Generator of real numbers found in text."""
def generator_numbers(text: str) -> Iterator[float]:
    for value in re.finditer(r'\d+\.\d+', text):
        yield float(value.group())

"""Sum of real numbers extracted from text using a generator function."""
def sum_profit(text: str, generator_func: Callable[[str], Iterator[float]]) -> float:
    total = 0.0
    for number in generator_func(text):
        total += number
    return total

if __name__ == "__main__":
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}") # 1351.46
