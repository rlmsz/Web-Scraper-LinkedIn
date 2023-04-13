import csv
from datetime import datetime

import data as data
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
import json
import re


path = r"C:\Users\rober\Desktop\chromedriver"
s = Service(path)
driver = webdriver.Chrome(service=s)

wait = WebDriverWait(driver, 10)
driver.get(
    "https://www.linkedin.com/jobs/search?location=Brazil&geoId=106057199&%2525253FcurrentJobId=3541779839&f_I=80&f_JT=F%2CI&currentJobId=3537496518&position=1&pageNum=0")

i = 2
while i <= (50):
    # Ir até o final da pagina
    print(i)
    i = i + 1
    print(i)
    time.sleep(2)
    try:
        # Clicar para carregar mais resultados
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        infinite_scroller_button = driver.find_element(By.XPATH, ".//button[@aria-label='Ver mais vagas']")
        infinite_scroller_button.click()
    except:
        pass

# Listar todas as vagas
job_lists = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
jobs = job_lists.find_elements(By.TAG_NAME, "li")  # return a list
print(len(jobs))

for job in jobs:
    pass

# Faz o backup de dados anteriores
try:
    salvar = open('data.json')
    dados = json.load(salvar)
    experiencia_lista = dados['Nível de experiência']
    tipo_lista = dados['Tipo de contratação']
    candidaturas_lista = dados['Número de candidaturas para vaga']
    linkcandidaturas_lista = dados['URL da candidatura']
    funcionariosempresa_lista = dados['Número de funcionários da empresa']
    seguidoresempresa_lista = dados['Número de seguidores da empresa']
    sedeempresa_lista = dados['Local sede da empresa']
    empresa_link_lista = dados['URL da empresa contratante']
    vaga_nome_lista = dados['Nome da vaga']
    empresa_nome_lista = dados['Nome da empresa contratante']
    data_lista = dados['Data da postagem da vaga']
    vaga_link_lista = dados['URL da vaga no linkedin']
    horario_scraping_lista = dados['Horário do scraping']
    contador = dados["Contador"]
# Se nao existirem, cria-se as listas
except:
    experiencia_lista = []
    tipo_lista = []
    candidaturas_lista = []
    linkcandidaturas_lista = []
    funcionariosempresa_lista = []
    seguidoresempresa_lista = []
    sedeempresa_lista = []
    empresa_link_lista = []
    contador = [0]
    vaga_nome_lista = []
    empresa_nome_lista = []
    data_lista = []
    vaga_link_lista = []
    horario_scraping_lista = []

print(contador)
# Conseguir o Resto dos dados
for item in range(max(contador), len(jobs)):
    # Clicar nos Detalhes
    try:
        print("Scraping...")
        job_click_path = f'/html/body/div/div/main/section/ul/li[{item + 1}]'
        job_click = job.find_element(By.XPATH, job_click_path).click()
    except:
        print("erro")
        pass
    time.sleep(3.5)
    # Conseguir o Nome
    driver.implicitly_wait(7)
    vaganome_path = '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2'
    vaga_nome = job.find_element(By.XPATH, vaganome_path).get_attribute("innerText")
    vaga_nome_lista.append(vaga_nome)
    # Conseguir Data
    driver.implicitly_wait(7)
    datavaga_path = '/html/body/div[1]/div/main/section/ul/li[' + str(1+item) + ']/div/div[2]/div/time'
    datavaga = job.find_element(By.XPATH, datavaga_path).get_attribute("datetime")
    data_lista.append(datavaga)
    # Conseguir Vaga Link
    driver.implicitly_wait(7)
    vaga_link_path = '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a'
    vaga_link = job.find_element(By.XPATH, vaga_link_path).get_attribute("href")
    vaga_link_lista.append(vaga_link)
    # horario scraping
    driver.implicitly_wait(7)
    horario_scraping = datetime.now()
    horario_scraping_lista.append(horario_scraping)
    # Nome da Empresa
    driver.implicitly_wait(7)
    empresa_path = '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a'
    empresa_nome = job.find_element(By.XPATH, empresa_path).get_attribute("innerText")
    empresa_nome_lista.append(empresa_nome)
    # Conseguir o nivel de experiencia
    experiencia_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span'
    try:
        experiencia = job.find_element(By.XPATH, experiencia_path).get_attribute('innerText')
        print(experiencia)
        experiencia_lista.append(experiencia.strip())
    except:
        experiencia_lista.append(None)
        pass

    # Conseguir o tipo de vaga
    tipo_path = '/html/body/div/div/section/div/div/section/div/ul/li[2]/span'
    try:
        tipo = job.find_element(By.XPATH, tipo_path).get_attribute('innerText')
        tipo_lista.append(tipo.strip())
        print(tipo)
    except:
        tipo_lista.append(None)
        pass

    # Conseguir o link da empresa
    empresa_link_path = '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a'
    try:
        empresa_link = job.find_element(By.XPATH, empresa_link_path).get_attribute('href')
        empresa_link_lista.append(empresa_link)
    except:
        empresa_link_lista.append(None)
        pass

    # Conseguir a quantidade de Candidaturas
    candidaturas_path = '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[2]'
    try:
        candidaturas = job.find_element(By.XPATH, candidaturas_path).get_attribute('innerText')
        driver.implicitly_wait(7)
        candidaturas_lista.append(candidaturas)
        print(candidaturas)
    except:
        try:
            candidaturas_path = '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/figure/figcaption'
            driver.implicitly_wait(7)
            candidaturas = job.find_element(By.XPATH, candidaturas_path).get_attribute('innerText')
            candidaturas_lista.append(candidaturas)
            print(candidaturas)
        except:
            print("Erro Candidaturas")
            candidaturas_lista.append(None)
    pass

    # Conseguir os detalhes da empresa
    ignorarempresa_path = '/html/body/div[4]/div/div/section/button'
    sedeempresa_path = '/html/body/main/section[1]/div/section[1]/div/dl/div[4]/dd'
    funcionariosempresa_path = '/html/body/main/section[1]/div/section[1]/div/dl/div[3]/dd'
    seguidoresempresa_path = '/html/body/main/section[1]/section/div/div[2]/div[1]/h3'

    try:
        empresa_link = job.find_element(By.XPATH, empresa_link_path)
        empresa_link.click()
        driver.switch_to.window(driver.window_handles[1])
        try:
            ignoraempresa = driver.find_element(By.XPATH, ignorarempresa_path)
            ignoraempresa.click()
            try:
                sede_empresa = driver.find_element(By.XPATH, sedeempresa_path).get_attribute('innerText')
                print(sede_empresa)
                sedeempresa_lista.append(sede_empresa)
            except:
                sedeempresa_lista.append(None)
                print("ErroSede")
            try:
                funcionarios_empresa = driver.find_element(By.XPATH, funcionariosempresa_path).get_attribute(
                    'innerText')
                print(funcionarios_empresa)
                funcionariosempresa_lista.append(funcionarios_empresa)
            except:
                funcionariosempresa_lista.append(None)
                print("ErroFuncionarios")
            try:
                driver.implicitly_wait(2)
                seguidoresempresa = driver.find_element(By.TAG_NAME, 'h3').text
                seguidoresempresa_lista.append(re.sub("[^0-9]", "", seguidoresempresa))
                seguidoresempresa = re.sub("[^0-9]", "", seguidoresempresa)
            except:
                seguidoresempresa_lista.append(None)
                print("ErroSeguidores")
        except:
            try:
                try:
                    sede_empresa = driver.find_element(By.XPATH, sedeempresa_path).get_attribute('innerText')
                    sedeempresa_lista.append(sede_empresa)
                except:
                    sedeempresa_lista.append(None)
                    print("ErroSede")
                try:
                    funcionarios_empresa = driver.find_element(By.XPATH, funcionariosempresa_path).get_attribute(
                        'innerText')
                    funcionariosempresa_lista.append(funcionarios_empresa)
                except:
                    funcionariosempresa_lista.append(None)
                    print("ErroFuncionarios")
                try:
                    time.sleep(2)
                    seguidoresempresa = driver.find_element(By.TAG_NAME, 'h3').text
                    seguidoresempresa = re.sub("[^0-9]", "", seguidoresempresa)
                    seguidoresempresa_lista.append(re.sub("[^0-9]", "", seguidoresempresa))
                except:
                    seguidoresempresa_lista.append(None)
                    print("ErroSeguidores")
            except:
                print("Erro")
                pass
            pass
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)
    except:
        sedeempresa_lista.append(None)
        funcionariosempresa_lista.append(None)
        seguidoresempresa_lista.append(None)
        print("Erro detalhes empresa")
        pass

    # Conseguir o Link das Candidaturas

    linkcandidaturas_path = '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/div/button[1]'
    ignorar_path = '//*[@id="sign-up-modal"]/div/section/header/button'
    try:
        linkcandidaturas = job.find_element(By.XPATH, linkcandidaturas_path)
        linkcandidaturas.click()
        driver.implicitly_wait(2)
        ignorar = job.find_element(By.XPATH, ignorar_path)
        ignorar.click()
        driver.switch_to.window(driver.window_handles[1])
        driver.implicitly_wait(2)
        link = driver.current_url
        print(driver.current_url)
        linkcandidaturas_lista.append(driver.current_url)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.implicitly_wait(2)
    except:
        print("Erro Numero Candidaturas")
        linkcandidaturas_lista.append(None)
        pass

    # Fazer o backup dos dados
    contador.append(1 + item)
    keys = (
        'Contador', 'URL da vaga no linkedin', 'Nome da vaga', 'Nome da empresa contratante',
        'URL da empresa contratante',
        'Modelo de contratação', 'Tipo de contratação', 'Nível de experiência', 'Número de candidaturas para vaga',
        'Data da postagem da vaga', 'Horário do scraping', 'Número de funcionários da empresa',
        'Número de seguidores da empresa', 'Local sede da empresa', 'URL da candidatura')
    values = (
        contador, vaga_link_lista, vaga_nome_lista, empresa_nome_lista, empresa_link_lista, None, tipo_lista,
        experiencia_lista,
        candidaturas_lista, data_lista, horario_scraping_lista, funcionariosempresa_lista, seguidoresempresa_lista,
        sedeempresa_lista, linkcandidaturas_lista)
    salvar = dict(zip(keys, values))
    backup = open("data.json", "w")

    backup.write(json.dumps(salvar, indent=4, sort_keys=True, default=str))
    backup.close()

print("fim")
driver.quit()

# Fazer a Tabela CSV
job_data = pd.DataFrame({
    'URL da vaga no linkedin': vaga_link_lista,
    'Nome da vaga': vaga_nome_lista,
    'Nome da empresa contratante': empresa_nome_lista,
    'URL da empresa contratante': empresa_link_lista,
    'Modelo de contratação': None,
    'Tipo de contratação': tipo_lista,
    'Nível de experiência': experiencia_lista,
    'Número de candidaturas para vaga': candidaturas_lista,
    'Data da postagem da vaga': data_lista,
    'Horário do scraping': horario_scraping_lista,
    'Número de funcionários da empresa': funcionariosempresa_lista,
    'Número de seguidores da empresa': seguidoresempresa_lista,
    'Local sede da empresa': sedeempresa_lista,
    'URL da candidatura': linkcandidaturas_lista
})

job_data.to_csv("Scraping-Roberto Lucas Morais de Souza.csv", encoding='utf-8', index=False)
exit()
