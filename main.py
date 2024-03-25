from selenium import webdriver
import urllib.parse
import time
import random
import pandas as pd
from string import Template
import re

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument(f'--user-data-dir=./session/')
driver = webdriver.Chrome(options=options)

def autenticate():
    driver.get("https://web.whatsapp.com/")
    while len(driver.find_elements(By.ID, "side")) == 0:
        time.sleep(1)

def send_message_to_phone(phone, message):
    message = urllib.parse.quote(message)
    driver.get(f"https://web.whatsapp.com/send?phone={phone}&text={message}")

    while len(driver.find_elements(By.ID, "side")) == 0:
        time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]').send_keys(Keys.ENTER)
    time.sleep(random.randint(7, 11))

def read_dataframe(filepath: str):
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    elif filepath.endswith(".xlsx") or filepath.endswith(".xls"):
        df = pd.read_excel(filepath)
    else:
        raise FileNotFoundError(f"Not Found: {filepath}")
    return df

def check_template(template: Template, columns):
    identifiers = template.get_identifiers()
    for identifier in identifiers:
        if identifier not in columns:
            raise KeyError(f"Não existe coluna para o identificador \"{identifier}\"")

def sanitize_phone_number(phone_number: str) -> str:
    pn = "".join([c for c in phone_number if re.match("[0-9]", c)])
    if re.fullmatch("9[0-9]{8}", pn):
        pn = f"5565{pn}"
    elif re.fullmatch("[0-9]{2}9[0-9]{8}", pn):
        pn = f"55{pn}"
    elif re.fullmatch("[0-9]{4}9[0-9]{8}", pn):
        pass
    else:
        raise RuntimeError(f"O número {pn} está em um formato não reconhecido. "
                           "Por favor use 9xxxx-xxxx, yy 9xxxx-xxxx ou zz yy 9xxxx-xxxx"
                           "zz = código do país e yy = ddd")
    return pn

def send_message(template_text: str, contacts_df: pd.DataFrame):
    template = Template(template_text)

    # Verify whether the template is correct
    check_template(template, contacts_df.columns().to_list())

    for i, row in contacts_df.iterrows():
        text = template.substitute(**row.to_dict())
        phone_number = sanitize_phone_number(row["phone_number"])
        send_message_to_phone(phone_number, text)


if __name__ == "__main__":
    contacts_df = read_dataframe("test.csv")
    text = "$nome, bom dia.\n Você precisa fazer a matrícula até o dia $data"

# assert sanitize_phone_number("90000-9283") == "5565900009283"
# assert sanitize_phone_number("(76) 90000-9283") == "5576900009283"
# assert sanitize_phone_number("+99 (22) 90000-9283") == "9922900009283"
# assert sanitize_phone_number("+99(22)90000-9283") == "9922900009283"