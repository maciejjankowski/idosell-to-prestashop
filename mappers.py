from generate_password import generate_password
import re

def map_client_record(idosell_client_record):
    """Maps columns from idosell schema (SCHEMA_A) to PrestaShop schema (SCHEMA_B).

    Args:
        idosell_client_record (dict): A dictionary representing a client record from idosell.

    Returns:
        dict: A dictionary representing the mapped client record for PrestaShop.
    """

    fields_map = {
        # pole poniżej to: presta_key : idosell_key
        "Customer ID": "id",
        "Active (0/1)": "block_account",  # Assuming 0 is blocked, 1 is active
        "Email *": "email",
        # "Password *": "login",  # Assuming password is used as login
        # "Birthday (yyyy-mm-dd)": "date_of_registration",  # Assuming birthday is used as registration date
        "Last Name *": "lastname",
        "First Name *": "firstname",
        # "Newsletter (0/1)": "newsletter_sms",  # Assuming newsletter is SMS based
        # "Registration date (yyyy-mm-dd)": "date_of_registration",
        # "Default group ID": "client_type",  # Assuming default group ID maps to client type
    }

    
    presta_client_record = {}
    for presta_key, idosell_key in fields_map.items():
        if idosell_key in idosell_client_record:
            presta_client_record[presta_key] = idosell_client_record[idosell_key]

    presta_client_record["Last Name *"]= \
        re.sub(r'[0-9!<>,;?=+()@#"°{}_$%:¤|./]', '', presta_client_record["Last Name *"])
        
    presta_client_record["First Name *"]= \
        re.sub(r'[0-9!<>,;?=+()@#"°{}_$%:¤|./]', '', presta_client_record["First Name *"])


    if len(presta_client_record["Last Name *"]) == 0:
        presta_client_record["Last Name *"] = \
            re.sub(r'[^a-zA-Z]', '', presta_client_record["Email *"].split('@')[0])[-10:]
    
    if len(presta_client_record["First Name *"]) == 0:
        presta_client_record["First Name *"] = \
            re.sub(r'[^a-zA-Z]', '', presta_client_record["Email *"].split('@')[0])[:10]
        
    
    
    
    # print(presta_client_record)

    # Handle special cases:
    if "block_account" in idosell_client_record:
        active = idosell_client_record["block_account"]
        if active == 'y':
            presta_client_record["Active (0/1)"] = 0
        elif active == 'n':
            presta_client_record["Active (0/1)"] = 1

            
    # - "Titles ID (Mr = 1, Ms = 2, else 0)": Map to "companyname" if available, otherwise leave empty
    if "Titles ID (Mr = 1, Ms = 2, else 0)" in idosell_client_record:
        raise Exception("Not implemented yet")
        title_id = idosell_client_record["Titles ID (Mr = 1, Ms = 2, else 0)"]
        if title_id == 1:
            presta_client_record["companyname"] = "Mr."
        elif title_id == 2:
            presta_client_record["companyname"] = "Ms."

    # - "Groups (x,y,z...)": Map to "labels" if available, otherwise leave empty
    if "Groups (x,y,z...)" in idosell_client_record:
        raise Exception("Not implemented yet")
        presta_client_record["labels"] = idosell_client_record["Groups (x,y,z...)"]
    

    presta_client_record["Password *"] = generate_password(include_symbols=False)
    # print(presta_client_record["Email *"],presta_client_record["Password *"])
    # raise Exception("setting password")
    return presta_client_record

# "Customer ID;Active (0/1);Titles ID (Mr = 1, Ms = 2, else 0);Email *;Password *;Birthday (yyyy-mm-dd);Last Name *;First Name *;Newsletter (0/1);Opt-in (0/1);Registration date (yyyy-mm-dd);Groups (x,y,z...);Default group ID"
# "id;login;block_account;companyname;firstname;lastname;;wholesaler;taxidnumber;phone;phone2;email;street;zipcode;city;address;country;language;date_last_order;recently_logged_on;date_of_registration;shop;client_type;mailing;newsletter_sms;note_about_client;opinions;labels;orders_send;orders_all;products_observe;products_bought;assortment_positions;orders_worth;"orders_worth_detail: net";"orders_worth_detail: gross";"orders_worth_wholesale: net";"orders_worth_wholesale: gross";"orders_worth_in_shop: 1";"orders_worth_in_shop: 2";"orders_worth_in_shop: 3";average_orders_worth;average_products;rma_all;returns_all;returns_products_all;ballance;balance_limit;invoice_tc_count;invoice_tc_worth;affiliate_program;affiliate;affiliate_orders_all;affiliate_orders_total;loyalty_points;rebate;membership_card;offerForamt;offerFileType;offerShops;apiIcdfAccess;is_iai_export"

