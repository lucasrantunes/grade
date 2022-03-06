from django.core.management.base import BaseCommand, CommandError
from avalible_classes.models import Curso, Disciplina, Turma

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser

class Command(BaseCommand):
    help = 'Update cursos database'

    def __get_user_data(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        user = dict()
        user = config["utfpr_login"]["user"]
        password = config["utfpr_login"]["password"]

        return user, password

    def __utfpr_login(self, driver, user, password):
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

    def __get_classes_lines(self, driver):
        classes_table = driver.find_element(by=By.XPATH, value='//table[@border="1"]')
        classes_lines = classes_table.find_elements(by=By.XPATH, value='.//tr')
        return classes_lines

    def __handle_classes(self, classes_lines):
        codigo_disciplina = 0
        for line in classes_lines:
            line_columns = line.find_elements(by=By.XPATH, value='.//td')
            first_column = line_columns[0].text
            if "semanais" in first_column:
                try:
                    codigo_disciplina = first_column[0:first_column.find(" ")]
                    ## Remove (x Aulas semanais) from the first_column
                    nome = first_column[first_column.find("- ")+2:first_column.find("  ")]
                    ## Get (x Aulas semanais) and return only the integer
                    aulas_semanais = int( first_column[first_column.find("(")+1:first_column.find(")")].replace(" Aulas semanais", "") )
                    self.__create_disciplina(codigo_disciplina, nome, aulas_semanais)
                except:
                    print(f"Disciplina {codigo_disciplina} não adicionada. (1)")
                    codigo_disciplina = 0
                    continue
            elif "Turma" in first_column:
                pass
            else:
                if codigo_disciplina != 0:
                    codigo_turma = line_columns[0].text
                    planejamento = line_columns[1].text
                    enquadramento = line_columns[1].text
                    vagas_total = int(line_columns[3].text)
                    vagas_calouros = int(line_columns[4].text)
                    reserva = line_columns[5].text
                    prioridade_curso = line_columns[7].text
                    horario = line_columns[8].text
                    professor = line_columns[9].text
                    optativa = line_columns[10].text

                    if "Presencial" in enquadramento:
                        enquadramento = 1
                    elif "remota" in enquadramento:
                        enquadramento = 3
                    else:
                        enquadramento = 2

                    self.__create_turma(codigo_disciplina, codigo_turma, planejamento, enquadramento, vagas_total,vagas_calouros, reserva, prioridade_curso, horario, professor, optativa)

    def __create_turma(self, codigo_disciplina, codigo_turma, planejamento, enquadramento, vagas_total, vagas_calouros, reserva, prioridade_curso, horario, professor, optativa):
        turma = Turma.objects.filter(codigo_disciplina=codigo_disciplina, codigo_turma=codigo_turma)
        if not turma:
            turma = Turma(codigo_disciplina=codigo_disciplina, codigo_turma=codigo_turma, enquadramento=enquadramento, vagas_total=vagas_total, vagas_calouros=vagas_calouros, reserva=reserva, prioridade_curso=prioridade_curso, horario=horario, professor=professor, optativa=optativa)
            turma.save()
        else:
            turma.codigo_disciplina = codigo_disciplina
            turma.codigo_turma = codigo_turma
            turma.planejamento = planejamento
            turma.enquadramento = enquadramento
            turma.vagas_total = vagas_total
            turma.vagas_calouros = vagas_calouros
            turma.reserva = reserva
            turma.prioridade_curso = prioridade_curso
            turma.horario = horario
            turma.professor = professor
            turma.optativa = optativa
            turma.save()
            print(f"Turma {codigo_turma} da {codigo_disciplina} foi atualizada.")

    def __create_disciplina(self, codigo_disciplina, nome, aulas_semanais):
        disciplina = Disciplina.objects.filter(codigo_disciplina=codigo_disciplina, nome=nome, aulas_semanais=aulas_semanais)
        if not disciplina:
            try:
                Disciplina(codigo_disciplina=codigo_disciplina, nome=nome, aulas_semanais=aulas_semanais).save()
            except:
                print(f"Disciplina {codigo_disciplina} não adicionada. (2)")
            

    def handle(self, *args, **options):
        user, password = self.__get_user_data()
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        driver.get("https://sistemas2.utfpr.edu.br/dpls/sistema/aluno01/mpListaHorario.pcExibirTurmas?p_arquivoNomeVc=6AC2773AB60FB07DF3A806157360B06A")
        if self.__utfpr_login(driver, user, password) == True:
            classes_lines = self.__get_classes_lines(driver)
            self.__handle_classes(classes_lines)
        else:
            print("UTFPR Login Error.")
        