

from loopers import loop
from verify_email import verify_email
import re
import requests

def get_email_from_loopers(url):
    return list(set(list(loop(url).values())[0]['emails']))

def get_valided_emails(emails):
    verify_emails_list = []
    for email in emails:
        if verify_email(email):
            verify_emails_list.append(email)
    print(verify_emails_list)

def get_status_of_url(contact_url):
    return requests.get(contact_url,timeout=5,verify=False).status_code

def get_contact_urls(url):

    contact_sub_domain_list = [
        'contact','contactus','contacts','contact-us','contact-us.php','contactus.php','contact.php','contactus.html','about-us','aboutus'
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

if __name__=='__main__':
    url='https://www.vmokshagroup.com/'
    # emails = get_email_from_loopers(url)
    # print(emails)
    # get_valided_emails(emails)

    # get_contact_urls(url)
    # print(get_status_of_url(url))
    print(get_contact_urls(url))