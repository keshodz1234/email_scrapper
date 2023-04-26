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

def get_valided_emails(emails):
    verify_emails_list = []
    if emails:
        for email in emails:
            if verify_email(email):
                verify_emails_list.append(email)
        return verify_emails_list
    else:
        return None
  

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

def get_all_emails_from_loopers(url):
    email_from_home = get_email_from_loopers(url)
    contact_url = get_contact_urls(url)
    print(contact_url)
    if contact_url:
        for url in contact_url:
            email_from_contact_url = get_email_from_loopers(url)
            # print(email_from_contact_url)
            if email_from_contact_url:
                break
        if email_from_home is not None and email_from_contact_url is not None:
            emails = list(set(email_from_home + email_from_contact_url))
        elif email_from_home is not None:
            emails = list(set(email_from_home))
        elif email_from_contact_url is not None:
            emails = list(set(email_from_contact_url))
        else:
            emails = None
        return emails
    else:
        return None

def get_all_emails_from_selenium(url):

    email_from_home = get_email_from_selenium_webdriver(url)
    contact_url = get_contact_urls(url)
    if contact_url:
        for url in contact_url:
            email_from_contact_url = get_email_from_selenium_webdriver(url)
            if email_from_contact_url:
                break
        if email_from_home is not None and email_from_contact_url is not None:
            emails = list(set(email_from_home + email_from_contact_url))
        elif email_from_home is not None:
            emails = list(set(email_from_home))
        elif email_from_contact_url is not None:
            emails = list(set(email_from_contact_url))
        else:
            emails = None
        return emails  
    else:
        return None

def get_valid_emails(emails):
    valid_emails = []
    unwanted_emails_string_reference_list =[
        'manateefamilydental', 'your@email.com', 'username', '.avi', '%', 'mail@mail.com', 'your@domain.com', '.JPG', '.webp', 'yourname', 'wixpress.com', 'domain', 'example', 'xxx@xxx', 'redbubble', '.jpg', '@mail', 'email@email.com', 'sentry.io', 'yourname@domain.com', 'test@test.com', '--', 'group.calendar.google.com', 'someone', 'woodandmyers.com', '.jff', 'email', 'yourmail', 'yourdomain', 'your', '.mp4', '.gif', '.png', 'service@domain.com', '.ico', 'sentry', '.jpeg'
    ]

    for email in emails:

        if all (unwanted_email_string_ref not in email for unwanted_email_string_ref in unwanted_emails_string_reference_list):
            if '@' in email:
                valid_emails.append(email)
        
    return valid_emails
    

def Email_Scrapper():
    # url='https://www.vmokshagroup.com/'
    # url = "https://usbiomag.com/"
    # url = "https://www.ancientrootsacu.com/" #selenium
    # url = "https://www.zentralabq.com" #***selenium
    url = "https://www.onpoint-acupuncture.com/" #***selenium

    # url = "https://www.rover.com/" #***
    # url = "https://gpcacupuncture.com/"
    url = "https://www.jadestaracupuncture.com/" #*** 
    url = "http://www.tucsonacupuncture.com/" #selenu

    # ===============Emails From Loopers===================
    emails = get_all_emails_from_loopers(url)

    if emails:
        return emails
    else:
        emails = get_all_emails_from_selenium(url)
        return emails
              

if __name__=='__main__':
    emails = Email_Scrapper()
    print(emails)
    if emails:
        valid_emails = get_valid_emails(emails)
        print(valid_emails)
    # validated_emails = get_valided_emails(emails)
    # print(f"valid emails {validated_emails}")
    
    
    