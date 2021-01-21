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
        else:
            if selected_option < 1 or selected_option > 9:
                print_menu()
                print("Try again. Please select a number from "
                      "1-9.")
            else:
                print(f"Sorry, '{main_menu[selected_option]}' "
                      f"functionality is not implemented yet.")
                break


if __name__ == '__main__':
    main()

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

------ Sample Run 3 (Invalid Input #1) ------

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

------ Sample Run 4 (Invalid Input #2) ------

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
