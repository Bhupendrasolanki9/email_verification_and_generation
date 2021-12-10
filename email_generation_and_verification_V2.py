import pandas as pd
import dns.resolver
import re
import socket
import smtplib
import pandas as pd
from collections import OrderedDict
import datetime
from emailverifier import Client
from emailverifier import exceptions
from validate_email import validate_email


def email(company_input,name):
    pattern1 = []
    pattern2 = []
    pattern3 = []
    fnames = []
    lnames = []
    
    # if specialty in positions:
    # for name in names:
    fname = name.split(' ')[0]
    lname = name.split(' ')[1]
    fnames.append(fname)
    lnames.append(lname)

    df = pd.read_csv('domains.csv')
    company_names = df['Company']
    companies = df['Domains']
    domains = []
    
    for company_name,company in zip(company_names,companies):
        if company_input == company_name: 
            domains.append(company)
    
    if len(domains) >1:
        domains = list(OrderedDict.fromkeys(domains))    
        print(domains)
        count = 0
        for fname,lname in zip(fnames,lnames):
            lname = lname.replace('(','')
            lname = lname.replace(')','')
            p1 = fname+'.'+lname+'@'+domains[0]
            p2 = fname+'_'+lname+'@'+domains[0]
            p3 = fname+lname+'@'+domains[0]
            pattern1.append(p1)
            pattern2.append(p2)
            pattern3.append(p3)

            p1 = fname+'.'+lname+'@'+domains[1]
            p2 = fname+'_'+lname+'@'+domains[1]
            p3 = fname+lname+'@'+domains[1]
            pattern1.append(p1)
            pattern2.append(p2)
            pattern3.append(p3)
        
    elif len(domains)==1:
        domain = ' '.join(map(str, domains))
        for fname,lname in zip(fnames,lnames):
            lname = lname.replace('(','')
            lname = lname.replace(')','')
            p1 = fname+'.'+lname+'@'+domain
            p2 = fname+'_'+lname+'@'+domain
            p3 = fname+lname+'@'+domain
            pattern1.append(p1)
            pattern2.append(p2)
            pattern3.append(p3)
    
    return pattern1,pattern2,pattern3

def email_verification1(pattern,name,specialty,client,company_input,filename):    
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1
    resolver.lifetime = 1
    # Address used for SMTP MAIL FROM command  
    valid_emails = []
    person_name = []
    specialty_name = []
    for email_address1,email_address2,email_address3 in zip(pattern[0],pattern[1],pattern[2]):
        email_address1 = email_address1.replace('(','')
        email_address1 = email_address1.replace(')','')
        try:
            is_valid1= validate_email(
            email_address=email_address1,
            check_format=True,
            check_blacklist=True,
            check_dns=True,
            dns_timeout=10,
            check_smtp=True,
            smtp_timeout=10,
            smtp_helo_host='my.host.name',
            smtp_from_address='my@from.addr.ess',
            smtp_skip_tls=False,
            smtp_tls_context=None,
            smtp_debug=False)
            if is_valid1 == True:
                print(is_valid1)
                valid_emails.append(email_address1)
                person_name.append(name)
                specialty_name.append(specialty)
                return valid_emails,person_name,specialty_name
            elif is_valid1 == False:
                is_valid2= validate_email(
                email_address=email_address2,
                check_format=True,
                check_blacklist=True,
                check_dns=True,
                dns_timeout=10,
                check_smtp=True,
                smtp_timeout=10,
                smtp_helo_host='my.host.name',
                smtp_from_address='my@from.addr.ess',
                smtp_skip_tls=False,
                smtp_tls_context=None,
                smtp_debug=False)
                if is_valid2 == True:
                    print(is_valid2)
                    valid_emails.append(email_address2)
                    person_name.append(name)
                    specialty_name.append(specialty)
                    return valid_emails,person_name,specialty_name
            elif is_valid2 == False:
                
                is_valid3= validate_email(
                email_address=email_address3,
                check_format=True,
                check_blacklist=True,
                check_dns=True,
                dns_timeout=10,
                check_smtp=True,
                smtp_timeout=10,
                smtp_helo_host='my.host.name',
                smtp_from_address='my@from.addr.ess',
                smtp_skip_tls=False,
                smtp_tls_context=None,
                smtp_debug=False)
                if is_valid3 == True:
                    print(is_valid3)
                    valid_emails.append(email_address3)
                    person_name.append(name)
                    specialty_name.append(specialty)
                    return valid_emails,person_name,specialty_name
                
        # If you get here, it means service returned HTTP error code
        except exceptions.HttpException:
            continue

        # If you get here, it means you cannot connect to the service
        except exceptions.GeneralException:
            continue

        # If you get here, it means you forgot to specify the API key
        except exceptions.UndefinedVariableException:
            continue

        # If you get here, it means you specified invalid argument
        # (options should be a dictionary)
        except exceptions.InvalidArgumentException:
            continue

        except:
            continue

        
    # return valid_emails,person_name,specialty_name

    
def dataStore(emails,company_input,filename):
    try:
        for email,name,specialty in zip(emails[0],emails[1],emails[2]):
            data = {
                "Name":name,
                "Company Name":company_input,
                "Specialty":specialty,
                "Email":email
                }
            f = pd.DataFrame([data])
            f.to_csv(filename,index=True,mode='a',header=False)
    except:
        pass

def main():
    client = Client('at_XNf3hXDaRsa0PfIgS4oCCTSZsAtDA')
    company_input = "Abbott"
    filename = datetime.date.today().strftime('%Y%m%d')+"Test_Perfect_Emails.csv"
    f = pd.DataFrame(columns=['Full Name','Company Name','Specialty','Email'])
    f.to_csv(filename,index=True,header=True)
    
    # specialties = ['Cardiovascular','CNS','Critical Care','Dermatology','Diabetes','Endocrinology','ENT','Gastroenterology','Haematology','Immunology','Implants','Infectious diseases','Inflammation','Internal diseases','Metabolic diseases','Nephrology','Neurology','Oncology','Ophthalmology','Orthopaedics','Osteoporosis','Pain management','Primary Care','Psychiatry','Pulmonology','Respiratory','Rheumatology','Surgery','THERAPEUTICS','Thrombosis','Urology','Vaccines']

    # final_file = datetime.date.today().strftime('%Y%m%d')+"Linkedin_Searched_Data.csv"
    final_file = "20211207Linkedin_Searched_Data.csv"
    df = pd.read_csv(final_file)
    names = df['Name']
    print(names)
    positions = df['Job Positions']
    specialties= df['Speciality']  
    specialties = specialties.fillna('None')
    positions =positions.dropna()
    # specialty = "NONE"
    for name,specialty,position in zip(names,specialties,positions):
        pattern = email(company_input,name)
        emails = email_verification1(pattern,name,specialty,client,company_input,filename)
        dataStore(emails,company_input,filename)

main()

    
