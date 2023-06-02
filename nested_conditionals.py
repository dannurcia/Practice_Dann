
def print_interval(value):
    interval = {
        value < 100: "Less than 100",
        100 <= value < 150: "Between 100 and 150",
        value >= 150: "Value is greater than or equal 150"
    }
    print(interval[True])


def print_value(value):
    values = {
        125: "It is 125",
        100: "It is 100",
        75: "It is 75",
        50: "It is 50",
        25: "It is 25"
    }
    print(values.get(value))


def main():
    # val = 125
    print("Introduzca un número menor a 200: ", end="")
    val = int(input())

    if val < 200:
        print("Value is less than 200")
        print_interval(val)
        print_value(val)
    else:
        print("Value is more than 200")


if __name__ == "__main__":
    main()
