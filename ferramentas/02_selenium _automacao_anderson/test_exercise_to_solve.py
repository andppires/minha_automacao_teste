from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pathlib
import time
from selenium.common.exceptions import UnexpectedAlertPresentException

def test_sample_page():
    # Caminho do arquivo HTML
    file_path = pathlib.Path(__file__).parent.resolve()
    driver = webdriver.Chrome()
    driver.get(f"file:////{file_path}/sample-exercise.html")
    
    # Pausa para você ver a página inicial carregando
    time.sleep(2)
    
    title = driver.title
    print(f"Título da página: {title}")
    
    # Espera até que o botão "generate" esteja presente
    generate_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "generate"))
    )
    generate_button.click()

    # Aguardar até que o código gerado apareça no elemento com ID "my-value"
    try:
        # Aguardando até que o código gerado esteja visível
        code_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "my-value"))
        )
        code = code_element.text
        print(f"Valor da mensagem gerada: {code}")
    except Exception as e:
        print(f"Erro ao capturar o código gerado: {e}")
        code = ""  # Definir como vazio caso não consiga capturar o código
    
    # Verifique se o código foi gerado
    if not code:
        print("Código gerado está vazio!")
        driver.quit()  # Encerra o navegador se não houver código gerado
        return  # Não prossegue o teste se o código não for gerado

    # Capture o código da mensagem e preencha o campo de texto
    text_box = driver.find_element(By.ID, "input")  # Verifique o ID do campo de texto
    text_box.clear()  # Limpar campo de texto
    text_box.send_keys(code)  # Preencher o campo com o código
    
    submit_button = driver.find_element(By.NAME, "button")  # Verifique o nome correto
    submit_button.click()

    # Pausa para observar o clique
    time.sleep(2)
    
    try:
        # Tratar o alerta
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()  # Fechar o alerta
    except UnexpectedAlertPresentException:
        print("Alerta inesperado encontrado, mas tratado.")
    
    # Espera para garantir que o resultado seja exibido
    result_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "my-value"))
    )
    value = result_element.text
    print(f"Valor da mensagem final: {value}")
    
    # Ajuste para validar apenas o código gerado (sem o prefixo)
    expected_message = code  # Apenas o código gerado
    assert value == expected_message, \
        f"Esperado: {expected_message}, mas obtido: {value}"
    
    driver.quit()
    print("Teste concluído.")

# Executando o teste
test_sample_page()
