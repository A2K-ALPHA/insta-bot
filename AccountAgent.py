import datetime
from logging import exception
import random
from time import sleep
import traceback
import Constants
import DBUsers
from selenium.webdriver.common.by import By
ID = "id"
NAME = "name"
XPATH = "xpath"
LINK_TEXT = "link text"
PARTIAL_LINK_TEXT = "partial link text"
TAG_NAME = "tag name"
CLASS_NAME = "class name"
CSS_SELECTOR = "css selector"

def login(webdriver):
    #Open the instagram login page
    webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    #sleep for 3 seconds to prevent issues with the server
    sleep(3)
    #Find username and password fields and set their input using our constants
    try:
        username = webdriver.find_element(By.NAME,'username')
        username.send_keys(Constants.INST_USER)
        password = webdriver.find_element(By.NAME,'password')
        password.send_keys(Constants.INST_PASS)
        #Get the login button
        try:
            button_login = webdriver.find_element(By.XPATH,
                '//*[@id="loginForm"]/div/div[3]/button/div')
                
        except:
            button_login = webdriver.find_element(By.XPATH,
                '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[6]/button/div')
        #sleep again
        sleep(2)
        #click login
        button_login.click()
        sleep(3)
        #In case you get a popup after logging in, press not now.
        #If not, then just return
    except:
        print("you logged in directly")
    try:
        notnow = webdriver.find_element(By.CSS_SELECTOR,
            'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
        notnow.click()
    except:
        return

def unfollow_people(webdriver, people):
    #if only one user, append in a list
    if not isinstance(people, (list,)):
        p = people
        people = []
        people.append(p)

    for user in people:
        try:
            webdriver.get('https://www.instagram.com/' + user + '/')
            sleep(5)
            unfollow_xpath = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[2]/button'

            unfollow_confirm_xpath = '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[1]'

            if webdriver.find_element(By.XPATH,unfollow_xpath).text != "Follow":
                sleep(random.randint(4, 15))
                webdriver.find_element(By.XPATH,unfollow_xpath).click()
                sleep(2)
                webdriver.find_element(By.XPATH,unfollow_confirm_xpath).click()
                sleep(4)
            DBUsers.delete_user(user)

        except Exception:
            traceback.print_exc()
            continue


def follow_people(webdriver):
    #all the followed user
    prev_user_list = DBUsers.get_followed_users()
    #a list to store newly followed users
    new_followed = []
    #counters
    followed = 0
    likes = 0
    #Iterate theough all the hashtags from the constants
    for hashtag in Constants.HASHTAGS:
        #Visit the hashtag
        print(hashtag)
        webdriver.get('https://www.instagram.com/explore/tags/' + hashtag+ '/')
        sleep(5)

        #Get the first post thumbnail and click on it
        first_thumbnail = webdriver.find_element(By.XPATH,
            '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]')

        first_thumbnail.click()
        sleep(random.randint(1,3))

        try:
            #iterate over the first 200 posts in the hashtag
            l=0
            for x in range(1,200):
                t_start = datetime.datetime.now()
                #Get the poster's username
                username = webdriver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div/div[1]/span/a').text
                print(username)
                likes_over_limit = False
                likes_over_limit = True
                try:
                    #get number of likes and compare it to the maximum number of likes to ignore post
                    """likes_t=(webdriver.find_element(By.XPATH,
                        '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/div/a/div').text).replace("likes",'')
                    likes_t=likes_t.replace(",",'')
                    likes = int(likes_t[:-1])
                    if likes > Constants.LIKES_LIMIT:
                        print("likes over {0}".format(Constants.LIKES_LIMIT))
                        likes_over_limit = True"""


                    print("Detected: {0}".format(username))
                    #If username isn't stored in the database and the likes are in the acceptable range
                    if username not in prev_user_list and likes_over_limit:
                        #Don't press the button if the text doesn't say follow
                        try:
                            if webdriver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div/div').text == 'Follow':
                                #Use DBUsers to add the new user to the database
                                DBUsers.add_user(username)
                                #Click follow
                                x=webdriver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div/div')
                                print(x.text)
                                x.click()
                                followed += 1
                                
                                print("Followed: {0}, #{1}".format(username, followed))
                                new_followed.append(username)
                        except Exception as e:
                            print("followed")

                        # Liking the picture
                        button_like = webdriver.find_element(By.XPATH,
                            '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button')

                        button_like.click()
                        likes += 1
                        print("Liked {0}'s post, #{1}".format(username, likes))
                        sleep(random.randint(5, 18))

                    if l==0:
                        path='/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div/button'
                    else:
                        path='/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button'
                    
                    # Next picture
                    l+=1
                    sleep(2)
                    
                    but1=webdriver.find_element(By.XPATH,path)
                    try:
                        but1.click()
                    except Exception as e:
                        print("hello")
                        print(e)
                    sleep(random.randint(10, 20))
                    
                except:
                    traceback.print_exc()
                    continue
                t_end = datetime.datetime.now()

                #calculate elapsed time
                t_elapsed = t_end - t_start
                print("This post took {0} seconds".format(t_elapsed.total_seconds()))


        except:
            traceback.print_exc()
            continue

        #add new list to old list
        for n in range(0, len(new_followed)):
            prev_user_list.append(new_followed[n])
        print('Liked {} photos.'.format(likes))
        print('Followed {} new people.'.format(followed))