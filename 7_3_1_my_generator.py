def my_generator(text):
    i = 0
    while i < len(text):
        yield text[i]
        i += 1


def main():
    s = 'Hello world!'
    one_letter_at_a_time = my_generator(s)
    for _ in s:
        print(next(one_letter_at_a_time))
    return 0


if __name__ == '__main__':
    main()
