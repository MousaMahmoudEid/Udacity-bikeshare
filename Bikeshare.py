import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#List and dicts to make it easier to work with pandas
list_of_cities = ["chicago", "new york city", "washington"]
dict_of_months = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "all": 7}
dict_of_days = {"saturday": 0, "sunday": 1, "monday": 2, "tuseday":3, "wednesday": 4, "thusday": 5, "friday": 6, "all" : 7}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please choose one of these cities : chicago, new york city or washington\n").lower()
    while city not in list_of_cities:
        city = input("Invalid city entery! please choose either chicago, new york city or washington\n").lower()
    # TO DO: get user input for month (all, january, february, ... , june)

    month = input("choose between (all, january, february, ... , june)\n").lower()
    while month not in dict_of_months.keys():
        month = input("Invalid month entery! please select from the availible choices\n").lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("choose between (all, monday, tuesday, ... sunday)\n").lower()
    while day not in dict_of_days.keys():
        day = input("Invalid day entery! please select from the availible choices\n").lower()   

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
    # load data file into a dataframe
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    #Added hours column
    df['hour'] = df['Start Time'].dt.hour
    #Added start and end column
    df['trip route'] = "from " + df['Start Station']+ " to " + df['End Station']
    
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ["saturday", "sunday", "monday", "tuseday", "wednesday","thusday","friday"]
        day = days.index(day)
        df = df[df['day_of_week'] == day]

    
    return df

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
 
#Through out the code we used try/except to handle empty dataframes encountered from user filtering

    try:
        # TO DO: display the most common month
        most_common_month = df['month'].mode()[0]
        for name_of_month, number_of_month in dict_of_months.items():
            if number_of_month == most_common_month:
                print("Most common month is {}".format(name_of_month))
                
        # TO DO: display the most common day of week
        most_common_day = df['day_of_week'].mode()[0]
        for name_of_day, number_of_day in dict_of_days.items():
            if number_of_day == most_common_day:
                print("Most common day of week is {}".format(name_of_day))  
                
        # TO DO: display the most common start hour
        most_common_start_hour = df['hour'].mode()[0]
        #Added if/else statment to convert hours to AM/PM 
        if most_common_start_hour > 12: 
            most_common_start_hour -= 12
            print("Most common start hour is {} PM".format(most_common_start_hour))
        else:
            print("Most common start hour is {} AM".format(most_common_start_hour))
            
    except IndexError:
        print("The current data enteries for the filters applied have no repeated data to determind common values required")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Through out the code we used try/except to handle empty dataframes encountered from user filtering
    
    try:
        # TO DO: display most commonly used start station
        print("The most common start station is {} ".format(df['Start Station'].mode()[0]))

        # TO DO: display most commonly used end station
        print("The most common end station is {} ".format(df['End Station'].mode()[0]))

        # TO DO: display most frequent combination of start station and end station trip
        print("The most frequent combination of start station and end station trip is {} ".format(df['trip route'].mode()[0]))
    except IndexError:
        print("The current data enteries for the filters applied have no repeated data to determind common values required")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def time_conversion(time):
    """Takes time in seconds and formats it to give days, hours, mins and secs."""
    time_days = time // (24*60*60)
    time %= (24*60*60)
    time_hours = time // (60*60)
    time %= (60*60)
    time_mins = time // 60
    time %= 60
    time_secs = time
    return int(time_days), int(time_hours), int(time_mins), int(time_secs)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    #Through out the code we used try/except to handle empty dataframes encountered from user filtering

    try:
        # TO DO: display total travel time
        days, hours, mins, secs = time_conversion(df['Trip Duration'].sum()) 

        print("The total travel time is {} days {}:{}:{}".format(days,hours,mins,secs))

        # TO DO: display mean travel time
        days, hours, mins, secs = time_conversion(df['Trip Duration'].mean())

        print("The mean travel time is {} days {}:{}:{}".format(days,hours,mins,secs))
    except ValueError:
        print("The current data enteries for the filters applied have no data to determind values requested")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Through out the code we used try/except to handle empty dataframes encountered from user filtering

    try:
        # TO DO: Display counts of user types
        #reformat and print user statistics
        user_status = df['User Type'].value_counts()
        for user_type , user_count in user_status.items():
            print("Recorded {} user(s) of type {}".format(user_count,user_type))
           
        #Since washington have no gender or birth dates we need to make sure to filter it out
        if city != 'washington':
        # TO DO: Display counts of gender
            gender_status = df['Gender'].value_counts()
            #reformat and print gender statistics
            for gender_type , gender_count in gender_status.items():
                print("Recorded {} user(s) of gender {}".format(gender_count,gender_type))
                
        # TO DO: Display earliest, most recent, and most common year of birth
            earliest_year = int(df['Birth Year'].min())
            most_recent = int(df['Birth Year'].max())
            most_common_birth_year = int(df['Birth Year'].mode()[0])
            print("The earliest birth year is {}".format(earliest_year))
            print("The most recent birth year is {}".format(most_recent))
            print("The most common birth year is {}".format(most_common_birth_year))
        else:
            print("There are no gender or birth year data for washington city")

    except IndexError:
        print("The current data enteries for the filters applied have no repeated data to determind common values required")
    except ValueError:
        print("The current data enteries for the filters applied have no data to determind values requested")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    """prints data from the dataframe or the whole dataframe"""
    #This function is for debugging purpose mostly
    
    #Checking data in the first 5 rows
    print_head = input("Would you like to print a sample of the data? (yes or no)\n").lower()
    if print_head == "yes":
        print(df.head())
        
    #Checking data in the whole dataframe
    print_df = input("Would you like to review the dataframe after filtering? (yes or no)\n").lower() 
    if print_df == "yes":
        print(df)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        
        print_raw_data(df)
        
        restart = input('\nWould you like to restart? (yes or no).\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
