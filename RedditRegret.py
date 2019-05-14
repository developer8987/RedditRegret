import sys
from selenium.webdriver.common.by import By
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#WebDriver setup
print "Setting up WebDriver..."
rp = 'firebug-2.0.19.xpi'
firefoxProfile = webdriver.FirefoxProfile()
firefoxProfile.add_extension(rp)
driver = webdriver.Firefox(firefox_profile=firefoxProfile)
mouse = webdriver.ActionChains(driver)
print "*** DONE ***"

#Open Reddit
print "Loading (old) Reddit site..."
driver.get("https://old.reddit.com")
wait = ui.WebDriverWait(driver,10)
print "*** DONE ***"

#Log in
print "Logging in using the provided username and password..."
username_field = driver.find_element_by_xpath("//input[@placeholder='username']")
password_field = driver.find_element_by_xpath("//input[@placeholder='password']")
submit_button = driver.find_element_by_xpath("//button[@type='submit']")
username = sys.argv[1]
password = sys.argv[2]
username_field.send_keys(username)
password_field.send_keys(password)
submit_button.click()
time.sleep(2)
print "*** DONE ***"

#Go to comment history
print "Navigating to comment history..."
username_button = driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[3]/span[1]/a[1]")
time.sleep(2)
username_button.click()
time.sleep(2)
comments_link = driver.find_element_by_xpath("//a[contains(text(),'Comments')]")
comments_link.click()
time.sleep(2)
print "*** DONE ***"

#Confirm to proceed
print ""
print "*** WARNING ***"
print "You are about to erase your entire comment history! This cannot be undone!"
print "*** WARNING ***"

confirm_delete_all_comments = raw_input("Please type 'DELETE' in ALL CAPS to ERASE ALL COMMENTS: ")
if confirm_delete_all_comments != "DELETE":
	sys.exit()

#DELETE COMMENT LOOP
print "Deleting comments..."
counter = 1
page = 1

while True:
    while counter < 50:
        #time.sleep(0.2)
        delete_link = driver.find_element_by_link_text('delete')
        delete_link.click()

        yes_link = driver.find_element_by_link_text('yes')
        yes_link.click()
        counter = counter + 2
        print "Deleted " + str(page) + " comments..."
        page = page + 1

    driver.refresh()
    #time.sleep(0.2)
    counter = 1
