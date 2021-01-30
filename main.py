""" This program runs a unit test against the  'currency converter'
function to see if it meets the expected criteria.
"""

conversions = {
    "USD": 1,
    "EUR": .9,
    "CAD": 1.4,
    "GBP": .8,
    "CHF": .95,
    "NZD": 1.66,
    "AUD": 1.62,
    "JPY": 107.92
}


def print_menu():
    """
    Print the main menu options.
    :return: Dictionary of main menu choices.
    """

    print("Main Menu")

    # Dictionary containing menu options
    menu_options = {
            1: 'Print Average Rent by Location and Property '
               'Type',
            2: 'Print Minimum Rent by Location and Property '
               'Type',
            3: 'Print Maximum Rent by Location and Property '
               'Type',
            4: 'Print Min/Avg/Max by Location',
            5: 'Print Min/Avg/Max by Property Type',
            6: 'Adjust Location Filters',
            7: 'Adjust Property Type Filters',
            8: 'Load Data',
            9: 'Quit'}

    # Print main menu options
    for option_number, option in menu_options.items():
        print(f"{option_number} - {option}")

    return menu_options


def menu():
    """
    Display the main menu and obtain users selection.
    :return:
    """

    # Prints Main Menu
    main_menu = print_menu()

    # Ask the user for main menu selection
    while True:
        try:
            selected_option = int(input("What is your choice? "))
        except ValueError:
            print_menu()
            print("Try again. Please enter a valid number only.")
            continue
        if selected_option < 1 or selected_option > 9:
            print_menu()
            print("Try again. Please select a number from "
                  "1-9.")
            continue
        if selected_option == 9:
            print("Goodbye! See you next time")
            break

        print(f"Sorry, '{main_menu[selected_option]}' "
              f"functionality is not implemented yet.")
        break


def main():
    """
    Obtain the user's name and greet them. After welcoming the user,
    display the main menu and ask for users selection while
    responding accordingly.
    :return:
    """

    # Ask the user for their name and greet them
    name = input("Hello, please enter your name: ")
    print(f"Hey {name}, welcome to our class project!")

    # Print main menu and ask for users input
    menu()


def currency_converter(quantity: float, source_curr: str,
                       target_curr: str):
    """
    Convert from one currency to another.
    :param quantity:
    :param source_curr:
    :param target_curr:
    :return: source currency, target currency, conversion value
    """

    # Test to see if the currencies selected are in the dictionary
    if source_curr not in conversions or target_curr not in \
            conversions or quantity <= 0:
        raise KeyError

    source_in_usd = quantity / conversions[source_curr]

    target_currency_converted = source_in_usd * conversions[target_curr]

    return source_curr, target_curr, target_currency_converted


def unit_test():
    """
    Test currency converter function to see if it meets requirements.
    :return:
    """

    test_3 = currency_converter(10, "USD", "GBP")
    test_4 = currency_converter(2.8, "CAD", "USD")
    test_5 = currency_converter(1.8, "EUR", "CAD")

    # Invalid Source Currency
    try:
        currency_converter(2.8, "BAD", "USD")
    except KeyError:
        print("PASS: Invalid Source Currency Raises KeyError")
    else:
        print("FAIL: Invalid Source Currency Does Not Raise An Error")

    # Invalid Target Currency
    try:
        currency_converter(2.8, "USD", "BAD")
    except KeyError:
        print("PASS: Invalid Target Currency Raises KeyError")
    else:
        print("FAIL: Invalid Target Currency Does Not Raise ValueError")

    # Test USD to another currency
    if test_3[2] == 8.0:
        print(f"PASS: Successful conversion from {test_3[0]} to "
              f"{test_3[1]}")
    else:
        print(f"FAIL: Unsuccessful Conversion from {test_3[0]} to "
              f"{test_3[1]}")

    # Test conversion from another currency to USD
    if test_4[2] == 2.0:
        print(f"PASS: Successful conversion from {test_4[0]} to "
              f"{test_4[1]}")
    else:
        print(f"FAIL: Unsuccessful Conversion from {test_4[0]} to "
              f"{test_4[1]}")

    # Conversion between two currencies other than USD
    if test_5[2] == 2.8:
        print(f"PASS: Successful conversion from {test_5[0]} to "
              f"{test_5[1]}")
    else:
        print(f"FAIL: Unsuccessful Conversion from {test_5[0]} to "
              f"{test_5[1]}")


if __name__ == '__main__':
    unit_test()
    # main()

"""
------ Sample Run Unit Test ------
PASS: Invalid Source Currency Raises KeyError
PASS: Invalid Target Currency Raises KeyError
PASS: Successful conversion from USD to GBP
PASS: Successful conversion from CAD to USD
PASS: Successful conversion from EUR to CAD
"""
