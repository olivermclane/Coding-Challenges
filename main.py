import csv
"""
This script allows user to query information about a particular county and city within Montana.
@author Oliver McLane 
@date 02/01/2024
"""


def read_csv(file_extension) -> {}:
    data_dict = {}  # Storage dictionary for prefix's

    with open(file_extension, 'r') as file:  # Opening file in python
        csv_reader = csv.DictReader(file)  # Reading file in python

        for row in csv_reader:  # Reading row in csv into dictionary
            prefix = row['License Plate Prefix']
            data_dict[prefix] = dict(row)

    return data_dict  # Returning dictionary


def main():
    data = read_csv('MontanaCounties.csv')  # Pulling data into via csv method

    querying = True
    while querying:  # Starting query loop
        query = input(
            "Welcome to license plate query service: Please enter your county number(Quit by typing Q or q): ")  # Requesting license plate prefix
        if query.upper() == 'Q':  # Checking user doesn't want to quit
            print("Thank you for using license plate service.")
            querying = False
        else:
            while query not in data.keys():  # If key doesn't exist in key request valid input
                query = input("Please enter a valid county number: ")

            display_format = input(
                "How would you like to view your license plate information? Type 1 for county, 2 for city, and 3 for "
                "Both: ")  # Request Style of print they would like for data

            while display_format not in ["1", "2", "3"]:
                print("Invalid input. Please enter 1, 2, or 3.")
                display_format = input(
                    "How would you like to view your license plate information? Type 1 for county, 2 for city, and 3 for Both: ")

            if display_format == "1":
                print(f"The license prefix: {query}, belongs to {data[query]['County']} county.")
            elif display_format == "2":
                print(f"The license prefix: {query}, belongs to {data[query]['County Seat']}, MT.")
            elif display_format == "3":
                print(
                    f"The license prefix: {query}, belongs to {data[query]['County Seat']},MT of {data[query]['County']} county.")



if __name__ == '__main__':
    main()
