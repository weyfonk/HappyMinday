'''
Created on 21.03.2015

@author: tan
'''

from datetime import date, timedelta
from lxml import etree
import calendar
import os

class BirthdayTree(object):
    '''
    classdocs
    '''


    def __init__(self, path):
        '''
        Constructor
        '''
        self._path = path
        
        if not os.path.exists(path):
            print('No existing file at {0}. Creating file...'.format(path))
            self.create_new_file()
            print('New file created at {0}'.format(path))
        
        self._data = etree.parse(path) #minidom.parse(path)
        self._root = self._data.getroot()

        self._monthNodes = self._root.iter('month')

        
    def add_entry(self, name, month, day, year):

        existingEntry = self.find_by_name(name)
        if existingEntry is not None:
            print('''An entry already exists for {0}. 
Please update the existing name or use a new one'''.format(name))
            return False
        
        day = int(day)
        month = int(month)
        year = int(year)
            
        currentMonthNodes = self._root.findall(".//month/[@index='{0}']".format(month))
        
        if len(currentMonthNodes) == 0:
            indexAfterInsert = -1
#                 print("month not found")
            for child in self._monthNodes:
                childMonth = int(child.get('index'))
                if (childMonth < month and child.getnext() is not None 
                    and int(child.getnext().get('index')) > month):
                    indexAfterInsert = self._root.index(child.getnext())
            
            monthNode = etree.Element('month')
            monthNode.set('index', str(month))
            
            if indexAfterInsert < 0:
                self._root.append(monthNode)
            else:
                self._root.insert(indexAfterInsert, monthNode)
            
        else:
#                 print("month found")
            monthNode = currentMonthNodes[0]
            
        currentDayNodes = monthNode.findall(".//day/[@index='{0}']".format(day))
            
        if len(currentDayNodes) == 0:
            #print("day not found")
            indexAfterInsert = -1
            
            for child in monthNode.findall('day'):
                childDay = int(child.get('index'))
                if (childDay < day and child.getnext() is not None
                    and int(child.getnext().get('index')) > day):
                    indexAfterInsert = list(monthNode).index(child.getnext())
            
            #print(indexAfterInsert)
            
            dayNode = etree.Element('day')
            dayNode.set('index', str(day))

            if indexAfterInsert < 0:
                monthNode.append(dayNode)
            else:
                monthNode.insert(indexAfterInsert, dayNode)
        else:
            print("day found")    
            dayNode = currentDayNodes[0]
            
        newBirthday = etree.SubElement(dayNode, 'person')
        newBirthday.set('name', name)
        newBirthday.set('year', str(year))
            
        self.save_file()
        self.indent(self._root, 0)
        self.search_name_entry(name)
        return True                
    
    
    def count_entries(self):
        result = len(self._root.findall('.//person'))
        print('{0} birthdays in the database.'.format(result))
        
    def create_new_file(self):
        with open(self._path, mode = 'w', encoding = 'utf-8') as newFile:
            root = etree.Element('birthdays')
            newTree = etree.ElementTree(root)
            
            for month in range(1,13):
                monthNode = etree.SubElement(root, 'month')
                monthNode.set('index', str(month))
            
            newContents = etree.tostring(newTree)
            print(newContents)
            
            newTree.write(self._path)
            #self.save_file()    
        
    
    def delete_entry(self, name):
        nameNode = self._root.find(".//person[@name='{0}']".format(name))
        
        if nameNode is None:
            print('Name not found: {0}'.format(name))
            return
        
        parent = nameNode.getparent()
        
        parent.remove(nameNode)
        self.save_file()
        
        print('Birthday deleted for {0}'.format(name))
        
    
    def search_name_entry(self, name):
        nameNode = self.find_by_name(name)
        if nameNode is None:
            print('Name not found: {0}'.format(name))
            return
        
        year = nameNode.get('year')
        month = int(nameNode.getparent().getparent().get('index'))
        monthStr = calendar.month_name[month]
        day = nameNode.getparent().get('index')
        age = date.today().year - int(year)
        # if birthday was earlier this year, show next year's age
        if(month < date.today().month 
           or (month == date.today().month and int(day) < date.today().day)):
            age = age + 1
        
        print('Next birthday for {0}: {1} {2} ({3})'.format(
			name, 
			monthStr,
            day,
			age
			))
    
    def search_next_entries(self, searchByMonth, interval, currentDate=date.today()):
#         currentMonth = 12
        lastMonth = (currentDate.month + interval) % 12
        
        currentMonth = currentDate.month
        nbDaysInCurrentMonth = calendar.monthrange(date.today().year, currentMonth)[1]
        remainingDaysInMonth = nbDaysInCurrentMonth - currentDate.day
        
        # search entries for current month and the next ones
        # depends on current day
        # ex: if called on Oct. 12 for 2 months, covers Oct 12 to Dec 12
        if(searchByMonth):
            daysInterval = remainingDaysInMonth
            for element in self._monthNodes:
                localMonth = int(element.get('index'))
                if( (lastMonth > currentMonth 
                     and currentMonth < localMonth < lastMonth)
                   or (lastMonth < currentMonth
                     and(localMonth > currentMonth
                      or localMonth < lastMonth))):
                          nbDaysInLocalMonth = calendar.monthrange(date.today().year, localMonth)[1]
                          daysInterval = daysInterval + nbDaysInLocalMonth
                          
                          
                if localMonth == lastMonth:
                    daysInterval = daysInterval + currentDate.day
                    
            self.search_next_entries(False, daysInterval, currentDate)

        # search for next days
        # relies on the monthly version in case the timespan covers more than a month
        else:
            savedInterval = interval
            #~ print('Birthdays between {0} and {1}:'.format(currentDate, currentDate + timedelta(days = savedInterval)))
            
            currentMonthNode = self._root.find(".//month/[@index='{0}']".format(currentMonth))
            print('Birthdays in {0}: '.format(calendar.month_name[currentMonth]))
            for dayNode in currentMonthNode.iter('day'):
                dayIndex = dayNode.get('index')
                if currentDate.day <=  int(dayIndex) <= currentDate.day + interval:
                    for person in dayNode.iter('person'): 
                        print('\t -{0}: {1} ({2})'.format(
                            dayIndex,
                            person.get('name'),
                            date.today().year - int(person.get('year'))
                            )
                        )
            # if interval goes further than current month, add results for following months
            if savedInterval >= remainingDaysInMonth:
                savedInterval = savedInterval - remainingDaysInMonth - 1
                self.search_next_entries(False, savedInterval, currentDate + timedelta(days = remainingDaysInMonth + 1))
    
        
    def show_next_month_data(self):
        self.search_next_entries(True, 1)
    
    
    def update_entry(self, oldName, newName):
        nodeToUpdate = self.find_by_name(oldName)

        if nodeToUpdate is None:
            print('No birthday found for {0} to update'.format(oldName))
            return
        nodeToUpdate.set('name', newName)
        print('Name updated for {0}. New name: {1}'.format(oldName, newName))
        self.save_file()
    
    
    def find_by_name(self, name):
        result = self._root.find(".//person[@name='{0}']".format(name))
        return result
    
    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
                
        if(level == 0):
            self._data.write(self._path)
    
    
    def is_empty(self):
        return len(list(self._root.iter('month'))) == 0
        
    def save_file(self):
        self._data.write(self._path)
            
