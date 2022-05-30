import time
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findSalePluse.settings')
django.setup()
from items.models import SaleProduct
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()



def find_element_percent(driver):
    time.sleep(2.0)
    element_xpath_value = "//*[@id='main-content']/div/div[3]/div/div/div/div[1]/div"
    items_page = driver.find_element(by=By.XPATH, value=element_xpath_value)
    item_list = items_page.find_elements(by=By.CLASS_NAME, value="grid-item")
    counter = 0
    list_of_items=[]
    result_dict = {}
    result_dict_key_counter = 0
    for item in item_list:
        item_span = None
        counter += 1
        try:
            item_span = item.find_element(by=By.XPATH, value=".//div/div/div/div/div/div/div/a[2]/div/span").text
        except:
            print('item doesn\'t have span percent tag')

        try:
            if int(item_span[1:3]) >= 30:
                # link_of_product
                link = item.find_element(by=By.XPATH, value=".//div/div/div/div/div/div/div/a[1]").get_attribute('href')
                # print(link)

                # product_name
                name = item.find_element(by=By.XPATH, value=".//div/div/div/div/div/div/a/div/p[1]").text
                # print(name)

                # product_price
                price = item.find_element(by=By.XPATH,
                                          value=".//a[@class = 'product-card-content-badges-wrapper___2brrU']/div[2]/div/div[1]").text
                # print(price)

                # product_price_on_sale
                price_on_sale = item.find_element(by=By.XPATH,
                                                  value=".//a[@class = 'product-card-content-badges-wrapper___2brrU']/div[2]/div/div[2]").text
                # print(price_on_sale)
                obj=SaleProduct(link=link,name=name,price=price,price_on_sale=price_on_sale)
                obj.save()
                # list_of_items.append(obj)
                item_dict = {"name": name, "price": price, "price_on_sale": price_on_sale}
                # result_dict_key_counter = result_dict_key_counter + 1
                result_dict[link] = item_dict
                # print(result_dict)
                # print(list_of_items)


        except:
            continue

        if counter % 3 == 0:
            driver.execute_script("arguments[0].scrollIntoView(true);", item)
            time.sleep(1.0)

    else:
        print(result_dict)
        return result_dict


def run_driver(driver):
    target_url = "https://www.adidas.com.tr/tr/outlet"

    try:
        driver.get(target_url)
        uselessWindows = driver.window_handles
        result = find_element_percent(driver)
        return result

    except TimeoutException:
        print("loading took too much time,try again...")
        time.sleep(2.0)
        driver.get(target_url)


run_driver(driver)