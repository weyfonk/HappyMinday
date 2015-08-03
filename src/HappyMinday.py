#!/usr/bin/env python

'''
Created on 17.03.2015

@author: tan
'''
import argparse
import calendar
import os
import sys
import traceback
from datetime import date
from BirthdayTree import BirthdayTree

QUIT_KEY = 'Q'

def main():
    
    parser = argparse.ArgumentParser(description='Manages a birthday collection')
    parser.add_argument('-a', '--add', help='Add an entry', action='store_true', required=False)
    parser.add_argument('-c', '--count', help='Count the entries', action='store_true', required=False)
    parser.add_argument('-d', '--day', help='Display entries for next X days', type=int, required=False)
    parser.add_argument('-i', '--init', help='Insert many entries', action='store_true', required=False)
    parser.add_argument('-m', '--month', help='Display entries for next X months', type=int, required=False)
    parser.add_argument('-r', '--remove', help='Remove an entry', required=False)
    parser.add_argument('-s', '--search', help='Search entries', required=False)
    parser.add_argument('-o', '--sort', help='Sort entries', action='store_true', required=False)
    parser.add_argument('-u', '--update', help='Update an entry', required=False)
    
    args = parser.parse_args()
    
    
    fileName = 'birthdays.xml'
    path = os.path.abspath(fileName)
    
    bt = BirthdayTree(path)

    #idea:  search function (by month, by day, by name, by year)
    try: 
        if args.init:
            print('----- Welcome to HappyMinday!----- \n')
            insert_entries(bt, True)
            
        else:
            if args.add:
                result = insert_entries(bt, False)
                
                if(result):
                    print('Birthday added')

            if args.search:
                name = args.search
                bt.search_name_entry(name, False)
                
            if (args.month is not None and args.month >= 0) \
             or (args.day is not None and args.day >= 0):
                    searchByMonth = args.month
                    interval = args.month if args.month else args.day
                    bt.search_next_entries(searchByMonth, interval)
                
            if args.remove:
                name = args.remove
                
                bt.delete_entry(name)
                
            if args.count:
                bt.count_entries()

            if args.sort:
                bt.sort_entries()
                
            if args.update:
                oldName = args.update
                newName = input('Choose a new name for {0}: \n'.format(oldName))
                bt.update_entry(oldName, newName)
                
            if bt._indent_after_treatment:
                bt.indent(bt._root, 0)
    except KeyboardInterrupt:
        print('\n Operation interrupted by the user. See you soon!')
    except:
        print('An error occurred: \n {0}'.format(traceback.format_exc()))


def insert_entries(birthdayTree, isLoop):
    """
    Lets the user insert as many entries as wanted
    """
    if isLoop:
        print('Welcome to init mode.')
        print('You will be able to add as many birthdays as you wish.')
        print('Press {0} when you are done'.format(QUIT_KEY))
    
    if not isLoop:
        result = add_entry(birthdayTree)
    else:
        while True:
            print('New birthday: ')
            result = add_entry(birthdayTree)
    return result
            
        
def add_entry(birthdayTree):
    """
    Adds an entry
    """
    name = validate_input('\t-Name: ')
    year = validate_input('\t-Year of birth: ')
    month = validate_input('\t-Month of birth: ')
    day = validate_input('\t-Day of birth: ')
    
    if validate_date(month, day, year):
        return birthdayTree.add_entry(name, month, day, year)
            

def validate_date(month, day, year):
    """ 
    Checks a date validity based on its day, month and year
    Returns true if the date is valid, false otherwise
    """
    if not month.isdigit() or not day.isdigit() or not year.isdigit():
        return False
    
    monthVal = int(month)
    dayVal = int(day)
    
    daysInMonth = calendar.monthrange(date.today().year, monthVal)[1] 
    
    isDayOk = dayVal >= 1 and dayVal <= daysInMonth
    isMonthOk = monthVal >= 1 and monthVal <= 12
    
    isDateOk = isDayOk and isMonthOk
    
    if not isDateOk:
        print('Error: incorrect date')
    
    return isDateOk


def validate_input(msg):
    """ 
    Displays a message to the user, checks whether the user chose to quit the program.
    If no quit is needed, returns user input
    """
    result = input(msg)
    if result.upper() == QUIT_KEY:
        print('Quitting.')
        quit()
    return result
     

if __name__ == '__main__':
    pass



main()
