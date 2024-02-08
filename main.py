import csv

"""
This script allows a user to query information about a particular county and city within Montana.

@author Oliver McLane
@date 02/07/2024
"""


def write_csv(csv_file_name, data):
    """Writes data to the specified CSV file using the csv module."""
    with open(csv_file_name, 'w', newline='') as csvfile:  # Open the CSV file in write mode
        fieldnames = data[0].keys()  # Get the field names from the first row of data
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # Create a writer object
        writer.writeheader()  # Write the header row
        writer.writerows(data)  # Write the data rows


def read_csv(file_extension) -> {}:
    """Reads data from a CSV file and returns it as a dictionary."""
    data_dict = {}  # Create an empty dictionary to store the data

    with open(file_extension, 'r') as file:  # Open the CSV file in read mode
        csv_reader = csv.DictReader(file)  # Create a reader object

        for row in csv_reader:  # Iterate through each row in the CSV file
            prefix = row['License Plate Prefix']  # Get the license plate prefix from the row
            data_dict[prefix] = dict(row)  # Add the row data to the dictionary, using the prefix as the key
    return data_dict  # Return the dictionary containing the data


def city_to_county(data):
    city_to_county = {}  # Create city to county dictionary
    for row in data.values():  # Loop through data in csv
        city = row['County Seat']  # Create row for County Seat
        county = row['County']  # Create row for County
        prefix = row['License Plate Prefix']  # Create Row for prefix
        city_to_county[city] = county, prefix  # Assign values for dictionary

    return city_to_county


def query_type():
    """Prompts the user to choose between license plate or city lookup."""
    while True:
        query_type = input(
            "Choose between options License plate or City lookup: (C for city and L for License prefix) ").upper()
        if query_type in ['L', 'C']:
            return query_type.lower()  # Return the lowercase version of the choice
        else:
            print("Invalid input. Please enter 'L' or 'C'.")


def query_license(data, prefix):
    """Queries information based on a license plate prefix."""
    if prefix in data.keys():  # Check if the prefix exists in the data
        return data[prefix]['County Seat'], data[prefix]['County']  # Return the county seat and county
    else:
        print(f"License Plate prefix {prefix} not found. Provide us:")
        city = input("City name: ")
        county = input("County name: ")
        data[prefix] = {'County Seat': city, 'County': county,
                        'License Plate Prefix': prefix}  # Add the new information to the data dictionary
        write_csv('MontanaCounties.csv', list(data.values()))  # Update the CSV file
        return city, county


def query_city(data, city_to_county, city):
    """Queries information based on a city name."""
    if city.capitalize() in city_to_county:
        return city_to_county[city.capitalize()]
    else:
        print(f"City '{city}' not found. Please provide:")
        county = input("County name: ")
        prefix = input("License plate prefix (optional): ")
        # Add the new information to the data dictionary and city-to-county mapping
        new_data = {'County Seat': city, 'County': county, 'License Plate Prefix': prefix}
        data[city] = new_data
        city_to_county[city] = county
        write_csv('MontanaCounties.csv', list(data.values()))  # Update the CSV file
        return county, prefix


def main():
    """Main function that runs the query loop."""
    querying = True
    while querying:  # Start the query loop
        data = read_csv('MontanaCounties.csv')  # Read the data from the CSV file
        city_to_county_var = city_to_county(data)

        user_query_type = query_type()  # Get the user's query type

        if user_query_type == 'l':  # If the user chose license plate lookup
            prefix = input("Enter license plate prefix: (Type Q to quit) ")
            if prefix.lower() == "q":
                querying = False  # Exit the loop if the user enters 'q'
            else:
                city, county = query_license(data, prefix)
                print(
                    f"The license plate prefix {prefix} belongs to the city of {city}, Montana, located in {county} county.")
        elif user_query_type == 'c':  # If the user chose city lookup
            city = input("Enter city name: (Type Q to quit) ")
            if city.lower() == "q":
                querying = False  # Exit the loop if the user enters 'q'
            else:
                county, prefix = query_city(data, city_to_county_var, city)
                print(f"The city {city}, Montana belongs to {county}, with a prefix of {prefix}")


if __name__ == '__main__':
    main()
