""" Copyright © 2018 ambarsingh95 (Ambar Singh) """

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



def yes_no_input():
    """This function is used to take a yes or no input, it asks user to enter
    yes or no but also accepts y, yup, yeah, n, nope in all cases and returns
    true or false accondingly"""

    print ('\nPlease enter yes or no.\n')
    take= (input('>>')).lower()
    while True:
        if take=='yes' or take=='y' or take=='yeah' or take=='yup':
            print ('')
            return True
            break
        elif take=='no' or take=='n' or take=='nope':
            print ('')
            return False
            break
        else:
            print ('Invalid input. Please enter yes or no. ')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) hour - hour of the day to filter by, or "all" to apply no hour filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('*'*40)
    print('')
    while True:
    # get user input for city (chicago, new york city, washington). Takes input in all cases
        while True:
            city = input(''.join(["Please choose the name of the city that ",
            "you'd like to explore data for (your options are Chicago, ",
            "New York City, Washington): \n"]))
            city = city.title()
            if (city == 'Chicago' or city == 'New York City' or
            city == 'Washington'):
                print ("\n ")
                break
                #city=input
            print ("\nPlease input a valid city from Chicago, New York City",
            "or Washington only.\n")

        #Check if user wants to filter data
        print ("Would you like to filter the data based on the following",
        "parameters (please enter yes or no otherwise your responses will be",
        "ignored):-\n")

        filter_list=[]       #initiating empty list
        filter_display_list=['Month', 'Day', 'Hour']
        def filter(which):
            """Local function takes in a string that is displayed to the user
            followed by ': ' and asks for yes/no input to check which parameters
            are to be filtered and appends a boolean to filter_list corresponding
            to the responses/input"""
            # take input and append true/false accordingly
            take_in= (input(which + ": ")).lower()
            if take_in =='yes':
                filter_list.append(True)
            else:
                filter_list.append(False)

        # run filter function for month, day, hour
        for i in filter_display_list:
            filter(i)
        print ("\n")

        """check the filters that need to be placed"""
        #list of months as a list variable for referencing/indexing
        months = ['January', 'February', 'March', 'April', 'May', 'June',]
        # get user input for month (all, january, february, ... , june)
        if filter_list[0]:
            while True:
                month = input(''.join(["To filter your data by month, please ",
                "enter the name of the month from January to June. Otherwise ",
                "enter ALL to explore data for all avalaible months: \n"]))
                month = month.title()
                if (month in months) or month=='All':
                    print ("\n")
                    break
                print ('Please input a valid month or the word ALL.\n')
        else:
            month ="All"

        # get user input for day of week (all, monday, tuesday, ... sunday)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday', 'Sunday']
        if filter_list[1]:
            while True:
                day = input(''.join(["To filter your data by day of the week, ",
                "please enter the name of the day. Otherwise enter ALL to ",
                "explore data for all days: \n"]))
                day = day.title()
                if (day in days) or day=='All':
                    print ("\n")
                    break
                print ('Please input a valid day or the word ALL.\n')
        else:
            day='All'

        # get user input for hour/all
        if filter_list[2]:
            while True:
                hour = input(''.join(["To filter your data by hour of the day,",
                " please enter the hour as an integer according to 24hr format",
                ". Otherwise enter ALL to explore data for all hours: \n"]))
                try:
                    if int(hour)<=24 or day=='All':
                        print ("\n")
                        break
                except ValueError:      #incase user inputs other than a Number
                    print ("Please print a valid response")
                    pass
                print ('Please input a valid hour or the word ALL.\n')
        else:
            hour='All'

        # confirming the inputs for filter
        print ("Here is your selection",
        "\nCity: {} \nMonth: {} \nDay of the week: {} ".format(city, month, day),
        "\nHour: {}".format(hour))
        print ("\nIf you are satisfied with your input",
        "please enter yes otherwise enter no to select again: ")
        confirm= yes_no_input()
        if confirm:
            break
        elif confirm:
            pass
    print('-'*40)
    return city, month, day, hour


def load_data(city,month,day, hour):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df= pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month']= df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday
    df['Hour']= df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'All':
    #use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)+1       # +1 because january=1
        # filter by month to create the new dataframe
        df = df[df['Month']==month]


    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday',
        'Sunday']
        day= days.index(day) # no +1 because Monday=0
        df = df[df['Day']==day]

    # filter by starting trip hour
    if hour != "All":
         df = df[df['Hour']==int(hour)]

    return df

def time_stats(df):
    """
    This function prints information on the time statistics corresponding to the
    start time of the filtered trips in the dataset

    Args:
        (DataFrame) df- filtered dataset that is being analyzed
    Returns:
        Nothing
        But function prints most busiest month, day, and hour of the day


    """
    print('\nCalculating Time Stats...\n')
    start_time = time.time()

    #list of months for indexing
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday',
    'Sunday']
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    #calculate modes for month, day, hour
    calc_modes=df[['Month', 'Day', 'Hour']].mode()

    #most common month
    month_comm=(calc_modes['Month']).iloc[0]-1
    month_comm= months[month_comm]
    print ('Most common month is: ' +str(month_comm) +'\n')


    #most common day
    day_comm=(calc_modes['Day']).iloc[0]
    day_comm=days[day_comm]
    print ('Most common day is: ' + day_comm+ '\n')

    #most common hour in 12hr time
    hour_comm=(calc_modes['Hour']).iloc[0]
    if hour_comm<12:
        hour_comm = str(hour_comm)+ ' AM'
    else:
        hour_comm = str(hour_comm-12)+ ' PM'

    print ('Most common hour is: ' + hour_comm + '\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # printing the graphs
    print ('\nWould you like view time stats in a graph?')
    graph=yes_no_input()
    def graph_it_time(col_name, ord):
        col_count  = df[col_name].value_counts()
        plt.figure(figsize=(10,8))
        if col_name!='Hour':
            sns.barplot([ord[i-((col_name=='Month'))] for i in col_count.index],
             col_count.values, alpha=0.75, order=ord )
        else:
            sns.barplot(col_count.index, col_count.values, alpha=0.75, )
        plt.ylabel('Number of Trips', fontsize=12)
        plt.xlabel(col_name, fontsize=12)
        plt.title('Time Stats by the {}'.format(col_name))
        plt.show()
    if graph:
        for i,o in [('Month',months),('Day', days),('Hour',list(range(1,25)))]:
            graph_it_time(i,o)
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #creating a column for trip start and end station together
    df['Start to End'] = df['Start Station'].map(str) + ' TO ' \
    + df['End Station'].map(str)

    #calculate modes for needed columns
    calc_modes=df[['Start Station', 'End Station', 'Start to End']].mode()

    # display most commonly used Start station
    start_comm= (calc_modes['Start Station']).iloc[0]
    start_count= (df['Start Station']==start_comm).sum()
    print (start_comm +' station is the most common start station with count of '
    +str(start_count))

    # display most commonly used end station
    end_comm= calc_modes['End Station'].iloc[0]
    end_count= (df['End Station']==end_comm).sum()
    print (end_comm+ ' station is the most common end station with a count of '
    +str(end_count))
    # display most frequent combination of start station and end station trip
    start_end_comm= calc_modes['Start to End'].iloc[0]
    start_end_count= (df['Start to End']==start_end_comm).sum()
    print (start_end_comm+ ' is the most common trip with a count of '
    +str(start_end_count))
    #calculating time taken to execute
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    print ('\nWould you like view station stats in a graph?')
    graph=yes_no_input()
    def graph_it_station(col_name):
        col_count  = df[col_name].value_counts()
        col_count = col_count[:10,]
        plt.figure(figsize=(10,8))
        if col_name=='Start to End':
            xlab= ['\n TO'.join(i.split('TO')) for i in col_count.index]
            sns.barplot(xlab, col_count.values, alpha=0.75)
        else:
            sns.barplot(col_count.index, col_count.values, alpha=0.75)
        plt.ylabel('Number of Trips', fontsize=12)
        plt.xlabel(col_name, fontsize=12)
        plt.xticks(fontsize=8, rotation=90)
        plt.title('Station Stats by : {}'.format(col_name))
        plt.tight_layout()
        plt.show()
    if graph:
        for i in ['Start Station', 'End Station', 'Start to End']:
            graph_it_station(i)
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    avg_trav_time= df['Trip Duration'].mean()
    print ('The average trip duration is {} seconds.'.format(avg_trav_time))
    # display mean travel time
    tot_trav_time= df['Trip Duration'].sum()
    print ('The total trip duration is {} seconds.'.format(tot_trav_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, limited):
    """Displays statistics on bikeshare users. Limited is an added variable to
    check if the data belongs to Washington, where we do not have gender and
    birth year data"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print (df['User Type'].value_counts())
    print ("\n")
    (df['User Type'].value_counts()).plot(title= 'User Type Distribution', kind='pie')
    plt.show()
    if not limited:
    # Display counts of gender
        print (df['Gender'].value_counts())
        print ("\n")
        (df['Gender'].value_counts()).plot(title= 'Gender Distribution', kind='pie')
        plt.show()
        # Display earliest, most recent, and most common year of birth
        print ('Earliest year of birth is: '+ str(int(df['Birth Year'].min())))
        print ('Most recent year of birth is: '+ str(int(df['Birth Year'].max())))
        print ('Most common year of birth is: '
        + str(int(df['Birth Year'].mode().iloc[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw(df):
    print ('Would you like to see the raw data for your selection?\n')
    see=yes_no_input()
    if see:
        print (df.iloc[:,:-3])
    else:
        print ("If you wish to view the first few rows of the raw data, please",
        "enter the number of rows you'd like to view (input no if you want to",
        "skip to the next step):")
        number_of_rows= input().lower()
        if number_of_rows=="no":
            return
        else:
            try:
                number_of_rows= int(number_of_rows)
                print (df.iloc[:,:-3].head(number_of_rows))
            except:
                print ('Invalid response. Skipping to next step.')
    print('-'*40)


def main():
    while True:
        city, month, day, hour = get_filters()
        df = load_data(city, month, day, hour)

        #print (df.head())
        if not df.empty:
            view_raw(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            if city == 'Washington':
                user_stats(df, limited=1)
            else:
                user_stats(df, limited=0)
        else:
            print ("The selection returned no values please try again.")

        print('\nWould you like to restart? Enter yes or no.\n')
        restart= yes_no_input()
        if not restart:
            break


if __name__ == "__main__":
	main()
