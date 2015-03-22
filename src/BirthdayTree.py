'''
Created on 21.03.2015

@author: tan
'''

from datetime import date
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
        self._data = etree.parse(path) #minidom.parse(path)
        self._root = self._data.getroot()

        self._monthNodes = self._root.iter('month')

        
    def add_entry(self, name, month, day, year):
        print('month: ', month)
            
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
#                 print(etree.tostring(dayNode, pretty_print = True))

            if indexAfterInsert < 0:
                monthNode.append(dayNode)
            else:
                monthNode.insert(indexAfterInsert, dayNode)
        else:
            print("day found")    
            dayNode = currentDayNodes[0]
#                 print(etree.tostring(dayNode, pretty_print = True))
            
        newBirthday = etree.SubElement(dayNode, 'person')
        newBirthday.set('name', name)
        newBirthday.set('year', str(year))
#             print(etree.tostring(newBirthday, pretty_print = True))
        
#             print(etree.tostring(monthNode, pretty_print = True))
            
#             ET.dump(monthNode)
        self._data.write(self._path)
        self.indent(self._root, 0)                
    
    
    def count_entries(self):
        result = len(self._root.findall('.//person'))
        print('{0} birthdays in the database.'.format(result))
        
    
    def delete_entry(self, name):
        nameNode = self._root.find(".//person[@name='{0}']".format(name))
        
        if nameNode is None:
            print('Name not found: {0}'.format(name))
            return
        
        parent = nameNode.getparent()
        
        parent.remove(nameNode)
        self._data.write(self._path)
        
        print('Birthday deleted for {0}'.format(name))
        
    
    def search_name_entry(self, name):
        nameNode = self._root.find(".//person[@name='{0}']".format(name))
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
           or (month == date.today().month and day < date.today().day)):
            age = age + 1
        
        print('Next birthday for {0}: {1} {2} ({3})'.format(
			name, 
			monthStr,
            day,
			age
			))
    
    def search_next_entries(self, searchByMonth, interval):
        currentMonth = date.today().month
#         currentMonth = 12
        lastMonth = (currentMonth + interval) % 12
        
        if(searchByMonth):
            for element in self._monthNodes:
                localMonth = int(element.get('index'))
                if( (lastMonth > currentMonth 
                     and localMonth >= currentMonth 
                     and localMonth < lastMonth)
                   or (lastMonth < currentMonth
                     and(localMonth >= currentMonth
                      or localMonth < lastMonth))):
                    print('Birthdays in {0}: '.format(calendar.month_name[localMonth]))
                    for day in element.iter('day'):
                        dayIndex = day.get('index')
                        for person in day.iter('person'): 
                            print('\t -{0}: {1} ({2})'.format(
                                dayIndex,
                                person.get('name'),
                                date.today().year - int(person.get('year'))
                                )
                            )
    
        
    def show_next_month_data(self):
        self.search_next_entries(True, 1)
    
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
            
