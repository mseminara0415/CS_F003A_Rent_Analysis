""" Greets users and asks for name, currency, and a header that will be
displayed. A menu is displayed where users have the option to view slices
of the data based on locations or property types, also giving the functionality
to enable/disable individual locations/properties. Data is loaded
from a csv with over 48,000 data points.
"""

from enum import Enum
import csv


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

filename = './AB_NYC_2019.csv'


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

    header_max_length = 30
    copyright = "No copyright has been set"

    def __init__(self, header=""):
        self._active_labels = {DataSet.Categories.LOCATION: set(),
                               DataSet.Categories.PROPERTY_TYPE: set()}
        self._labels = {DataSet.Categories.LOCATION: set(),
                        DataSet.Categories.PROPERTY_TYPE: set()}
        self._data = None
        try:
            self.header = header
        except ValueError:
            self.header = ""

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
                """
        if not self._data:
            raise DataSet.EmptyDatasetError
        for category in self.Categories:
            self._labels[category] = set([i[category.value]
                                          for i in self._data])

            self._active_labels[category] = self._labels[
                category].copy()

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

    def _table_statistics(self, row_category: Categories, label: str):
        """
        Calculates min, max, and average based on the selected category and
        the current set of active labels.
        :param row_category:
        :param label:
        :return:
        """

        active_properties = self._active_labels[row_category.PROPERTY_TYPE]
        active_locations = self._active_labels[row_category.LOCATION]

        if row_category == self.Categories.LOCATION:
            matching = [_property for _property in self._data
                        if _property[0] == label
                        and _property[1] in active_properties]

        elif row_category == self.Categories.PROPERTY_TYPE:
            matching = [location for location in self._data
                        if location[0] in active_locations
                        and location[1] == label]
        else:
            matching = []

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
            location_list = list(
                self._labels[DataSet.Categories.LOCATION])
            location_list.sort()
            property_list = list(
                self._labels[DataSet.Categories.PROPERTY_TYPE])
            property_list.sort()
            print(f"               ", end="")
            for item in property_list:
                print(f"{item:20}", end="")
            print()
            for item_one in location_list:
                print(f"{item_one:15}", end="")
                for item_two in property_list:
                    try:
                        value = self._cross_table_statistics(item_one,
                                                             item_two)[
                            stat.value]
                        print(f"$ {value:<18.2f}", end="")
                    except DataSet.NoMatchingItems:
                        print(f"$ {'N/A':<18}", end="")
                print()

    def display_field_table(self, rows: Categories):
        """
        Displays min, max, and average data based on a filtered dataset.
        :param rows:
        :return:
        """
        if self._data is None:
            raise DataSet.EmptyDatasetError("Please load data.")
        else:
            active_labels = self._active_labels[rows]

            # Print Header Line
            if rows == rows.PROPERTY_TYPE:
                print("The location data matches the following criteria:")
                for item in self._active_labels[rows.LOCATION]:
                    print(item)
            else:
                print("The property data matches the following criteria:")
                for item in self._active_labels[rows.PROPERTY_TYPE]:
                    print(item)

            print(f"                         ", end="")
            print(f"{'Minimum':20}{'Maximum':20}{'Average':520}")
            for item in active_labels:
                print(f"{item:25}", end="")

                for header in range(3):
                    try:
                        value = self._table_statistics(rows, item)[header]
                        print(f"$ {value:<18.2f}", end="")
                    except DataSet.NoMatchingItems:
                        print(f"$ {'N/A':<18}", end="")
                print()

    def get_labels(self, category: Categories):
        """
        Returns a list of the items in _labels[category].
        :param category:
        :return:
        """
        return [item for item in self._labels[category]]

    def get_active_labels(self, category: Categories):
        """
        Return a list of items in _labels[category].
        :param category:
        :return:
        """
        return [item for item in self._active_labels[category]]

    def toggle_active_label(self, category: Categories, descriptor: str):
        """
        Add or remove labels from _active_labels allowing the user
        to filter out certain property types or locations.
        :param category:
        :param descriptor:
        :return:
        """
        if descriptor not in self._labels[category]:
            raise KeyError
        elif descriptor not in self._active_labels[category]:
            self._active_labels[category].add(descriptor)
        else:
            self._active_labels[category].remove(descriptor)

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

    def load_file(self, file_name):
        """
        Load Data from file. .
        :return:
        """

        # Load in data from file
        file_to_open = open(file_name, mode="r", newline='')
        csv_reader = csv.reader(file_to_open)

        # Create list of tuples in same format as method 'Load
        # Default Data'
        data_original = [tuple(row)[1:] for row in csv_reader][1:]
        data_formatted = [(x[0], x[1], int(x[2])) for x in
                          data_original]

        # Determine how many lines of data are in the file
        n_lines = len(data_original)
        self._data = data_formatted

        # Initialize Labels
        self._initialize_sets()

        return n_lines


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
            print()
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

        if selected_option == 4:
            try:
                locations = dataset.Categories.LOCATION
                dataset.display_field_table(locations)
                continue
            except dataset.EmptyDatasetError:
                print("Please load Data first.")
                continue

        if selected_option == 5:
            try:
                properties = dataset.Categories.PROPERTY_TYPE
                dataset.display_field_table(properties)
                continue
            except dataset.EmptyDatasetError:
                print("Please load Data first.")
                continue

        if selected_option == 6:
            try:
                manage_filters(dataset, dataset.Categories.LOCATION)
                print_menu()
                continue
            except dataset.EmptyDatasetError:
                print("Please load Data first.")
                continue

        if selected_option == 7:
            try:
                manage_filters(dataset,
                               dataset.Categories.PROPERTY_TYPE)
                print_menu()
                continue
            except dataset.EmptyDatasetError:
                print("Please load Data first.")
                continue

        if selected_option == 8:
            n_lines = dataset.load_file(file_name=filename)
            print(f"Data Set successfully loaded {n_lines} lines.")
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
            "Checking that I can access copyright after creating an "
            "object: Pass")
    else:
        print(
            "Checking that I can access copyright after creating an "
            "object: Fail")


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


def manage_filters(dataset: DataSet, category: DataSet.Categories):
    """
    Displays the active labels and allows users to enable/disable which ones
    are in the filter criteria for the data.
    :param dataset:
    :param category:
    :return:
    """

    labels = dataset.get_labels(category)
    labels.sort()

    while True:
        active_labels = dataset.get_active_labels(category)
        active_labels.sort()
        print("The following labels are in the dataset:")
        for i, label in enumerate(labels, 1):
            status = "ACTIVE" if label in active_labels else "INACTIVE"
            print(f"{i}: {label:25}{status}")
        select_option = input("Please select an option number to "
                              "toggle. Type 'Exit' to return to menu.")

        try:
            if select_option == "Exit".lower()\
                    or select_option == "Exit".upper()\
                    or select_option == "Exit".title():
                break
            else:
                dataset.toggle_active_label(category,
                                            labels[int(select_option)-1])
        except (IndexError, ValueError):
            print()
            print("Please select one of the listed options only.")


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

"""
========== Sample Run ==========
Hello, please enter your name: Matt
Hey Matt, welcome to our class project!
What is your home currency?usd
Enter a header for the menu:header
Options for converting from USD:
USD        EUR        CAD        GBP        CHF        NZD        AUD        JPY        
10.00      9.00       14.00      8.00       9.50       16.60      16.20      1079.20    
20.00      18.00      28.00      16.00      19.00      33.20      32.40      2158.40    
30.00      27.00      42.00      24.00      28.50      49.80      48.60      3237.60    
40.00      36.00      56.00      32.00      38.00      66.40      64.80      4316.80    
50.00      45.00      70.00      40.00      47.50      83.00      81.00      5396.00    
60.00      54.00      84.00      48.00      57.00      99.60      97.20      6475.20    
70.00      63.00      98.00      56.00      66.50      116.20     113.40     7554.40    
80.00      72.00      112.00     64.00      76.00      132.80     129.60     8633.60    
90.00      81.00      126.00     72.00      85.50      149.40     145.80     9712.80    

copyright Matthew Seminara
header
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

Please load Data first.

What is your choice? 8

Data Set successfully loaded 48895 lines.

What is your choice? 1

               Entire home/apt     Private room        Shared room         
Bronx          $ 127.51            $ 66.79             $ 59.80             
Brooklyn       $ 178.33            $ 76.50             $ 50.53             
Manhattan      $ 249.24            $ 116.78            $ 88.98             
Queens         $ 147.05            $ 71.76             $ 69.02             
Staten Island  $ 173.85            $ 62.29             $ 57.44             

What is your choice? 2

               Entire home/apt     Private room        Shared room         
Bronx          $ 28.00             $ 0.00              $ 20.00             
Brooklyn       $ 0.00              $ 0.00              $ 0.00              
Manhattan      $ 0.00              $ 10.00             $ 10.00             
Queens         $ 10.00             $ 10.00             $ 11.00             
Staten Island  $ 48.00             $ 20.00             $ 13.00             

What is your choice? 3

               Entire home/apt     Private room        Shared room         
Bronx          $ 1000.00           $ 2500.00           $ 800.00            
Brooklyn       $ 10000.00          $ 7500.00           $ 725.00            
Manhattan      $ 10000.00          $ 9999.00           $ 1000.00           
Queens         $ 2600.00           $ 10000.00          $ 1800.00           
Staten Island  $ 5000.00           $ 300.00            $ 150.00            

What is your choice? 4

The property data matches the following criteria:
Entire home/apt
Private room
Shared room
                         Minimum             Maximum             Average                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
Brooklyn                 $ 0.00              $ 124.38            $ 10000.00          
Staten Island            $ 13.00             $ 114.81            $ 5000.00           
Bronx                    $ 0.00              $ 87.50             $ 2500.00           
Manhattan                $ 0.00              $ 196.88            $ 10000.00          
Queens                   $ 10.00             $ 99.52             $ 10000.00          

What is your choice? 5

The location data matches the following criteria:
Brooklyn
Staten Island
Bronx
Manhattan
Queens
                         Minimum             Maximum             Average                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
Entire home/apt          $ 0.00              $ 211.79            $ 10000.00          
Private room             $ 0.00              $ 89.78             $ 10000.00          
Shared room              $ 0.00              $ 70.13             $ 1800.00           

What is your choice? 6

The following labels are in the dataset:
1: Bronx                    ACTIVE
2: Brooklyn                 ACTIVE
3: Manhattan                ACTIVE
4: Queens                   ACTIVE
5: Staten Island            ACTIVE
Please select an option number to toggle. Type 'Exit' to return to menu.3
The following labels are in the dataset:
1: Bronx                    ACTIVE
2: Brooklyn                 ACTIVE
3: Manhattan                INACTIVE
4: Queens                   ACTIVE
5: Staten Island            ACTIVE
Please select an option number to toggle. Type 'Exit' to return to menu.4
The following labels are in the dataset:
1: Bronx                    ACTIVE
2: Brooklyn                 ACTIVE
3: Manhattan                INACTIVE
4: Queens                   INACTIVE
5: Staten Island            ACTIVE
Please select an option number to toggle. Type 'Exit' to return to menu.Exit
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

What is your choice? 5

The location data matches the following criteria:
Brooklyn
Staten Island
Bronx
                         Minimum             Maximum             Average                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
Entire home/apt          $ 0.00              $ 176.35            $ 10000.00          
Private room             $ 0.00              $ 75.68             $ 7500.00           
Shared room              $ 0.00              $ 51.81             $ 800.00            

What is your choice? 
"""
