from selenium import webdriver
import BotEngine


chromedriver_path = 'chromedriver' 
webdriver = webdriver.Chrome(executable_path=chromedriver_path)

BotEngine.init(webdriver)
BotEngine.update(webdriver)

webdriver.close()

