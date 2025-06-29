"""Contains all the helper modules which required to run the Applied Valuation acceptance"""
import re
import json
import datetime
import logging
from pytz import timezone
import sender
import requests
import email
import base64
from bs4 import BeautifulSoup
# from scrapy.http import HtmlResponse
from stdlib.creds import email_cred
from datetime import date, timedelta
from stdlib.utility import cursorexec,ignored_message,exception_mail_send,client_mail_send,check_ordertype,criteria_with_params,zipcode_check,login_into_gmail
import html
import requests
from email.utils import parseaddr
from stdlib.test_utility import test_exception_mail_send

email_creds = email_cred()

class pcv:
    
    def __init__(self, client_data, portal_name):
        
        self.client_data = client_data
        self.portal_name = portal_name
        self.session = requests.Session()

    
    def checkorder_mail(self):
        try:
            conn = login_into_gmail('murcorpcv@gmail.com', 'ekmw pldz tdhw zkkp')
            conn.select('inboxx')
            retcode, data = conn.search(
                None,
                '(UNSEEN FROM "@pcvmurcor.com" OR SUBJECT "new BPO order from PCV Murcor" SUBJECT "Fee Quote Request on Order")'
            )

            print("The status is", retcode)
            str_list = list(filter(None, data[0].decode().split(' ')))
            logging.info('No: of unread messages Applied valuation: {}'.format(len(str_list)))
            unread_new_emails = {}  

            if retcode == 'OK':
                for num in data[0].decode().split(' '):
                    if num:
                        type, data = conn.fetch(num, '(RFC822)' )
                        for response_part in data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_string(response_part[1].decode('utf-8'))
                                # to_address = "littlerockbpo@bangrealty.com"
                                to_address =  msg['To']
                                mail_content = ""
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    
                                    if content_type == 'text/plain':
                                        mail_content += part.get_payload(decode=True).decode(part.get_content_charset())
                                    
                                    elif content_type == 'text/html':
                                        mail_content += part.get_payload(decode=True).decode(part.get_content_charset())
                                    
                                    elif content_type == 'multipart/alternative':
                                        
                                        for alternative_part in part.get_payload():
                                            
                                            if alternative_part.get_content_type() == 'text/plain':
                                                mail_content += alternative_part.get_payload(decode=True).decode(alternative_part.get_content_charset())
                                            
                                            elif alternative_part.get_content_type() == 'text/html':
                                                mail_content += alternative_part.get_payload(decode=True).decode(alternative_part.get_content_charset())
                                    
                                    elif content_type == 'multipart/mixed': 
                                    # or content_type == 'multipart/related':
                                        
                                        for mixed_part in part.get_payload():
                                            
                                            if mixed_part.get_content_type() == 'text/plain':
                                                mail_content += mixed_part.get_payload(decode=True).decode(mixed_part.get_content_charset())
                                            
                                            elif mixed_part.get_content_type() == 'text/html':
                                                mail_content += mixed_part.get_payload(decode=True).decode(mixed_part.get_content_charset())
                                    else:
                                        print('other content type',content_type)
                                
                                # if 'Please provide us with a fee and turn time for this' in mail_content or ('Click the following link to view the details of the order:' in mail_content and 'New Order' in msg['subject']):
                                    
                                    unread_new_emails[to_address] = [mail_content, msg['subject']]
                                    
                        return unread_new_emails
        except Exception as ex:
            test_exception_mail_send(self.portal_name, self.portal_name, ex)
            # exception_mail_send(self.portal_name, self.portal_name, ex)
            logging.info(f"An exception while checking for new order mail notification {ex}")


    def extract_response_link_and_order(self, value):
        try:
            mail_body = value[0]
            subject = value[1]

            mail_content_soup = BeautifulSoup(mail_body, 'html.parser')

            response_link = None
            for a in mail_content_soup.find_all('a', href=True):
                if 'dashboard.pcvmurcor.com' in a['href']:
                    response_link = a['href']
                    break

            order_id_match = re.search(r'ORDER\s*#\s*(\d+)', subject)
            print("order id is : ", order_id_match)
            order_id = order_id_match.group(1) if order_id_match else ''
            print(order_id)

            addr_tag = mail_content_soup.find('td', string='Subject Address')
            if addr_tag:
                address = addr_tag.find_next_sibling('td').get_text(strip=True)
                zipcode = address.split(',')[-1].strip().split()[-1]
            else:
                address = ''
                zipcode = ''

            order_type_tag = mail_content_soup.find('td', string='Order Type')
            order_type = order_type_tag.find_next_sibling('td').get_text(strip=True) if order_type_tag else ''

            due_tag = mail_content_soup.find('td', string='Due Date')
            due_text = due_tag.find_next_sibling('td').get_text(strip=True) if due_tag else ''
            try:
                due_date = datetime.datetime.strptime(due_text, '%m/%d/%Y %I:%M %p')
                due = due_date.strftime('%d-%m-%Y')
            except:
                due = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%d-%m-%Y')

            price_tag = mail_content_soup.find('td', string='Fee')
            price_text = price_tag.find_next_sibling('td').get_text(strip=True).replace('$', '') if price_tag else ''
            extracted_order_price = price_text if price_text else ''

            avail_order = {
                'address': address,
                'zipcode': zipcode,
                'order_type': order_type,
                'due': due,
                'order_id': order_id
            }

            if extracted_order_price:
                avail_order['price'] = extracted_order_price

            if response_link:
                return response_link, avail_order
            else:
                logging.warning('Response link not found.')
                return None, None

        except Exception as e:
            logging.error(f'An exception in the function "extract_response_link_and_order()": {e}')
            return None, None


    def extract_counter_response_link_and_order(self, value):
        try:
            mail_body = value[0]
            subject = value[1]
            mail_content_soup = BeautifulSoup(mail_body, 'html.parser')
            response_link = None
            for a in mail_content_soup.find_all('a', href=True):
                if 'dashboard.pcvmurcor.com' in a['href'] and 'FeeQuote.aspx' in a['href']:
                    response_link = a['href']
                    break
            order_id_match = re.search(r'Order\s*#[:\s]*(\d+)', mail_body, re.IGNORECASE)
            order_id = order_id_match.group(1) if order_id_match else ''
            product_match = re.search(r'Product Name[:\s]*(.*)', mail_body)
            product_name = product_match.group(1).strip() if product_match else ''
            address_match = re.search(r'Property Address[:\s]*(.*)', mail_body)
            address = address_match.group(1).strip() if address_match else ''
            zipcode = ''
            if address:
                try:
                    zipcode = address.split(',')[-1].strip().split()[-1]
                except:
                    zipcode = ''
            # Default due date -> temparary
            due = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%d-%m-%Y')
            avail_order = {
                'address': address,
                'zipcode': zipcode,
                'order_type': product_name,
                'due': due,
                'order_id': order_id
            }
            if response_link:
                return response_link, avail_order
            else:
                logging.warning("Counter: Response link not found.")
                return None, None
        except Exception as e:
            logging.error(f'An exception in "extract_counter_response_link_and_order()": {e}')
            return None, None


    def counter_check_ordertype(self, avail_order, common_db_data):
        try:
            order_type = avail_order['order_type'].lower()  
            donot_accept_ordertypes = [x.lower().strip() for x in self.client_data['donot_accept_ordertypes'].split(',')]        
            if self.client_data['order_quote_ordertypes']:
                client_quote_order_types = [x.strip() for x in self.client_data['order_quote_ordertypes'].split(',')]
            else: 
                client_quote_order_types = ''
            
            if common_db_data['exterior_ordertypes']:    
                exterior_ordertypes = [x.lower().strip() for x in common_db_data['exterior_ordertypes'].split(',')]
            else: 
                exterior_ordertypes = ''
                
            if "Exterior" in client_quote_order_types and (order_type in exterior_ordertypes) and (order_type not in donot_accept_ordertypes):
                
                requesting_fee = self.client_data['order_quote_ext_price']
                zipcode_in_db = self.client_data['Zipcode']
                return requesting_fee, zipcode_in_db, True
            
            #quote exterior inspection order type
            if common_db_data['exterior_inspection_ordertypes']:
                exterior_inspection_ordertypes = [x.lower().strip() for x in common_db_data['exterior_inspection_ordertypes'].split(',')] 
            else: 
                exterior_inspection_ordertypes = ''
                
            if "Exterior Inspection" in client_quote_order_types and (order_type in exterior_inspection_ordertypes) and (order_type not in donot_accept_ordertypes):
                
                requesting_fee = self.client_data['order_quote_ext_insp_price']
                zipcode_in_db = self.client_data['Zipcode']
                return requesting_fee, zipcode_in_db, True
            
            #quote interior order type
            if common_db_data['interior_ordertypes']:
                interior_ordertypes = [x.lower().strip() for x in common_db_data['interior_ordertypes'].split(',')]
            else: 
                interior_ordertypes = ''
            
            if "Interior" in client_quote_order_types and (order_type in interior_ordertypes) and (order_type not in donot_accept_ordertypes):
                
                requesting_fee = self.client_data['order_quote_int_price']
                zipcode_in_db = self.client_data['Int_Zipcode']
                return requesting_fee, zipcode_in_db, True
            
            #quote interior inspection order type
            if common_db_data['interior_inspection_ordertypes']:
                interior_inspection_ordertypes = [x.lower().strip() for x in common_db_data['interior_inspection_ordertypes'].split(',')]
            else: 
                interior_inspection_ordertypes = ''
            
            if "Interior Inspection" in client_quote_order_types and (order_type in interior_inspection_ordertypes) and (order_type not in donot_accept_ordertypes):
                
                requesting_fee = self.client_data['order_quote_int_insp_price']
                zipcode_in_db = self.client_data['Int_Zipcode']
                return requesting_fee, zipcode_in_db, True
            
            return None, None, False 
            
        except Exception as e:
            
            logging.exception(f'An exception occured while checking quote order type : {e}')
            return None, None, False
        
    def criteria_check_new_order(self, avail_order):
        try:
            due_text = str(avail_order['due'])  # Ex: "05/31/2025 5:00 PM"
            try:
                due_datetime = datetime.datetime.strptime(due_text, "%m/%d/%Y %I:%M %p")
            except ValueError:
                due_datetime = datetime.datetime.strptime(due_text.split(" ")[0], "%m/%d/%Y")
            zone = timezone('EST')
            today_str = datetime.datetime.now(zone).strftime("%m/%d/%Y")
            today = datetime.datetime.strptime(today_str, "%m/%d/%Y")
            diff = (due_datetime - today).days
            logging.info(f"Days until due: {diff}")

            common_db_data = cursorexec("order_updation", 'SELECT', "SELECT * FROM `common_data_acceptance`")

            price_in_db, zipcode_in_db, typecheck_flag = check_ordertype(
                avail_order['order_type'], avail_order.get('price', 0),
                common_db_data, self.client_data, self.portal_name
            )

            if typecheck_flag:
                zipcode_dict = {zipcode.strip(): True for zipcode in zipcode_in_db.split(',')}
                due_str = due_datetime.strftime('%d-%m-%Y')  
                avail_order['due'] = due_str  
                due, fee_portal, flag = criteria_with_params(
                    price_in_db, zipcode_dict, avail_order['price'], diff,
                    avail_order['zipcode'], self.client_data, due_str,
                    common_db_data, self.portal_name, avail_order['address']
                )
                return avail_order, due, flag
            else:
                logging.info("Order Type Not Mapped in Database")
                ignored_msg = "Order Type not satisfied"
                return avail_order, ignored_msg, typecheck_flag

        except Exception as ex:
            exception_mail_send(self.portal_name, self.client_data['Client_name'], ex)
            logging.exception("Exception in PCV criteria_check")
            return avail_order, "Exception", False


    def criteria_check_order_quote(self, avail_order):
        try:
            due_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m/%d/%Y %I:%M %p")
            avail_order['due'] = due_date
            diff = 1
            common_db_data = cursorexec("order_updation", "SELECT", "SELECT * FROM `common_data_acceptance`")
            
            requesting_fee, zipcode_in_db, typecheck_flag = self.counter_check_ordertype(avail_order, common_db_data)
            
            if not typecheck_flag:
                logging.info("Order Type not valid for quote.")
                return avail_order, due_date, False
            
            avail_order['price'] = requesting_fee
            
            zipcode_in_db={zipcode: True for zipcode in zipcode_in_db.split(',')}
            due,fee_portal,flag=criteria_with_params(requesting_fee,zipcode_in_db,requesting_fee, diff, avail_order['zipcode'],self.client_data,avail_order['due'],common_db_data,self.portal_name,avail_order['address'])

            # is_valid = zipcode_check(
            #     avail_order['zipcode'],
            #     avail_order['order_type'],
            #     requesting_fee,
            #     self.client_data,
            #     self.portal_name
            # )

            if flag:
                logging.info("Order passed criteria for quote.")
                return avail_order, due_date, True
            else:
                logging.warning(" Counter criteria failed: {due_result}")
                return avail_order, due_date, False

        except Exception as ex:
            logging.exception("Exception occurred in criteria_check_order_quote()")
            return avail_order, "", False

            
    def login_pcv(self, username, password):
        try:
            self.session = requests.Session()
            login_url = "https://dashboard.pcvmurcor.com/login.aspx"

            # Step 1: Load login page
            response = self.session.get(login_url)
            soup = BeautifulSoup(response.content, "html.parser")

            # Step 2: Extract ASP.NET tokens
            viewstate = soup.find("input", {"name": "__VIEWSTATE"})["value"]
            viewstategen = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"]
            eventvalidation = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]

            # Step 3: Prepare login data
            login_data = {
                "__LASTFOCUS": "",
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": viewstate,
                "__VIEWSTATEGENERATOR": viewstategen,
                "__EVENTVALIDATION": eventvalidation,
                "ctl00$MainContent$Login1$UserName": username,
                "ctl00$MainContent$Login1$Password": password,
                "ctl00$MainContent$Login1$btnLogin": "LOGIN"
            }

            # Step 4: Headers
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://dashboard.pcvmurcor.com",
                "Referer": login_url,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            }

            # Step 5: Submit login form
            login_response = self.session.post(login_url, headers=headers, data=login_data)

            post_login_soup = BeautifulSoup(login_response.content, "html.parser")

            # Step 6: Look for login confirmation
            welcome_span = post_login_soup.find("span", {"id": "MainContent_lbWelcome"})

            if welcome_span and "Welcome" in welcome_span.text:
                logging.info(f" PCV login successful: {welcome_span.text.strip()}")
                cookie_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
                cookie_json = json.dumps(cookie_dict)
                cursorexec("order_acceptance", "UPDATE", f"""
                    UPDATE pcv SET Session_cookie = '{cookie_json}'
                    WHERE Email_address = '{self.client_data["Email_address"]}'
                """)
                return True, self.session, post_login_soup
            else:
                logging.warning(" PCV login failed: Welcome message not found.")
                return False, None, None
            
        except Exception as ex:
            logging.exception(" Exception during PCV login")
            return False, None, None
        
        
    def load_session_from_db(self):
        """
        Attempts to reuse a previously stored session from the database.
        Returns:
            (bool, session object, soup object) — indicating success, session, and parsed page.
        """
        try:
            cookie_data = self.client_data.get("Session_cookie")
            if not cookie_data:
                logging.info(" No session cookie found in DB for client.")
                return False, None, None

            # Convert cookie JSON back to dict
            cookies = json.loads(cookie_data)

            # Create session and apply cookies
            self.session = requests.Session()
            self.session.cookies = requests.utils.cookiejar_from_dict(cookies)

            # Try accessing a protected page to verify session
            test_url = "https://dashboard.pcvmurcor.com/memberpages/Main/SummaryPage.aspx"
            response = self.session.get(test_url, allow_redirects=True)

            # If redirected to login, session is expired
            if "login.aspx" in response.url.lower():
                logging.warning(" Stored session expired or redirected to login.")
                return False, None, None

            soup = BeautifulSoup(response.content, "html.parser")
            welcome_span = soup.find("span", {"id": "MainContent_lbWelcome"})

            if welcome_span and "Welcome" in welcome_span.text:
                logging.info(f"Reused valid session from DB: {welcome_span.text.strip()}")
                return True, self.session, soup
            else:
                logging.warning("Session may be invalid — welcome text not found.")
                return False, None, None

        except Exception as ex:
            logging.exception("Error while loading session from DB")
            return False, None, None


            
    def ensure_logged_in(self):
        success, session, soup = self.load_session_from_db()
        if success:
            return True, session, soup
        success, session, soup = self.login_pcv(
            self.client_data['userid'],
            self.client_data['password']
        )
        return success, session, soup


    def send_counter(self, response_link, fee, due_date):
        try:
            session = requests.Session()
            resp = session.get(response_link)
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            
            page_title = soup.find("span", {"id": "dvQuote_lblActionMsg"})
            property_address = soup.find("span", string="Property Address")
            property_name = soup.find("span", string="Product Name")

            logging.info("📝 Fee Quote Page Loaded")
            print("📝 Fee Quote Page Loaded")
            if page_title:
                print("page title", page_title)
                logging.info(f"Page Title: {page_title.text.strip()}")
            if property_address:
                print("property address",property_address)
                address_val = property_address.find_next_sibling("span").text.strip()
                print("property address",address_val)
                logging.info(f"Property Address: {address_val}")
            if property_name:
                product_val = property_name.find_next_sibling("span").text.strip()
                print("Product Name",product_val)
                logging.info(f"Product Name: {product_val}")
                

            viewstate = soup.find("input", {"name": "__VIEWSTATE"})["value"]
            viewstategen = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"]
            eventvalidation = soup.find("input", {"name": "__EVENTVALIDATION"})["value"]

            now = datetime.datetime.now()
            due_datetime = (now + datetime.timedelta(hours=25)).strftime("%m/%d/%Y %I:%M %p")
            expire_datetime = (now + datetime.timedelta(hours=48)).strftime("%m/%d/%Y %I:%M %p")


            data = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__LASTFOCUS": "",
                "__VIEWSTATE": viewstate,
                "__VIEWSTATEGENERATOR": viewstategen,
                "__EVENTVALIDATION": eventvalidation,

                "txtDesiredFee": str(fee),
                "ddQuoteReason": "5",  
                "txtDueDateTime": due_datetime,
                "txtExpiredDateTime": expire_datetime,

                # "btnSubmit": "Submit Fee Quote"
            }
            print("The free quoate submitted data",data)

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0",
                "Referer": response_link,
            }

            post_url = response_link.split('?')[0]
            result = session.post(post_url, data=data, headers=headers)
            print("the quote order :",result)

            if result.status_code == 200 and "Fee Quote Submitted" in result.text:
                logging.info("Counter offer submitted successfully.")
                return True
            else:
                logging.warning("Counter offer submission may have failed.")
                return False

        except Exception as e:
            logging.exception("Error in send_counter()")
            return False
