MIN_NUMBER = 359282
MAX_NUMBER = 820401


def is_potential_password(number):
    has_same_adjacent_digit = False
    adjacent_same_digit_count = 1
    prev_digit = number % 10
    number = number // 10

    while number > 0:
        rest = number % 10
        number = number // 10
        if rest > prev_digit:
            return False

        if not has_same_adjacent_digit:
            if rest == prev_digit:
                if adjacent_same_digit_count == 1:
                    adjacent_same_digit_count += 1
                    has_same_adjacent_digit = True
            else:
                adjacent_same_digit_count = 1
        else:
            if rest == prev_digit:
                if adjacent_same_digit_count == 2:
                    has_same_adjacent_digit = False
                    adjacent_same_digit_count += 1
            else:
                adjacent_same_digit_count = 1

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