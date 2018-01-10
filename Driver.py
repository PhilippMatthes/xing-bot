from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.common.keys import Keys
import pickle
import datetime
from pickle import UnpicklingError

from Log import Log
from Config import Config

if Config.headless_is_available:
    from xvfbwrapper import Xvfb


def timestamp():
    return time.strftime('%a %H:%M:%S') + " "


def focus(browser, element):
    browser.execute_script("arguments[0].focus();", element)


class Driver(object):
    def __init__(self):
        # Set up virtual display
        if Config.headless_is_available:
            self.display = Xvfb()
            self.display.start()

        # Load history
        try:
            with open("log/requested_users.pickle", "rb") as f:
                self.requested_users = pickle.load(f)
        except FileNotFoundError:
            with open("log/requested_users.pickle", "wb") as f:
                self.requested_users = {}
                pickle.dump({}, f)

        # Load Username
        try:
            with open("log/username.pickle", "rb") as f:
                self.username = pickle.load(f)
        except FileNotFoundError:
            key = input("Please enter your username: ")
            while len(key) == 0:
                key = input("You must enter a username. Please try again: ")
            with open("log/username.pickle", "wb") as f:
                pickle.dump(key, f)
            self.username = key

        # Load Password
        try:
            with open("log/password.pickle", "rb") as f:
                self.password = pickle.load(f)
        except FileNotFoundError:
            key = input("Please enter your password: ")
            while len(key) == 0:
                key = input("You must enter a password. Please try again: ")
            with open("log/password.pickle", "wb") as f:
                pickle.dump(key, f)
            self.password = key

        # Final setup
        if Config.headless_is_available:
            self.browser = webdriver.PhantomJS()
        else:
            self.browser = webdriver.Chrome("./chromedriver")

        if Config.headless_is_available:
            self.browser.set_window_size(1980, 1080)

    def login(self, browser):
        Log.send("Logging in.")
        browser.get(Config.start_url)
        sleep(Config.load_delay)

        if browser.current_url == Config.logged_in_url:
            return

        try:
            browser.find_element_by_id(Config.login_button_id).click()
            sleep(Config.load_delay)
            browser.find_element_by_name(Config.login_form_username_name).send_keys(self.username)
            password_field = browser.find_element_by_name(Config.login_form_password_name)
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)
            sleep(Config.login_delay)
            return

        except KeyboardInterrupt:
            return

        except Exception as e:
            self.exception_routine(browser, e)

    def unrequest(self, browser, amount_of_users=5):
        Log.send("Unrequesting {} users.".format(amount_of_users))
        browser.get(Config.contacts_unconfirmed_url)
        sleep(Config.load_delay)

        try:
            user_sections = browser.find_elements_by_xpath(Config.contacts_unconfirmed_section_xpath)

            for section in user_sections:

                if amount_of_users < 1:
                    break

                section_user_name = section.find_element_by_xpath(
                    Config.contacts_unconfirmed_section_subclass_username_xpath).text

                for user in [k for k, v in sorted(self.requested_users.items(), key=lambda p: p[1], reverse=True)]:
                    if section_user_name == user and amount_of_users > 0:
                        delete_element = section.find_element_by_xpath(
                            Config.contacts_unconfirmed_section_subclass_delete_xpath)
                        focus(browser, delete_element)
                        delete_element.click()
                        sleep(Config.load_delay)

                        frame = browser.find_element_by_id(Config.contacts_unconfirmed_confirm_deletion_frame_id)
                        frame.find_element_by_xpath(Config.contacts_unconfirmed_confirm_deletion_xpath).click()

                        Log.send("Unrequested: {}".format(section_user_name))

                        amount_of_users -= 1
                        sleep(Config.unrequest_delay)

        except KeyboardInterrupt:
            return

        except Exception as e:
            self.exception_routine(browser, e)

    def request(self, browser, amount_of_users=5):
        Log.send("Requesting {} users.".format(amount_of_users))
        browser.get(Config.contacts_recommended_url)
        sleep(Config.load_delay)

        try:
            user_sections = browser.find_elements_by_xpath(Config.contacts_recommended_card_xpath)

            for section in user_sections:

                if amount_of_users < 1:
                    break

                focus(browser, section)
                section_user_name = section.find_element_by_xpath(Config.contacts_recommended_username_xpath).text
                if section_user_name in self.requested_users.keys():
                    continue
                section.find_element_by_xpath(Config.contacts_recommended_add_button_xpath).click()
                Log.send("Requested: {}".format(section_user_name))
                self.requested_users[section_user_name] = datetime.datetime.now()
                with open("log/requested_users.pickle", "wb") as f:
                    pickle.dump(self.requested_users, f)

                amount_of_users -= 1
                sleep(Config.request_delay)

        except KeyboardInterrupt:
            return

        except Exception as e:
            self.exception_routine(browser, e)


    def exception_routine(self, browser, exception):
        browser.save_screenshot('error.png')
        Log.send_image('error.png', str(exception))
        sleep(Config.exception_delay)
        self.login(browser)

    def run(self):
        self.login(self.browser)
        self.request(self.browser, Config.requests_per_batch)
        self.unrequest(self.browser, Config.requests_per_batch)
