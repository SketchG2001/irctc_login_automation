from flask import Flask, request, render_template, url_for, redirect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Initialize the Microsoft Edge browser
        options = webdriver.EdgeOptions()
        options.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'  # Replace with your Edge browser's path
        driver = webdriver.Edge(options=options)

        try:
            # Navigate to the IRCTC website
            driver.get("https://www.irctc.co.in/nget/train-search")

            # Click the login button to open the popup using the provided XPath
            login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/app-root/app-home/div[1]/app-header/div[2]/div[2]/div[1]/a[1]")))
            login_button.click()

            # it will open the new window tab (popup)
            driver.switch_to.window(driver.window_handles[-1])

            # Locate and interact with the login form elements (username and password fields)
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='userid']")))
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='password']")))

            # username and password
            username_field.send_keys(username)
            password_field.send_keys(password)

            # Locate and interact with the CAPTCHA input field by name
            captcha_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "captcha")))

            # Tesseract to extract text from the CAPTCHA image
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

            # Capture the CAPTCHA image
            captcha_image = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img[@class='captcha-img']")))
            captcha_image.screenshot("captcha.png")

            # Use Tesseract to extract tgext from the CAPTCHA image
            captcha_text = pytesseract.image_to_string(Image.open("captcha.png"))

            # Enter the CAPTCHA text into the form
            captcha_input.send_keys(captcha_text)

            # Locate and click the login submit button
            login_submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
            login_submit_button.click()

            # Waiting for the login to complete (customize the timeout as needed)
            WebDriverWait(driver, 100).until(EC.url_changes(driver.current_url))



        except Exception as e:
            print("An error occurred:", str(e))
        finally:
            # Close the browser window when done with everything
            driver.quit()
            return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')
@app.route('/index')
def home():
    # when driver close redirect to home
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

