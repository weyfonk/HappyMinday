#!/usr/bin/env python

'''
Created on 17.03.2015

@author: tan
'''
import calendar
import os
import sys
# import xml.etree.ElementTree as ET
from datetime import date
from BirthdayTree import BirthdayTree

QUIT_KEY = 'Q'

def main(argv):
    fileName = 'birthdays.xml'
    path = os.path.abspath(fileName)
    
    bt = BirthdayTree(path)

    #idea:  search function (by month, by day, by name, by year)
    
    if len(argv) == 0:
        print('----- Welcome to HappyMinday!----- \n')
        loop_insert_entries(bt)
        
    else:
        if argv[0].upper() == '-A':
            
            if(len(argv) != 5
               or not validate_date(argv[2], argv[3], argv[4])):
                return
            
            person = argv[1]
            month = int(argv[2])
            day = int(argv[3])
            year = int(argv[4])
            
            result = bt.add_entry(person, month, day, year)
            
            if(result):
                print('Birthday added')

        if argv[0].upper() == '-S':
            
            # syntax -S d 5 (5 next days) / -S m 3 (3 next months)
            if argv[1].upper() == 'M':
                searchByMonth = True
            
            if argv[1].upper() == 'D':
                searchByMonth = False
            
            if argv[2].isdigit():
                interval = int(argv[2])
            
            bt.search_next_entries(searchByMonth, interval)
            
        if argv[0].upper() == '-D':
            name = argv[1]
            
            bt.delete_entry(name)
            
        if argv[0].upper() == '-P':
            name = argv[1]
            bt.search_name_entry(name)
            
        if argv[0].upper() == '-C':
            bt.count_entries()
            
        if argv[0].upper() == '-U':
            oldName = argv[1]
            newName = argv[2]
            bt.update_entry(oldName, newName)
            
        bt.indent(bt._root, 0)


def loop_insert_entries(birthdayTree):
    
    userInput = ''
    
    print('Welcome to init mode.')
    print('You will be able to add as many birthdays as you wish.')
    print('Press {0} when you are done'.format(QUIT_KEY))
    
    while True:
        print('New birthday: ')
        name = validate_input('\t-Name: ')
        year = validate_input('\t-Year of birth: ')
        month = validate_input('\t-Month of birth: ')
        day = validate_input('\t-Day of birth: ')
        
        if validate_date(month, day, year):
            birthdayTree.add_entry(name, month, day, year)
            

def validate_date(month, day, year):
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


''' Displays a message to the user, checks whether the user chose to quit the program.
 If no quit is needed, returns user input'''
def validate_input(msg):
    result = input(msg)
    if result.upper() == QUIT_KEY:
        print('Quitting.')
        quit()
    return result
     

if __name__ == '__main__':
    pass



main(sys.argv[1:])
