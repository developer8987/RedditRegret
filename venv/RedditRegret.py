import sys
import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

#Constants
username_field_xpath = "//input[@placeholder='username']"
password_field_xpath = "//input[@placeholder='password']"
submit_button_xpath = "//button[text()='login']"
username_button_xpath = "/html[1]/body[1]/div[2]/div[3]/span[1]/a[1]"
comments_link_xpath = "//a[contains(text(),'Comments')]"

#WebDriver setup
print "Setting up WebDriver..."
try:
    rp = 'firebug-2.0.19.xpi'
    firefoxProfile = webdriver.FirefoxProfile()
    firefoxProfile.add_extension(rp)
except:
    print "*** ERROR ***"
    print "*** You need to have the 'firebug-2.0.19.xpi' file in the same directory as this script."
    print "*** In order to build this file, simply go to https://github.com/firebug/firebug and"
    print "*** navigate to the 'Build Firebug XPI' section, and follow the instructions to build the .xpi"
    print "*** If the version is different, just change the 'rp = 'firebug-2.0.19.xpi'' line in this script"
    print "*** to the version you have built. This program will now self-destruct. Have a blessed day."
    print "*** ERROR ***"
    exit()

driver = webdriver.Firefox(firefox_profile=firefoxProfile)
print "*** DONE ***"

#Open Reddit
print "Loading (old) Reddit site..."
driver.get("https://old.reddit.com")
wait = WebDriverWait(driver,10)
print "*** DONE ***"

#Log in
print "Logging in using the provided username and password..."
try:
    username = sys.argv[1]
    password = sys.argv[2]
except:
    print "*** ERROR ***"
    print "You must provide a username and a password as command line arguments. This program will now stop. "
    print "Please rerun the script in the following manner: '~ python RedditRegret.py myusername mypassword' "
    print "*** ERROR ***"
    exit()
wait.until(EC.element_to_be_clickable((By.XPATH, username_field_xpath)))
username_field = driver.find_element_by_xpath(username_field_xpath)
username_field.send_keys(username)
wait.until(EC.element_to_be_clickable((By.XPATH, password_field_xpath)))
password_field = driver.find_element_by_xpath(password_field_xpath)
password_field.send_keys(password)




time.sleep(5)


wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
submit_button = driver.find_element_by_xpath(submit_button_xpath)
submit_button.click()


time.sleep(15)


print "*** DONE ***"

#Go to comment history
print "Navigating to comment history..."
wait.until(EC.element_to_be_clickable((By.XPATH, username_button_xpath)))
username_button = driver.find_element_by_xpath(username_button_xpath)
username_button.click()
wait.until(EC.element_to_be_clickable((By.XPATH, comments_link_xpath)))
comments_link = driver.find_element_by_xpath(comments_link_xpath)
comments_link.click()
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
try:
    while True:
        while counter < 50:
            # time.sleep(0.2)
            delete_link = driver.find_element_by_link_text('delete')
            delete_link.click()
            yes_link = driver.find_element_by_link_text('yes')
            yes_link.click()
            counter = counter + 2
            print "Deleted " + str(page) + " comments..."
            page = page + 1
        driver.refresh()
        # time.sleep(0.2)
        counter = 1
except NoSuchElementException:
    print "Looks like we couldn't find a delete button."
    print "Either you're all out of comments,"
    print "...or we're all out of options. Thanks for using RedditRegret."
    exit()
