#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""RedditRegret - delete all your comments!"""

import os
import sys
import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

# Constants
website_url = "https://old.reddit.com"
username_field_xpath = "//input[@placeholder='username']"
password_field_xpath = "//input[@placeholder='password']"
submit_button_xpath = "//button[text()='login']"
username_button_xpath = "//span[@class='user']//a[contains(@href, 'https://old.reddit.com/user/')]"
comments_link_xpath = "//a[text()='comments']"
comments_error_xpath = "//div[@class='ProfileCommentsPage__error']"
upvote_count_xpath = ".//span[@class='score likes']"
main_comment_xpath = "//div[@data-type='comment']"

# WebDriver setup (you need to have Chromedriver installed, look it up)
print "Setting up WebDriver..."
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)
print "*** DONE ***"

# Open Reddit
print "Loading (old) Reddit site..."
driver.get(website_url)
wait = WebDriverWait(driver, 10)
print "*** DONE ***"

# Log in
print "Logging in using the provided username and password..."

try:
    username = sys.argv[1]
    password = sys.argv[2]
except:
    print """ *** ERROR ***
    You must provide a username and a password as command line arguments. This program will now stop.
    Please rerun the script in the following manner: '~ python RedditRegret.py myusername mypassword'
    *** ERROR *** """
    exit()
wait.until(EC.element_to_be_clickable((By.XPATH, username_field_xpath)))
username_field = driver.find_element_by_xpath(username_field_xpath)
username_field.send_keys(username)
wait.until(EC.element_to_be_clickable((By.XPATH, password_field_xpath)))
password_field = driver.find_element_by_xpath(password_field_xpath)
password_field.send_keys(password)
wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
submit_button = driver.find_element_by_xpath(submit_button_xpath)
submit_button.click()
print "*** DONE ***"

# Go to comment history
print "Navigating to comment history..."
wait.until(EC.element_to_be_clickable((By.XPATH, username_button_xpath)))
username_button = driver.find_element_by_xpath(username_button_xpath)
username_button.click()
wait.until(EC.element_to_be_clickable((By.XPATH, comments_link_xpath)))
comments_link = driver.find_element_by_xpath(comments_link_xpath)
comments_link.click()
upvote_count_list = driver.find_elements_by_xpath(upvote_count_xpath)
print "*** DONE ***"

# Check if there are comments, and confirm to proceed
try:
    nocomments = driver.find_element_by_xpath(comments_error_xpath)
    print "\n*** LOOKS LIKE YOU HAVE NO COMMENTS! EXITING! *** \n\nThank you for using RedditRegret."
    sys.exit()
except Exception:
    print """ 
    *** WARNING ***
    You are about to erase your entire comment history! This cannot be undone!
    *** WARNING *** """
    confirm_delete_all_comments = raw_input("Please type 'DELETE' in ALL CAPS to ERASE ALL COMMENTS: ")
    if confirm_delete_all_comments != "DELETE":
        print "GOOD CHOICE"
        sys.exit()

# DELETE COMMENT LOOP
print "Deleting comments..."

counter = 1
page = 1
try:
    while True:
        time.sleep(0.2)
        mainElementList = driver.find_elements_by_xpath(main_comment_xpath)
        for element in mainElementList:
            commentCount = element.find_element_by_xpath(upvote_count_xpath).get_attribute('Title')
            print commentCount
            if int(commentCount) < 11:
                time.sleep(0.2)
                delete_link = element.find_element_by_link_text('delete')
                delete_link.click()
                time.sleep(0.2)
                yes_link = element.find_element_by_link_text('yes')
                yes_link.click()
                print "Deleted " + str(page) + " comments..."
                page = page + 1

        driver.refresh()
        time.sleep(0.2)
except NoSuchElementException:
    print """ 

    *** DONE! ***

    Looks like we couldn't find a delete button.
    Either you're all out of comments,
    ...or we're all out of options. Thanks for using RedditRegret. """
    exit()
