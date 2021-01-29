""" This program asks a user for their name, and responds with a
friendly greeting. After greeting the user, a main menu is displayed
and the program asks them to select one of the options while
responding accordingly.
"""


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


def currency_converter(quantity: float, source_curr: str,
                       target_curr: str):

    source_in_usd = quantity * conversions["USD"] / conversions[
        source_curr]

    target_currency_converted = source_in_usd * conversions[target_curr]

    return source_curr, target_curr, target_currency_converted


def unit_test():
    test_3 = currency_converter(2.8, "USD", "CAD")
    test_4 = currency_converter(2.8, "CAD", "USD")
    test_5 = currency_converter(10, "JPY", "EUR")

    try:
        currency_converter(2.8, "BAD", "USD")
    except KeyError:
        print("PASS: Invalid Source Currency Raises KeyError")
    try:
        currency_converter(2.8, "USD", "BAD")
    except KeyError:
        print("PASS: Invalid Source Currency Raises KeyError")

    # Test USD to another currency
    try:
        print(f"PASS: Successful conversion from {test_3[0]} to "
              f"{test_3[1]}")
    except:
        print(f"FAIL: Unsuccessful Conversion from {test_3[0]} to "
              f"{test_3[1]}")

    # Test another currency to USD
    try:
        print(f"PASS: Successful conversion from {test_4[0]} to "
              f"{test_4[1]}")
    except:
        print(f"FAIL: Unsuccessful Conversion from {test_4[0]} to "
              f"{test_4[1]}")

    # Conversion between two currencies other than USD
    try:
        print(f"PASS: Successful conversion from {test_5[0]} to "
              f"{test_5[1]}")
    except:
        print(f"FAIL: Unsuccessful Conversion from {test_5[0]} to "
              f"{test_5[1]}")


if __name__ == '__main__':

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

    unit_test()

    # main()

"""
------ Sample Run 1 (Valid Input #1) ------

Hello, please enter your name: Matt
Hey Matt, welcome to our class project!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 1
Sorry, 'Print Average Rent by Location and Property Type' functionality is not implemented yet.

------ Sample Run 2 (Valid Input #2) ------

Hello, please enter your name: James
Hey James, welcome to our class project!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 4
Sorry, 'Print Min/Avg/Max by Location' functionality is not implemented yet.

------ Sample Run 3 (Valid Input #3) ------

Hello, please enter your name: Matt
Hey Matt, welcome to our class project!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 9
Goodbye! See you next time

------ Sample Run 4 (Invalid Input #1) ------

Hey Sarah, welcome to our class project!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 15
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
Try again. Please select a number from 1-9.
What is your choice?

------ Sample Run 5 (Invalid Input #2) ------

Hello, please enter your name: Kevin
Hey Kevin, welcome to our class project!
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? e
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
Try again. Please enter a valid number only.
What is your choice?
"""
