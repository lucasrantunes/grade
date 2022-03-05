from django.core.management.base import BaseCommand, CommandError
from avalible_classes.models import Curso

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser

class Command(BaseCommand):
    help = 'Update cursos database'

    def get_user_data(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        user = dict()
        user = config["utfpr_login"]["user"]
        password = config["utfpr_login"]["password"]

        return user, password

    def utfpr_login(self, driver, user, password):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@formcontrolname="username"]'))
            )
            return False
        finally:
            user_element = driver.find_element(by=By.XPATH, value='//input[@formcontrolname="username"]')
            password_element = driver.find_element(by=By.XPATH, value='//input[@formcontrolname="password"]')
            button_element = driver.find_element(by=By.XPATH, value='//button[@label="Login"]')

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
                return True

    def get_classes_lines(self, driver):
        classes_table = driver.find_element(by=By.XPATH, value='//table[@border="1"]')
        classes_lines = classes_table.find_elements(by=By.XPATH, value='.//tr')
        return classes_lines

    def print_classes(self, classes_lines):
        class_id = 0
        for line in classes_lines:
            line_columns = line.find_elements(by=By.XPATH, value='.//td')
            first_column = line_columns[0].text
            if "semanais" in first_column:
                class_id += 1
                ## Remove (x Aulas semanais) from the first_column
                # nome = first_column[0:first_column.find("  ")]
                ## Get (x Aulas semanais) and return only the integer
                # aulas_semanais = int( nome[nome.find("(")+1:nome.find(")")].replace(" Aulas semanais", "") )
                #db.execute(f"INSERT INTO subject (name) VALUES ('{class_name}')")
                print(f"{first_column}")
                
            elif "Turma" in first_column:
                pass
            else:
                turma = line_columns[0].text
                planejamento = line_columns[1].text
                enquadramento = line_columns[2].text
                vagas_total = line_columns[3].text
                vagas_calouros = line_columns[4].text
                reserva = line_columns[5].text
                prioridade_curso = line_columns[7].text
                horario = line_columns[8].text
                professor = line_columns[9].text
                optativa = line_columns[10].text

                print(f"{class_id}) Turma: {turma}, Horário: {horario}, Professor: {professor}")

    def handle(self, *args, **options):
        user, password = self.get_user_data()
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        driver.get("https://sistemas2.utfpr.edu.br/dpls/sistema/aluno01/mpListaHorario.pcExibirTurmas?p_arquivoNomeVc=6AC2773AB60FB07DF3A806157360B06A")
        if self.utfpr_login(driver, user, password) == True:
            classes_lines = self.get_classes_lines(driver)
            self.print_classes(classes_lines)
        else:
            print("UTFPR Login Error.")
        