from selenium.webdriver import Chrome
import time
from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import re
def split_word(word):
    return [char for char in word]

browser = Chrome()
browser.get('https://sis.ndu.edu.lb/advreg/bin/home_online.asp')
student_button = browser.find_element_by_id("Image7")
student_button.click()
username = browser.find_element_by_id('textfield')
password = browser.find_element_by_id('textfield2')

user_input = input("Username: ")
pass_input = input("Password: ")
username.send_keys(user_input)
password.send_keys(pass_input)
login = browser.find_element_by_id('Image8')
login.click()
browser.switch_to.frame('left')
contract_sheet = browser.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[5]/td/table/tbody/tr/td[2]/a')
contract_sheet.click()
browser.switch_to.default_content()
browser.switch_to.frame('body')
table = browser.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[2]/table")
sheet = table.find_elements_by_xpath("/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/pre/div")
line_sheet = sheet[0].text.splitlines()
majors = line_sheet.index("           MAJOR REQUIREMENTS ( 79 cr. )                                  ")
end_of_majors = line_sheet.index(" EEN  599  2                                                   ")
courses = []
for line in line_sheet[majors:end_of_majors+1]:
    if line.startswith(' CS') or line.startswith(' EE'):
        courses.append(line)
remaining_courses = []
for course in courses:
    if course[15] == ' ':
        remaining_courses.append(course)
        
for index, course in enumerate(remaining_courses):
    course = course[1:9]
    course = ''.join(course.split())
    remaining_courses[index] = course
browser.switch_to.default_content()

browser.switch_to.frame('left')
offerings = browser.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[13]/td/table/tbody/tr/td[2]/a')
offerings.click()
browser.switch_to.default_content()
browser.switch_to.frame('body')


el = browser.find_element_by_name('sem')
for option in el.find_elements_by_tag_name('option'):
    if option.text.strip() == "Fall 2021":
         option.click()



for index,course in enumerate(remaining_courses):
    course_search = browser.find_element_by_name('Mask')
    search = browser.find_element_by_name('Image8')
    course_search.send_keys(course)
    search.click()
    try:
        time = browser.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td[5]/span')
    except:
        new = split_word(course)
        new[3] = str(int(new[3])+1)
        new = ''.join(new)
        remaining_courses[index] = new

for course in remaining_courses:
    course_search = browser.find_element_by_name('Mask')
    search = browser.find_element_by_name('Image8')
    course_search.send_keys(course)
    search.click()
    try:
        time = browser.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[5]/span')
    except:
        print(course + " is not available this semester.")
    else:
        print(course + ": " + time.text)
