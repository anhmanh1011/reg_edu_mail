import concurrent
import random
import string
import time
import traceback
from collections import namedtuple

import psycopg2 as psycopg2
import requests
import undetected_chromedriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

# Press the green button in the gutter to run the script.
conn = psycopg2.connect(
    host="localhost",
    database="db",
    user="root",
    password="root"
)

# Open a cursor to perform database operations
# conn.autocommit = True

cur = conn.cursor()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def wait_util(driver: uc.Chrome, by: By, element: str, time: int) -> any:
    return WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((by, element)))


def generate_ssn():
    area_number = random.randint(1, 899)
    group_number = random.randint(1, 99)
    serial_number = random.randint(1, 9999)
    return "{:03d}{:02d}{:04d}".format(area_number, group_number, serial_number)


def get_name_generator(count: int) -> list:
    r = requests.get("https://randomuser.me/api/?inc=gender,name,login,cell&nat=us&results=%s" % count)
    if r.status_code == 200:
        response_json = r.json()
        data = response_json['results']
        print(data)
        my_list = []
        for item in data:
            my_list.append({'first_name': item['name']['first'], 'last_name': item['name']['last'],
                            'user_name': item['login']['username'], 'cell': item['cell']})
        return my_list
    raise Exception("Loi get_name_generator")


def remove_char(s: str) -> str:
    digits = [int(char) for char in s if char.isdigit()]
    result = int(''.join(map(str, digits)))
    return result


def generate_birthday() -> str:
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(2000, 2002)
    return "{:02d}/{:02d}/{:04d}".format(month, day, year)


def generate_email():
    username_length = random.randint(5, 10)
    domain_length = random.randint(5, 10)
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(username_length))
    domain = ''.join(random.choice(string.ascii_lowercase) for _ in range(domain_length))
    return f"{username}@gmail.com"


def get_current_ip() -> str:
    url = "https://httpbin.org/ip"
    response = requests.request("GET", url)
    data = response.json()
    return data['origin']


def get_addr() -> list:
    url = "http://api.positionstack.com/v1/reverse?access_key=00df51f9752b0f25abae1be5b1999b79&query=" + get_current_ip()
    print(url)
    response = requests.request("GET", url)
    lst: list = []
    if (response.status_code == 200):
        data = response.json()
        print(data)
        for item in data['data']:
            addr_name: str = ''.join(item['name'])
            city = item['locality']
            state = item['region_code']
            postal_code = item['postal_code']
            lst.append({'addr_name': addr_name, 'city': city, 'state': state, 'postal_code': postal_code})
        return lst
    raise Exception('Khong the get vi tri')


def run(email, user, addr) -> str:
    str_insert = "insert into public.edu_csn ( first_name, last_name, cell, addr, city, state_country, postal_code, email_id, status) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)"
    first_name: str = user['first_name']
    last_name: str = user['last_name']
    cell: str = remove_char(user['cell'])
    addr_name: str = addr['addr_name']
    city: str = addr['city']
    state_country: str = addr['state']
    postal_code: str = addr['postal_code']
    email_id: str = email.id
    status: str = 'SUCCESS'
    options = uc.ChromeOptions()
    # options.add_argument(
    #     "--load-extension=C:\\Users\\daoma\\PycharmProjects\\github_student_pack\\dknlfmjaanfblgfdfebhijalfmhmjjjo\\0.3.4_0")
    # options.add_argument("--window-size=270,425")
    proxy = "smartproxy.crawlbase.com:8012"
    # options.add_argument("--proxy-server=%s" % proxy)
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--disable-application-cache")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-application-cache")

    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)

    # options.add_experimental_option("detach", True)
    # options.add_argument("--app=https://httpbin.org/ip")

    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # captcha_key = '0d3baac93ed3fbbbddb7dfac3f529f88'
    # options.add_argument(r'--load-extension=D:\ifibfemgeogfhoebkmokieepdoobkbpo\3.3.1_0')
    driver = uc.Chrome(service=Service(
        r"C:\\Users\\daoma\\appdata\\roaming\\undetected_chromedriver\\undetected\\chromedriver.exe"),
        options=options)
    try:

        # driver.get(
        #     "https://nopecha.com/setup#sub_1MizllCRwBwvt6pteITkRiia|enabled=true|disabled_hosts=%5B%5D|hcaptcha_auto_open=true|hcaptcha_auto_solve=true|hcaptcha_solve_delay=true|hcaptcha_solve_delay_time=3000|recaptcha_auto_open=true|recaptcha_auto_solve=true|recaptcha_solve_delay=true|recaptcha_solve_delay_time=1000|recaptcha_solve_method=Image|funcaptcha_auto_open=true|funcaptcha_auto_solve=true|funcaptcha_solve_delay=true|funcaptcha_solve_delay_time=1000|awscaptcha_auto_open=true|awscaptcha_auto_solve=true|awscaptcha_solve_delay=true|awscaptcha_solve_delay_time=1000|textcaptcha_auto_solve=true|textcaptcha_solve_delay=true|textcaptcha_solve_delay_time=100|textcaptcha_image_selector=|textcaptcha_input_selector=")
        time.sleep(2)
        driver.get("https://my.csn.edu/en-US/sign-up/")

        wait_util(driver, By.ID, "ContentContainer_MainContent_FirstName", 10).send_keys(first_name)
        driver.find_element(By.ID, 'ContentContainer_MainContent_LastName').send_keys(last_name)
        driver.find_element(By.ID, 'ContentContainer_MainContent_Email').send_keys(email.username)
        driver.find_element(By.ID, 'ContentContainer_MainContent_Password').send_keys('Anhmanhbu8')
        driver.find_element(By.ID, 'ContentContainer_MainContent_ConfirmPassword').send_keys('Anhmanhbu8')
        driver.find_element(By.ID, 'Birthday').send_keys(generate_birthday())
        driver.find_element(By.ID, 'ContentContainer_MainContent_chkAgreeWithTermsAndConditions').click()
        driver.find_element(By.ID, 'ApplyBtn').click()
        time.sleep(2)
        driver.find_element(By.ID, 'ContentContainer_MainContent_SubmitLenderSignUpButton').click()
        wait_util(driver, By.ID, 'firsttimecollegeseeking', 10).click()
        driver.find_element(By.ID, 'CustomNext').click()
        time.sleep(5)
        driver.find_element(By.ID, 'CustomNext').click()
        time.sleep(5)
        foundry_academicperiod = driver.find_element(By.ID, "foundry_academicperiod")
        foundry_academicperiod_name = driver.find_element(By.ID, "foundry_academicperiod_name")
        foundry_academicperiod_entityname = driver.find_element(By.ID, "foundry_academicperiod_entityname")
        driver.execute_script(f"arguments[0].value='4be38c76-c554-ed11-bba2-000d3a582176';", foundry_academicperiod)
        driver.execute_script(f"arguments[0].value='Spring 2023';", foundry_academicperiod_name)
        driver.execute_script(f"arguments[0].value='mshied_academicperiod';", foundry_academicperiod_entityname)

        grmtr_csncampus_name = driver.find_element(By.ID, "grmtr_csncampus_name")
        grmtr_csncampus = driver.find_element(By.ID, "grmtr_csncampus")
        grmtr_csncampus_entityname = driver.find_element(By.ID, "grmtr_csncampus_entityname")
        driver.execute_script(f"arguments[0].value='Online Campus';", grmtr_csncampus_name)
        driver.execute_script(f"arguments[0].value='f79bc385-5c88-ed11-81ad-0022481d6e55';",
                              grmtr_csncampus)
        driver.execute_script(f"arguments[0].value='account';", grmtr_csncampus_entityname)

        select = Select(driver.find_element(By.ID, 'gendercode'))
        select.select_by_value('1')

        driver.find_element(By.ID, "address1_line1").send_keys(addr_name)
        driver.find_element(By.ID, "address1_city").send_keys(city)
        driver.find_element(By.ID, "address1_stateorprovince").send_keys(state_country)
        driver.find_element(By.ID, "address1_postalcode").send_keys(postal_code)
        driver.find_element(By.ID, "telephone1").send_keys(cell)

        select_country = Select(driver.find_element(By.ID, "grmtr_contactcountry"))
        select_country.select_by_value('595360000')
        # driver.execute_script(f"arguments[0].value='595360000';", grmtr_contactcountry)

        address1_addresstypecode = driver.find_element(By.ID, "address1_addresstypecode")
        driver.execute_script(f"arguments[0].value='1';", address1_addresstypecode)

        driver.find_element(By.ID, "grmtr_donottext_0").click()

        driver.find_element(By.ID, 'CustomNext').click()

        time.sleep(5)

        grmtr_highschooleducation = driver.find_element(By.ID, "grmtr_highschooleducation")
        driver.execute_script(f"arguments[0].value='595360000';", grmtr_highschooleducation)
        driver.find_element(By.XPATH,
                            '/html/body/div[4]/form/div[4]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset[2]/table/tbody/tr[1]/td[1]/div[2]/div[1]/div[2]/button[2]').click()
        time.sleep(2)
        driver.find_element(By.XPATH,
                            '/html/body/div[4]/form/div[4]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/div/section/div/div/div[2]/div[2]/div[1]/div/div/input').send_keys(
            addr['city'] + Keys.ENTER)
        time.sleep(5)
        wait_util(driver, By.XPATH,
                  '/html/body/div[4]/form/div[4]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/div/section/div/div/div[2]/div[2]/div[2]/table/tbody/tr[1]',
                  20).click()
        # driver.find_element(By.XPATH,
        #                     '/html/body/div[4]/form/div[4]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset[2]/table/tbody/tr[1]/td[1]/div[2]/div[2]/div/section/div/div/div[2]/div[2]/div[2]/table/tbody/tr[1]').click()
        time.sleep(2)
        wait_util(driver, By.ID, 'btnModalSelect', 20).click()
        # driver.find_element(By.ID, 'btnModalSelect').click()
        time.sleep(2)

        wait_util(driver, By.XPATH,
                  '/html/body/div[4]/form/div[4]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/div/fieldset[2]/table/tbody/tr[3]/td[1]/div[2]/div/input',
                  20).send_keys(
            "02/02/2023")
        time.sleep(2)

        driver.find_element(By.ID, 'CustomNext').click()
        time.sleep(5)

        grmtr_transferringtocsnhighschool_name = wait_util(driver,By.ID,'grmtr_transferringtocsnhighschool_name',20)
        grmtr_transferringtocsnhighschool = driver.find_element(By.ID, "grmtr_transferringtocsnhighschool")
        grmtr_transferringtocsnhighschool_entityname = driver.find_element(By.ID,
                                                                           "grmtr_transferringtocsnhighschool_entityname")
        driver.execute_script(f"arguments[0].value='Art & Design';", grmtr_transferringtocsnhighschool_name)
        driver.execute_script(f"arguments[0].value='3d03fde8-367c-ed11-81ad-0022481d6cbe';",
                              grmtr_transferringtocsnhighschool)
        driver.execute_script(f"arguments[0].value='mshied_programversion';",
                              grmtr_transferringtocsnhighschool_entityname)
        driver.find_element(By.ID, 'CustomNext').click()
        time.sleep(5)

        wait_util(driver, By.ID, 'foundry_submitdetailsonyoureducation', 20).click()
        driver.find_element(By.ID, 'grmtr_certifytrueinformation').click()
        driver.find_element(By.ID, 'grmtr_accuratemailingaddress').click()
        driver.find_element(By.ID, 'grmtr_studentsignature').send_keys(first_name + ' ' + last_name)
        driver.find_element(By.ID, 'grmtr_certifyage_1').click()

        driver.find_element(By.ID, 'CustomNext').click()
        time.sleep(5)
        driver.find_element(By.ID, 'CustomNext').click()
        time.sleep(5)
        data_insert = (first_name, last_name, cell, addr_name, city, state_country, postal_code, email_id, status)
        print(data_insert)
        cur.execute(str_insert, data_insert)
        conn.commit()
        return 'success'

    except Exception as e:

        status = 'FAILED'
        data_insert = (first_name, last_name, cell, addr_name, city, state_country, postal_code, email_id, status)
        print(data_insert)
        cur.execute(str_insert, data_insert)
        conn.commit()
        print("=========== BEGIN ===========")
        print(traceback.format_exc())
        print(email)
        print(user)
        print("=========== END ===========")
        return 'ERROR'
    finally:
        driver.close()



if __name__ == '__main__':
    str_SELECT = "SELECT e.id, e.username, e.passw from EMAIL e where e.id not in (SELECT email_id from edu_csn) "
    cur.execute(str_SELECT)
    Row = namedtuple('Row', [desc[0] for desc in cur.description])
    # Fetch the data and convert it to named tuples
    rows = [Row(*row) for row in cur.fetchall()]
    users = get_name_generator(rows.__len__())
    lst_addr = get_addr()
    print(lst_addr)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks to the pool
        futures = [
            executor.submit(run, email=rows[i], user=users[i], addr=lst_addr[random.randrange(0, lst_addr.__len__())])
            for i in range(len(rows))]

        # Wait for tasks to complete
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print("result: " + result)
    # for i in range(len(rows)):
    #     run(email=rows[i], user=users[i], addr=addr)
    # conn.commit()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
