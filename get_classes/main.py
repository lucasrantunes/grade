from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

driver.get("https://sistemas2.utfpr.edu.br/dpls/sistema/aluno01/mpListaHorario.pcExibirTurmas?p_arquivoNomeVc=6AC2773AB60FB07DF3A806157360B06A")


try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@formcontrolname="username"]'))
    )
finally:
    user_element = driver.find_element(by=By.XPATH, value='//input[@formcontrolname="username"]')
    password_element = driver.find_element(by=By.XPATH, value='//input[@formcontrolname="password"]')
    button_element = driver.find_element(by=By.XPATH, value='//button[@label="Login"]')

    user = ""
    password = ""

    user_element.click()
    user_element.send_keys(user)

    password_element.click()
    password_element.send_keys(password)

    button_element.click()

    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//table[@border="1"]'))
        )
    finally:
        classes_table = driver.find_element(by=By.XPATH, value='//table[@border="1"]')
        classes_table_html = classes_table.get_attribute('outerHTML')
        
        print(classes_table_html)