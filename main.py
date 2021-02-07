""" Greet users and ask for their name. Ask user what home currency
they have and print out conversion rates based on other currencies.
Prints main menu and asks users for their choice.
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

home_currency = ''


def print_menu():
    """
    Print the main menu options.
    :return: Dictionary of main menu choices.
    """

    print("\nMain Menu")

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

    # Select currency
    global home_currency
    while True:
        home_currency = input("What is your home currency?").upper()
        if home_currency in conversions.keys():
            currency_options(home_currency)
            break
        else:
            print("Please select a valid currency.")
            home_currency = ''
            continue

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
    if test_3[2] == 8:
        print(f"PASS: Successful conversion from {test_3[0]} to "
              f"{test_3[1]}")
    else:
        print(f"FAIL: Unsuccessful Conversion from {test_3[0]} to "
              f"{test_3[1]}")

    # Test conversion from another currency to USD
    if test_4[2] == 2:
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


def currency_options(base_currency: str):
    print(f"Options for converting from {base_currency}:")

    currency_list = [currency for currency in conversions]

    currency_list.remove(base_currency)

    currency_list.insert(0, base_currency)

    quantities = range(10, 91, 10)

    # Print Header Line
    for currency in currency_list:
        print(f"{currency:10}", end=' ')

    for quantity in quantities:
        print()
        for currency in currency_list:
            print(f""
                  f"{currency_converter(quantity, base_currency,currency)[2]:<10.2f}", end=' ')


if __name__ == '__main__':
    # unit_test()
    main()

"""
------ Sample Run Unit Test ------
Hello, please enter your name: Matt
Hey Matt, welcome to our class project!
What is your home currency?BAD
Please select a valid currency.
What is your home currency?GBP
Options for converting from GBP:
GBP        USD        EUR        CAD        CHF        NZD        AUD        JPY        
10.00      12.50      11.25      17.50      11.88      20.75      20.25      1349.00    
20.00      25.00      22.50      35.00      23.75      41.50      40.50      2698.00    
30.00      37.50      33.75      52.50      35.62      62.25      60.75      4047.00    
40.00      50.00      45.00      70.00      47.50      83.00      81.00      5396.00    
50.00      62.50      56.25      87.50      59.38      103.75     101.25     6745.00    
60.00      75.00      67.50      105.00     71.25      124.50     121.50     8094.00    
70.00      87.50      78.75      122.50     83.12      145.25     141.75     9443.00    
80.00      100.00     90.00      140.00     95.00      166.00     162.00     10792.00   
90.00      112.50     101.25     157.50     106.88     186.75     182.25     12141.00   
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
What is your choice? 
"""
