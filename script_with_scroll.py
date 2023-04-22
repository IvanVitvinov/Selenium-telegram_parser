from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


class ParserUser:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.user_list = []
        self.processed_containers = []
        self.count = 0
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        self.driver = webdriver.Chrome(options=options)
        self.action = ActionChains(self.driver)

    def start_browser(self, id_chat):

            # Переходим по ссылке
            self.driver.get(f"https://web.telegram.org/k/#{id_chat}")
            time.sleep(20)
            print(1)

    def get_user_names(self, filename):

        try:
                containers = self.driver.find_elements(By.CLASS_NAME, 'bubble-content-wrapper')
                print(len(containers))
                print(containers)
                print(reversed(containers))
                for container in reversed(containers):
                    # Проверяем, был ли элемент уже обработан
                    if container in self.processed_containers:
                        print('cointunie')
                        continue
                    try:
                        title = container.find_element(By.CLASS_NAME, "peer-title")
                        title.click()
                        time.sleep(3)
                    except Exception as e:
                        ActionChains(self.driver).send_keys(Keys.PAGE_UP).perform()
                        self.get_user_names(filename)
                        print(e)

                    current_url = self.driver.current_url
                    username = current_url.split('#')[1]
                    self.user_list.append(username)
                    time.sleep(5)

                    btn_end = self.driver.find_element(By.CSS_SELECTOR, '#column-center > div > div.chat.tabs-tab.active > div.sidebar-header.topbar > div.chat-info-container > button')
                    ActionChains(self.driver).move_to_element(btn_end).perform()
                    btn_end.click()
                    time.sleep(3)

                    self.processed_containers.append(container)

                    center_x = self.driver.execute_script("return window.innerWidth / 2")
                    center_y = self.driver.execute_script("return window.innerHeight / 2")

                    ActionChains(self.driver).move_by_offset(center_x, center_y).perform()
                    self.driver.execute_script("window.scrollBy(0, -100);")

                    if len(self.user_list) > 20:
                        break

                with open(filename, 'w') as f:
                    f.write('\n'.join(self.user_list))

        except Exception as e:
            self.close_browser()
            print(e)

    def close_browser(self):
        self.driver.quit()
        self.driver.close()

def main():
    parser = ParserUser()
    parser.start_browser('-1583493187')
    parser.get_user_names('5000users.txt')
    parser.close_browser()


if __name__ == "__main__":
    main()

