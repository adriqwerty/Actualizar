from selenium import webdriver

driver = webdriver.Chrome()
driver.get(url)

html = driver.page_source
df = pd.read_html(html)[0]