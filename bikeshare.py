import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = list(CITY_DATA.keys())
    city = ''
    while city not in cities:
        city = input("Enter name of the city. You can explore data from Chicago, New York City or Washington.\n").lower()
        if city not in cities:
            print("There is not valid name of the city. \nTry: Chicago, New York City or Washington.\n")



    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = ''
    while month not in months:
        month = input("Enter name of month to filter by, or 'all' to apply no month filter.\n").lower()
        if month not in months:
            print("There is not valid name of month. \nTry: all, january, february, ... , june ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "All"]
    day = ''
    while day not in days:
        day = input("Enter name of the day of week to filter by, or 'all' to apply no day filter.\n").title()
        if day not in days:
            print("There is not valid name of the day of week. \nTry: all, Monday, Tuesday, ... Sunday ")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # loading data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # converting the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extracting month and day of week from Start Time to create new columns
    df['month'] =  df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filtering by month if applicable
    if month != 'all':
        # using the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filtering by month to create the new dataframe
        df = df[df['month'] == month]
    # filtering by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most popular month is: ", popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day of week is: ", popular_day)

    # display the most common start hour
    # extracting hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular hour is: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print ("The most popular start station is: ",popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print ("The most popular end station is: ",popular_end)

    # display most frequent combination of start station and end station trip
    popular_start_end = df['Start Station'] + df['End Station']
    print ("The most frequent combination of start station and end station trip is: ", popular_start_end.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['duration'] = df['End Time'] - df['Start Time']
    print("Total travel time is: ", df['duration'].sum())

    # display mean travel time
    print("Mean travel time is: ", df['duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User types: \n", user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print("User gender: \n", gender)
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_year = df['Birth Year']
        print("The earliest year of birth is: ", birth_year.min())
        print("The most recent year of birth is: ", birth_year.max())
        print("The most common year of birth is: ", birth_year.mode()[0])
    else:
        print('Birth stats cannot be calculated because Birth Year does not appear in the dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # Choosing dataset
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Showing raw data on user request
        row = 0
        while True:
            raw_data = input('Would you like to see 5 rows of data? yes/no\n').lower()
            if raw_data != 'yes':
                break
            elif row >= len(df):
                break
            print(df.iloc[row:row+5])
            row += 5

        # Showing descriptive statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Restart option
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
