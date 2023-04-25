# ============== Packages =================

from loopers import loop
from verify_email import verify_email
import re
import requests
from driver import Driver

# =============== declaring functions =================
# =============== taking url main domain ==============

def get_email_from_loopers(url):

    loopers_dict_value = list(loop(url).values())
    

    if loopers_dict_value:
       
        emails_list  = loopers_dict_value[0]['emails']
       
    else:
        emails_list = None

    if emails_list is None:
        return None
    else:
        return list(set(emails_list))
    
# =============== verifing emails ======================
sdfd
def get_valided_emails(emails):
    verify_emails_list = []
    for email in emails:
        if verify_email(email):
            verify_emails_list.append(email)
    print(verify_emails_list)

# ================ checking url status ==================

def get_status_of_url(contact_url):
    try:
        statusCode =  requests.get(contact_url,timeout=5,verify=False).status_code
    except Exception as e:
        statusCode = 404
    return statusCode

def get_contact_urls(url):

    contact_sub_domain_list = [
       'contact-us-and-hours','contact','contactus','contacts','contact-us','contact-us.php','contactus.php','contact.php','contactus.html','about-us','aboutus','contact.html'
    ]

    contact_sub_domain_url = []
    regex = r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)"
    regex_home_url_object = re.finditer(regex,url)

    for url in regex_home_url_object:
        home_url = (str(url).split("='")[-1].replace("'>",""))
    
    for contact_sub_domain in contact_sub_domain_list:
        contact_url = f"{home_url}/{contact_sub_domain}"
        print(contact_url)

        response_status_code = get_status_of_url(contact_url)
        print(response_status_code)

        if response_status_code == 200 or response_status_code == 403:
            contact_sub_domain_url.append(contact_url)
    
    return contact_sub_domain_url

# =================== declaration of main function ===================
def get_page_source(url):

    driver = Driver()
    driver.get(url)
    page_source_txt = str(driver.page_source)
    driver.close()
    return page_source_txt

def get_email_from_selenium_webdriver(url):
    
    text = get_page_source(url)
    # print(text)

    email_regex = re.compile(r'''(
                [a-zA-Z0-9._%+-]+
                @
                [a-zA-Z0-9.-]+
                (\.[a-zA-Z]{2,4})
                )''', re.VERBOSE)       
    try:
        matches = set([groups[0] for groups in email_regex.findall(text)])
        return matches if matches else None
    except Exception as err:
        print(" {} \nFailed to read page!".format(err))
        return None

def Email_Scrapper():
    url='https://www.vmokshagroup.com/'
    # url = "https://usbiomag.com/"
    # url = "https://www.ancientrootsacu.com/" #selenium
    # url = "https://www.zentralabq.com" #***selenium
    # url = "https://www.onpoint-acupuncture.com/" #***selenium

    # url = "https://www.rover.com/" #***
    # url = "https://gpcacupuncture.com/"
    # url = "https://www.jadestaracupuncture.com/" #*** 
    # url = "http://www.tucsonacupuncture.com/" #selenu

    email = get_email_from_loopers(url)
   
    if email:
        
        return email
    
    if not email:
        email = get_email_from_selenium_webdriver(url)
        if email:
            return list(set(email))
        
    if not email:
        contact_url = get_contact_urls(url)
        for url in contact_url:
            email = get_email_from_loopers(url)
            if email:
                return email
            else:
                email = get_email_from_selenium_webdriver(url)
                if email:
                    return list(set(email))
                
if __name__=='__main__':
    emails = Email_Scrapper()
    print(emails)
    # emails = get_email_from_loopers(url)
    # print(emails)
    # get_valided_emails(emails)

    # get_contact_urls(url)
    # print(get_status_of_url(url))
    # print(get_contact_urls(url))