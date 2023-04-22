from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
import pyautogui
import time


class ParserUser:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.user_list = []
        self.count_usernames = 1000   # Set the number of usernames we want to get from the chat

    def start_browser(self, id_chat):
            # Open telegram chat by link
            self.driver.get(f"https://web.telegram.org/k/#{id_chat}")
            time.sleep(20)

    def get_user_names(self, filename):
        try:
            while len(self.user_list) < self.count_usernames:

                # Create a container for processed messages
                processed_containers = []
                time.sleep(1)

                # Looking for messages on the page
                containers = self.driver.find_elements(By.CLASS_NAME, 'bubble-content-wrapper')

                # Reverse the list, since the messages in the chat are in reverse order
                containers_reversed = list(reversed(containers))

                # Loop through all messages from the flipped list and add usernames to the list
                for container in containers_reversed:
                    # Resave the finished file every 50 new usernames
                    if len(self.user_list) % 50 == 0:
                        with open(filename, 'w') as f:
                            f.write('\n'.join(self.user_list))
                            print('Write data to file')

                    # Check if the element has already been processed
                    if container in processed_containers:
                        print('cointunie')
                        continue

                    # Skip forwarded messages
                    try:
                        if container.find_elements(By.CLASS_NAME, "reply.is-overriding-color"):
                            print("Skipping container with reply")
                            continue
                    except Exception as e:
                        self.get_user_names(filename)
                        print(e)

                    # Trying to click on a username
                    try:
                        title = container.find_element(By.CLASS_NAME, "peer-title")
                        try:
                            title.click()
                        except ElementClickInterceptedException:
                            print("ElementClickInterceptedException occurred, trying to scroll and continue.")
                            continue
                        time.sleep(1)
                    except Exception as e:
                        self.scroll_chat()
                        print(e)

                    # Cut from url username
                    current_url = self.driver.current_url
                    if '#' in current_url:
                        username = current_url.split('#')[1]
                        self.user_list.append(username)
                    else:
                        print("Could not find character '#' in URL.")
                        continue

                    # Back to chat
                    btn_end = self.driver.find_element(By.CSS_SELECTOR, '#column-center > div > div.chat.tabs-tab.active > div.sidebar-header.topbar > div.chat-info-container > button')
                    try:
                        ActionChains(self.driver).move_to_element(btn_end).perform()
                        btn_end.click()
                        time.sleep(1)
                    except MoveTargetOutOfBoundsException:
                        print("MoveTargetOutOfBoundsException occurred, trying to scroll and continue.")
                        continue

                    processed_containers.append(container)
                    # Scroll through the chat looking for new messages
                    self.scroll_chat()

            with open(filename, 'w') as f:
                f.write('\n'.join(self.user_list))

        # Catch the exception and return to the function
        except StaleElementReferenceException:
            self.scroll_chat()
            self.scroll_chat()
            self.get_user_names(filename)

    def close_browser(self, filename):
        self.driver.quit()
        self.driver.close()
        with open(filename, 'w') as f:
            f.write('\n'.join(self.user_list))

    @staticmethod
    def scroll_chat():
        try:
            time.sleep(1)
            pyautogui.scroll(15)
            time.sleep(1)

        except Exception as e:
            print(e)
            print("Don't scroll")


def main():
    parser = ParserUser()
    parser.start_browser('chat_id')
    parser.get_user_names('1000.txt')
    parser.close_browser('1000.txt')


if __name__ == "__main__":
    main()

