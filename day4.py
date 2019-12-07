MIN_NUMBER = 359282
MAX_NUMBER = 820401


def is_potential_password(number):
    has_same_adjacent_digit = False
    prev_digit = number % 10
    number = number // 10

    while number > 0:
        rest = number % 10
        number = number // 10
        if rest > prev_digit:
            return False

        if rest == prev_digit:
            has_same_adjacent_digit = True

        prev_digit = rest

    return has_same_adjacent_digit


def run_program(min_number, max_number):
    potential_passwords = 0
    for i in range(min_number, max_number):
        if is_potential_password(i):
            potential_passwords += 1

    return potential_passwords


if __name__ == '__main__':
    print(run_program(MIN_NUMBER, MAX_NUMBER))