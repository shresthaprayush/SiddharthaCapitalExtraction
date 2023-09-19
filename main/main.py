import os.path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pytesseract

import cv2

def exportToExcle(data,clientName,boid,availableLimit,sno):
    symbol = []
    cdsFreeBalance = []

    for d in data:
        symbol.append(d[1])
        cdsFreeBalance.append(d[3])

    mainDictironary = {
        'S.No': sno,
        'Client Name': clientName,
        'BO ID': boid,
        'Stock Symbol': symbol,
        'CDS Free Balance': cdsFreeBalance,
        'Available Trading Limit': availableLimit,
    }

    df = pd.DataFrame(mainDictironary)
    df.to_csv('output.csv')

    my_index_cols = ['S.No', 'Client Name', 'Available Trading Limit',
                     'Stock Symbol']  # this can also be a list of multiple columns
    df.set_index(my_index_cols).to_excel('extractionResults.xlsx', index=True)


def getCaptchaText():
    image_bw = cv2.imread('sc.png', 0)

    noiseless_image_bw = cv2.fastNlMeansDenoising(image_bw, None, 20, 7, 21)

    cv2.imwrite("../images/scnoisereomoved.jpg", noiseless_image_bw)
    image_bw2 = cv2.imread('../images/scnoisereomoved.jpg', 0)

    noiseless_image_bw2 = cv2.fastNlMeansDenoising(image_bw2, None, 20, 7, 21)
    cv2.imwrite("../images/scnoisereomoved2.jpg", noiseless_image_bw2)

    image = cv2.imread('../images/scnoisereomoved2.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
    bg = cv2.morphologyEx(image, cv2.MORPH_DILATE, se)
    out_gray = cv2.divide(image, bg, scale=255)
    out_binary = cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU)[1]

    cv2.imwrite('../images/scnoisereomoved3.jpg', out_binary)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    image = cv2.imread("../images/scnoisereomoved3.jpg", cv2.IMREAD_GRAYSCALE)
    cv2.dilate(image, (5, 5), image)
    extractedText = pytesseract.image_to_string(image)
    print(f'{extractedText}')
    return extractedText

def main():

    global myInformationBlock
    loginPath = 'login'
    dpHolding = 'tms/me/dp-holding'

    credentialDataFrame = pd.read_csv('../credentialfile/credentials.csv')
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(options=options)

    for index,cD in credentialDataFrame.iterrows():
        print(cD)
        username = cD['username']
        password = cD['password']
        url = cD['url']

        loingUrl = os.path.join(url,loginPath)
        driver.get(loingUrl)
        time.sleep(2)

        userNameInputBox = driver.find_element(By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "ng-invalid", " " ))]')
        passwordInputBox = driver.find_element(By.XPATH,'//*[(@id = "password-field")]')
        captchaBox = driver.find_element(By.XPATH,'//*[(@id = "captchaEnter")]')
        submitButton = driver.find_element(By.XPATH,'/html/body/app-root/app-login/div/div/div[2]/form/div[4]/input')
        captchaImage = driver.find_element(By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "captcha-image-dimension", " " ))]')
        userNameInputBox.send_keys(username)
        captchaSuccess = False

        captchaImage.screenshot('sc.png')
        captchaText = getCaptchaText()


        while not captchaSuccess:
            captchaImage.screenshot('sc.png')
            captchaText = getCaptchaText()
            passwordInputBox.send_keys(password)
            captchaBox.send_keys(captchaText)
            time.sleep(5)
            try:
                myInformationBlock = driver.find_element(By.XPATH,'/html/body/app-root/tms/app-menubar/aside/nav/ul/li[3]/a')
                captchaSuccess = True
                break
            except Exception as e:
                print('Error')
                captchaSuccess = False

        # submitButton.click()

        # #MyInformation
        # myInformationBlock = driver.find_element(By.XPATH,'/html/body/app-root/tms/app-menubar/aside/nav/ul/li[3]/a')
        myInformationBlock.click()
        time.sleep(5)

        nameBlock = driver.find_element(By.XPATH,'/html/body/app-root/tms/main/div/div/app-tms-member-admin/app-client-search2/div[2]/div/div[2]/app-client-search-general/div[1]/div')
        boidBlock = driver.find_element(By.XPATH,'/html/body/app-root/tms/main/div/div/app-tms-member-admin/app-client-search2/div[2]/div/div[2]/app-client-search-general/div[2]/div[2]/ul/li[3]/span')
        tradingLimitBlock  = driver.find_element(By.XPATH,'/html/body/app-root/tms/main/div/div/app-tms-member-admin/app-client-search2/div[2]/div/div[2]/app-client-search-general/div[4]/div/div/div[2]/div[1]/table/tbody/tr[1]/td')

        name = nameBlock.text
        boid = boidBlock.text
        tradingLimit = tradingLimitBlock.text

        #DP Holding
        holdingUrl = os.path.join(url,dpHolding)
        driver.get(holdingUrl)
        time.sleep(5)

        tableBody = driver.find_element(By.XPATH,'/html/body/app-root/tms/main/div/div/app-dp-holding/div/div/kendo-grid/div/kendo-grid-list/div/div[1]/table/tbody')
        tableRows = tableBody.find_elements(By.TAG_NAME,'tr')
        tableRowsArray = []
        for tr in tableRows:
            tableDataArray = []
            tableData = tr.find_elements(By.TAG_NAME,'td')
            for td in tableData:
                tableDataArray.append(td.text)
                print(td.text)
            tableRowsArray.append(tableDataArray)
        print(tableRowsArray)

        exportToExcle(tableRowsArray,name,boid,tradingLimit,1)


main()