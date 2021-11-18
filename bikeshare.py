import time
import pandas as pd

city_data = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    cities = ['chicago', 'new york city', 'washington']
    city = input("Would you like to retrieve bikeshare information for Chicago, New York City or Washington?: ").lower().strip()
    # keep trying is format is not as desired
    try:
        while city not in cities:
            city = input("Please choose between Chicago, New York City, Washington or all: ").lower().strip()
    except Exception as e:
        print("Exception occurred: {}".format(e))

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input("Would you like to retrieve bikeshare information for january, february, march, april, may, june or all?: ").lower().strip()
    # keep trying is format is not as desired
    try:
        while month not in months:
            month = input("Please choose between january, february, march, april, may, june or all: ").lower().strip()
    except Exception as e:
        print("Exception occurred: {}".format(e))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = input("For which day of the week would you like to retrieve bikeshare information?: ").lower().strip()
    # keep trying is format is not as desired
    try:
        while day not in days:
            day = input("Please choose between monday, tuesday, wednesday, thursday, friday, saturday, sunday or all: ").lower().strip()
    except Exception as e:
        print("Exception occurred: {}".format(e))

    print("Selected city: {} \nSelected month: {} \nSelected day: {}".format(city, month, day))
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
    print(f"Imported csv file: {city_data[city]}")
    df = pd.read_csv(f"data/{city_data[city]}")
    df = df.assign(
        month=pd.to_datetime(df['Start Time']).dt.strftime('%B').str.lower(),
        day=pd.to_datetime(df['Start Time']).dt.strftime('%A').str.lower(),
        hour=pd.to_datetime(df['Start Time']).dt.strftime('%H'),
        city=city
    )
    if month == 'all' and day == 'all':
        df = df
    elif month == 'all' and day != 'all':
        df = df[df['day'] == day]
    elif month != 'all' and day == 'all':
        df = df[df['month'] == month]
    else:
        df = df[(df['month'] == month) & (df['day'] == day)]
    print(df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(f"The most common month is {df['month'].mode().values[0]}")

    # display the most common day of week
    print(f"The most common day is {df['day'].mode().values[0]}")

    # display the most common start hour
    print(f"The most common hour is {df['hour'].mode().values[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"The most common used start station is {df['Start Station'].mode().values[0]}")

    # display most commonly used end station
    print(f"The most common used end station is {df['End Station'].mode().values[0]}")

    # display most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + ' ' + df['End Station']
    print(f"The most common combination of start and end station is {df['Start and End Station'].mode().values[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f"The total travel time is {df['Trip Duration'].sum()}")

    # display mean travel time
    print(f"The average travel time is {df['Trip Duration'].mean()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"The user type distribution is as follows: \n{df['User Type'].value_counts()}")

    # Display counts of gender
    if any(df['city'].isin(['chicago', 'new york city'])):
        print(f"The gender distribution is as follows: \n{df['Gender'].value_counts()}")
        # Display earliest, most recent, and most common year of birth
        print(f"The earliest year of birth is {int(df['Birth Year'].min())}")
        print(f"The most recent year of birth is {int(df['Birth Year'].max())}")
        print(f"The most common year of birth is {int(df['Birth Year'].mode().values[0])}")
    else:
        print(f"No gender/age information available!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(city):
    """
    Asks user for raw data need

    Args:
    (str) city - selected country file
    Returns:
    str - Text containing raw data or message that no data is requested
    """
    first_decision = input("Would you like to view some raw data? ").lower().strip()
    while first_decision != 'yes' and first_decision != 'no':
        first_decision = input("Please choose either 'Yes' or 'No': ").lower().strip()

    more_data = "no"

    with open(f"data/{city_data[city]}") as f:
        lines = f.readlines()
        len_lines = len(lines)
        idx = 0
        while (first_decision == 'yes' or more_data == 'yes') and idx < len_lines:
            print(len(lines))
            for line in lines[idx:idx+5]:
                print(line)
            first_decision = 'no'
            more_data = input("Would you like to view some more raw data? ").lower().strip()
            while more_data != 'yes' and more_data != 'no':
                more_data = input("Please choose either 'Yes' or 'No': ").lower().strip()
            idx += 5

    print(f"\n Okay we will stop printing now!")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
