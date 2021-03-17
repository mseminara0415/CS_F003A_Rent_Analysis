""" Greet users and ask for their name. Ask user what home currency
they have and print out conversion table based on their selected home currency.
Asks users to enter a header for their dataset that will be displayed above the
menu.The main menu is printed and asks users for their selected option.
"""

from enum import Enum

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


class DataSet:
    """
    Class to manage our dataset.
    """
    header_max_length = 30
    copyright = "No copyright has been set"

    def __init__(self, header=""):
        try:
            self.header = header
        except ValueError:
            self.header = ""

        self._data = None
        self._labels = {}
        self._active_labels = {}

    class EmptyDatasetError(Exception):
        def __init__(self, message):
            self.message = message

    class NoMatchingItems(Exception):
        def __init__(self, message):
            self.message = message

    class Categories(Enum):
        LOCATION = 0
        PROPERTY_TYPE = 1

    class Stats(Enum):
        MIN = 0
        AVG = 1
        MAX = 2

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header: str):
        if len(header) <= DataSet.header_max_length:
            self._header = header
        else:
            raise ValueError("Header must be <= 30 characters")

    def _initialize_sets(self):
        """ Examine the category labels in self.__data and create a set
        for each category containing the labels.
        :return:
        """
        if self._data is None:
            raise DataSet.EmptyDatasetError("Please load data.")
        else:
            location_list = [location[
                                 DataSet.Categories.LOCATION.value]
                             for location in self._data]

            prop_list = [location[
                             DataSet.Categories.PROPERTY_TYPE.value]
                         for location in self._data]

            self._labels = {DataSet.Categories.LOCATION: set(
                location_list), DataSet.Categories.PROPERTY_TYPE: set(
                prop_list)}

            self._active_labels = self._labels.copy()

    def _cross_table_statistics(self, descriptor_one: str,
                                descriptor_two: str):
        """
        Find data that matches both descriptors.
        :param descriptor_one:
        :param descriptor_two:
        :return: tuple that includes min,avg,max of matching data
        """
        if self._data is None:
            raise DataSet.EmptyDatasetError("Please load data.")
        else:
            matching = [test for test in self._data if test[0] ==
                        descriptor_one and test[1] == descriptor_two]
            if not matching:
                raise DataSet.NoMatchingItems("No matching items.")
            else:
                rents = [rent[2] for rent in matching]
                avg = sum(rents) / len(rents)

                return min(rents), avg, max(rents)

       def display_cross_table(self, stat: Stats):
        """
        Displays table stats.
        :param stat:
        :return:
        """
        if self._data is None:
            raise DataSet.EmptyDatasetError("Please load data.")
        else:

            # Print Headers (Property Types)
            location_list = list(self._labels[DataSet.Categories.LOCATION])
            location_list.sort()
            property_list = list(self._labels[DataSet.Categories.PROPERTY_TYPE])
            property_list.sort()

            print(f"               ", end="")
            # Print Header
            for property_name in property_list:
                print(f"{property_name:20}", end=' ')
            print()
            for location in location_list:
                print(f"{location:15}", end=' ')
                for property_type in property_list:
                    try:
                        print(f"""$ {self._cross_table_statistics(location,
                                                         property_type)[stat.value]
                        :<18.2f}""", end=' ')
                    except DataSet.NoMatchingItems:
                        print(f"$ {'N/A':<18}", end=' ')
                print()

    def load_default_data(self):
        """
        Load dataset.
        :return:
        """
        self._data = [('Staten Island', 'Private room', 70),
                      ('Brooklyn', 'Private room', 50),
                      ('Bronx', 'Private room', 40),
                      ('Brooklyn', 'Entire home / apt', 150),
                      ('Manhattan', 'Private room', 125),
                      ('Manhattan', 'Entire home / apt', 196),
                      ('Brooklyn', 'Private room', 110),
                      ('Manhattan', 'Entire home / apt', 170),
                      ('Manhattan', 'Entire home / apt', 165),
                      ('Manhattan', 'Entire home / apt', 150),
                      ('Manhattan', 'Entire home / apt', 100),
                      ('Brooklyn', 'Private room', 65),
                      ('Queens', 'Entire home / apt', 350),
                      ('Manhattan', 'Private room', 98),
                      ('Brooklyn', 'Entire home / apt', 200),
                      ('Brooklyn', 'Entire home / apt', 150),
                      ('Brooklyn', 'Private room', 99),
                      ('Brooklyn', 'Private room', 120)]

        # Initialize Labels
        self._initialize_sets()


def menu(dataset: DataSet):
    """
    Display the main menu and obtain users selection.
    :return:
    """

    # Print Currency Options
    currency_options(home_currency)

    # Print Copyright
    print(f"\n\n{dataset.copyright}")

    # Print Header
    print(f"{dataset.header}")

    # Print Main Menu
    main_menu = print_menu()

    # Ask the user for main menu selection
    while True:
        try:
            print()
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
        if selected_option == 1:
            try:
                dataset.display_cross_table(dataset.Stats.AVG)
                continue
            except dataset.EmptyDatasetError:
                print("Please load Data first.")
                continue

        if selected_option == 2:
            try:
                dataset.display_cross_table(dataset.Stats.MIN)
                continue
            except dataset.EmptyDatasetError:
                print("Please load Data first.")
                continue

        if selected_option == 3:
            try:
                dataset.display_cross_table(dataset.Stats.MAX)
                continue
            except dataset.EmptyDatasetError:
                print("Please load Data first.")
                continue

        if selected_option == 8:
            dataset.load_default_data()
            print("Data Set successfully loaded.")
            continue

        if selected_option == 9:
            print("Goodbye! See you next time")
            break

        else:

            print(f"Sorry, '{main_menu[selected_option]}' "
                  f"functionality is not implemented yet.")
        break


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

    return target_currency_converted


def unit_test():
    """
    Test currency converter function to see if it meets requirements.
    :return:
    """

    try:
        currency_converter(1, "USE", "USD")
    except KeyError:
        print("PASS: Invalid Source Currency Raises ValueError")
    else:
        print("FAIL: Invalid Source Currency Does Not Raise Error")
    try:
        currency_converter(1, "USD", "USE")
    except KeyError:
        print("PASS: Invalid Target Currency Raises ValueError")
    else:
        print("FAIL: Invalid Target Currency Does Not Raise ValueError")
    if currency_converter(10, "USD", "GBP") == 8:
        print("PASS: Conversion from USD to GBP")
    else:
        print("FAIL: Conversion from USD to GBP")
    if currency_converter(2.8, "CAD", "USD") == 2:
        print("PASS: Conversion from CAD to USD")
    else:
        print("FAIL: Conversion from CAD to USD")
    if currency_converter(1.8, "EUR", "CAD") == 2.8:
        print("PASS: Conversion from EUR to CAD")
    else:
        print("FAIL: Conversion from EUR to CAD")


def class_unit_test():
    """
    Unit test to make sure our class DataSet meets specifications.
    :return:
    """
    test1 = DataSet()
    test2 = DataSet("Less than 30 characters")
    test3 = DataSet("More than 30 characters long is not going to work")
    test4 = DataSet()
    test5 = DataSet()

    if test1.header == "":
        print("Testing constructor with default parameter: Pass")
    else:
        print("Testing constructor with default parameter: Fail")
    if test2.header == "Less than 30 characters":
        print("Testing constructor with valid header argument: Pass")
    else:
        print("Testing constructor with valid header argument: Fail")
    if test3.header == "":
        print("Testing constructor with invalid header argument: Pass")
    else:
        print("Testing constructor with invalid header argument: Fail")
    try:
        test4.header = "This should work"
        if test4.header == "This should work":
            print("Testing setter with valid assignment: Pass")
    except ValueError:
        print("Testing setter with valid assignment: Fail")
    try:
        test5.header = "This should not work since more than 30"
        if test5.header == "This should not work since more than 30":
            print("Testing setter with invalid assignment: Fail")
    except ValueError:
        print("Testing setter with invalid assignment: Pass")
    DataSet.copyright = "copyright Matt Seminara unit test"
    if DataSet.copyright == "copyright Matt Seminara unit test":
        print("Checking that I can access Dataset.copyright: Pass")
    else:
        print("Checking that I can access Dataset.copyright: Fail")
    test6 = DataSet()
    if test6.copyright == "copyright Matt Seminara unit test":
        print("Setting Dataset.copyright = 'copyright Matt Seminara "
              "unit test'")
        print(
            "Checking that I can access copyright after creating an object: Pass")
    else:
        print(
            "Checking that I can access copyright after creating an object: Fail")


def data_unit_test():
    my_set = DataSet()

    try:
        my_set._cross_table_statistics("no data", "no data")
    except DataSet.EmptyDatasetError:
        print("Method Raises EmptyDataSet Error: Pass")
    else:
        print("Method Raises EmptyDataSet Error: Fail")

    # Load Data
    my_set.load_default_data()

    try:
        my_set._cross_table_statistics("Bronx", "duplex")
    except DataSet.NoMatchingItems:
        print("Invalid Property Type Raises NoMatchingItems Error: "
              "Pass")
    else:
        print("Invalid Property Type Raises NoMatchingItems Error: "
              "Fail")
    try:
        my_set._cross_table_statistics("Los Angeles", "Private room")
    except DataSet.NoMatchingItems:
        print("Invalid Borough Raises NoMatchingItems Error: Pass")
    else:
        print("Invalid Borough Raises NoMatchingItems Error: Fail")

    try:
        my_set._cross_table_statistics("Staten Island", "Entire home "
                                                        "/ apt")
    except DataSet.NoMatchingItems:
        print("No Matching Rows Raises NoMatchingItems: Pass")
    else:
        print("No Matching Rows Raises NoMatchingItems: Fail")

    test1 = my_set._cross_table_statistics("Staten Island",
                                           "Private room")

    if test1 == (70, 70, 70):
        print("One Matching Row Returns Correct Tuple: Pass")
    else:
        print("One Matching Row Returns Correct Tuple: Fail")

    test2 = my_set._cross_table_statistics("Manhattan", "Private room")

    if test2 == (98, 111.5, 125):
        print("Multiple Matching Rows Returns Correct Tuple: Pass")
    else:
        print("Multiple Matching Rows Returns Correct Tuple: Fail")


def currency_options(base_currency: str):
    """
    Prints out currency option table, which shows conversion rates
    against their selected home currency.
    :param base_currency:
    :return:
    """
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
            print(
                f"""{currency_converter(quantity,
                                        base_currency,
                                        currency):<10.2f}""",
                end=' ')


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

    while home_currency not in conversions:
        home_currency = input("What is your home currency?").upper()

    DataSet.copyright = "copyright Matthew Seminara"
    air_bnb = DataSet()
    while True:
        try:
            if air_bnb.header == "":
                air_bnb.header = input("Enter a header for the menu:")
            break
        except ValueError:
            continue

    # Print main menu and ask for users input
    menu(air_bnb)


if __name__ == '__main__':

    main()
