"""FILE CONTAINS THE Applied Valuation Acceptance MAIN FUNCTION which is used to run the acceptance"""
import logging
import datetime
import time
import ctypes
from random import randint
from helper.pcv import pcv
from stdlib.creds import dbcred,email_cred
from stdlib.utility import inactive_inDB,capacity_mail_send,send_login_error_mail,ignored_order,write_to_db,send_accepted_mail,cursorexec,exception_mail_send,logger_mail,successmessageconditionalyaccept,client_mail_send,check_counter_accepted
import sys
import sender

portal_name = 'pcvmurcor'
email_creds = email_cred()

def classify_order_type(subject):
    """Classify the email as new order or counter quote request."""
    subject_lower = subject.lower()
    if "new bpo order from pcv murcor" in subject_lower:
        return "new_order"
    elif "fee quote request on order" in subject_lower:
        return "counter_request"
    else:
        return "unknown"


def main():
    # logger_mail(portal_name)

    while True:
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(f"{portal_name}")
            init = pcv("", portal_name)

            # cursorexec("order_updation",'UPDATE',f"""UPDATE `servercheck` SET `event`='{datetime.datetime.now()}' where `portal`='{portal_name}' and `clientname` = '{portal_name}'  """)
            # script_status_update_buddy("pcvmurcor", 'active', 'running')

            orders_found = init.checkorder_mail()
            print(orders_found)
    
            if orders_found:
                
                for key, value in orders_found.items():
                    logging.info(f'subject line : {value[1]}')
                    key = key.replace("<", "").replace(">", "").strip()
                    mail_content, subject = value
                    order_type = classify_order_type(subject)
                    print(f"\n Processing: {order_type.upper()} | Subject: {subject} | Email: {key}")
                    new_order = []
                    countered = []
                    ignored = []

                    client_data = cursorexec("order_acceptance", "SELECT", f"""SELECT * FROM `pcv` WHERE `Email_address` = '{key}' LIMIT 1""")
                    init.client_data = client_data
                    order_received_time = datetime.datetime.now()

                    if client_data and client_data['Status'] == 'Active':
                        logging.info(f"%s acceptor for %s", portal_name, client_data['Client_name'])

                        if 'New Order' not in subject:
                            
                            if order_type == "new_order":
                                response_link, subject_details = init.extract_response_link_and_order(value)

                                if not subject_details:
                                    print(" Could not extract order details. Skipping.")
                                    continue

                                to_accept, due_date, criteria_flag = init.criteria_check_new_order(subject_details)
                                logging.info(f"After criteria check : to_accept = {to_accept}, due_date : {due_date}")

                                # criteria_flag = True
                                if criteria_flag:
                                    is_logged_in, session, soup = init.ensure_logged_in()

                                    if is_logged_in:
                                        print(soup.prettify())
                                        logging.info(f"Criteria matched. Attempting to accept...")
                                        print(" Criteria matched. Attempting to accept...")
                                        flag_check = init.accept_pcv_order(session, response_link, due_date, to_accept['price'])

                                        if flag_check:
                                            new_order.append({
                                                'to_accept': to_accept,
                                                "due_date": due_date,
                                                "order_received_time": order_received_time
                                            })
                                        else:
                                            ignored.append({
                                                'to_accept': to_accept,
                                                'ignoredmsg': 'Order Expired',
                                                'fee_portal': to_accept['price'],
                                                'client_data': client_data,
                                                'Address': to_accept['address'],
                                                "order_received_time": order_received_time
                                            })
                                else:
                                    print("Order criteria failed.")
                                    ignored.append({
                                        'to_accept': to_accept,
                                        'ignoredmsg': due_date,
                                        'fee_portal': to_accept['price'],
                                        'client_data': client_data,
                                        'Address': to_accept['address'],
                                        "order_received_time": order_received_time
                                    })

                            elif order_type == "counter_request":
                                if client_data and client_data['order_quote_status'] == 'ON':  

                                    try:
                                        response_link, avail_order = init.extract_counter_response_link_and_order([mail_content, subject])
                                        
                                        if avail_order:
                                            avail_order, due, criteria_flag  = init.criteria_check_order_quote(avail_order)
                                            print(f"Countering with: ${avail_order['price']} for Order ID: {avail_order['order_id']}")
                                            
                                            if criteria_flag:
                                                print(f"Ready to submit fee: {avail_order['price']} for order {avail_order['order_id']}")
                                                countered.append({'countered_order': avail_order, 'due_date' : due,  })
                                                print(countered)

                                                success = init.send_counter(response_link, avail_order['price'], due)
                                                print("the sucess msg of fee quoate", success)
                                                 
                                                # write_to_db(client_data, str(datetime.datetime.now()), due, portal_name,
                                                #         avail_order['price'], avail_order['order_type'], avail_order['address'],
                                                #         "Countered", portal_name, avail_order['order_id'], subject, order_received_time)
                                            else:
                                                print("Counter order did not meet criteria.")
                                        else:
                                            print(" Could not extract counter order details.")
                                    except Exception as e:
                                        logging.exception("Exception in counter handling")
                                else:
                                  print(f"Skipping - client inactive or quote status is ON: {key}")

                            # Handle ignored orders
                            for ignore in ignored:
                                order_details = ignore['to_accept']
                                zipcode = order_details['zipcode'].split("-")[0] if '-' in order_details['zipcode'] else order_details['zipcode']
                                subject_line = f"Ignored Order!!! - {portal_name} - {ignore['ignoredmsg']}"
                                # ignored_order(
                                #     ignore['Address'], order_details['order_type'], ignore['ignoredmsg'],
                                #     ignore['fee_portal'], ignore['client_data'], portal_name,
                                #     zipcode, subject_line, ignore['order_received_time']
                                # )

                        else:
                            # Confirmed Order
                            order_address = init.extract_confirmation_order_details(subject)
                            counter_accepted_flag = init.check_if_counter_accepted(client_data, order_address, portal_name)
                            print(f"Counter Accepted? {counter_accepted_flag}")

                    else:
                        print(" Client is inactive.")
                        # inactive_inDB(client_data['Client_name'], portal_name)

                    

                time.sleep(randint(1, 2))

            else:
                print("No new orders found.")
                time.sleep(randint(1, 2))

        except Exception as ex:
            logging.exception("Unhandled exception in main loop")
            time.sleep(30)
            continue


if __name__ == "__main__":
    main()