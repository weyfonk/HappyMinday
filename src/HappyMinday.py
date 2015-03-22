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

def main(argv):
    path = os.path.abspath('birthdays.xml')
    
    bt = BirthdayTree(path)

    #idea: add parameters like timespan (ex. next x day(s)/week(s)/month(s)) for reminder
    # + search function (by month, by day, by name, by year)
    
    if len(argv) == 0:
        
        if(bt.is_empty()):
            print('Error: no data in {0}!'.format(path))
            return
        
        bt.show_next_month_data()
        
        
    else:
        if argv[0].upper() == '-A':
            
            if(len(argv) != 5
               or not validate_date(argv[2], argv[3], argv[4])):
                print('Error: incorrect command syntax')
                return
            
            person = argv[1]
            month = int(argv[2])
            day = int(argv[3])
            year = int(argv[4])
            
            bt.add_entry(person, month, day, year)
            
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
            

def validate_date(month, day, year):
    if not month.isdigit() or not day.isdigit() or not year.isdigit():
        return False
    
    monthVal = int(month)
    dayVal = int(day)
    
    daysInMonth = calendar.monthrange(date.today().year, monthVal)[1] 
    
    isDayOk = dayVal >= 1 and dayVal <= daysInMonth
    isMonthOk = monthVal >= 1 and monthVal <= 12
    
    return isDayOk and isMonthOk


     

if __name__ == '__main__':
    pass



main(sys.argv[1:])
