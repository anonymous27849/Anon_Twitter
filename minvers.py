#TO RUN
#TERMINAL, WORKON WILDHACKS (VIRTUALENV)
#PYTHON MINVERS.PY 

from selenium import webdriver
import getpass

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# go to the google home page
driver.get("http://www.twitter.com")

username = "wildhacks"
password = getpass.getpass()

driver.execute_script("$('#front-container #signin-email').val('%s');"  % (username))
driver.execute_script("$('#front-container #signin-password').val('%s');" % (password))


driver.execute_script("$('#signin-email').val('testusername');")
driver.execute_script("$('#signin-password').val('testpassword');")

#currenly it runs, opens firefox, goes to twitter, and asks for password in terminal

#need to implement click submit button 