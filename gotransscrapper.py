def initSelenium(self):
    import os
    from selenium import webdriver

    DIR = os.path.dirname(os.path.abspath(__file__))

    path_to_phantomjs = DIR+'/phantomJS/bin/phantomjs' # change path as needed

    # hide phantomJS
    dcap = dict()
    dcap["phantomjs.page.settings.userAgent"] = (
         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
         "(KHTML, like Gecko) Chrome/15.0.87")

    self.browser = webdriver.PhantomJS(executable_path = path_to_phantomjs, desired_capabilities = dcap)

    url = "https://translate.google.de/?um=12&ie=UTF-8&hl=de&client=tw-ob#auto/"+self.tlang+"/"

    self.browser.get(url)


def getGoogleTranslationFromText(self, text):
    import time

    bet_fa = self.browser.find_element_by_id("source")
    bet_fa.clear()
    bet_fa.send_keys(text)
    
    # give google time to translate 
    time.sleep(.700)

    return self.browser.find_element_by_xpath('//*[@id="result_box"]/span').text
