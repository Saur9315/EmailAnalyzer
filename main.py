import email_retrieve
import pandas as pd
import re
import ml_model
import nlp_message_processing
import db_config
from decouple import config
from googletrans import Translator


pd.set_option('display.max_columns', None)


def translate_to_russian(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='ru')
    return translation.text

# sender_name = 'Paul'
# sender_address = 'client_01@gmail.com'
# email_subject = "Inquiry about Server Purchase."
# email_text = f"""
#     Hello Company Team,
#     I hope this email finds you well. My name is {sender_name}, and I am reaching out to inquire about your
#     server products. We are planning to upgrade our server infrastructure, and I'm interested in learning more about
#     the specifications, pricing, and any ongoing promotions or discounts.
#     Could you please provide detailed information about the server models you offer, including their
#     features and pricing? Additionally, if there are any upcoming events or webinars related to your server solutions,
#     I would appreciate the details.
#
#     Thank you for your time, and I look forward to hearing from you soon.
#
#     Best regards,
#     {sender_name}.
#     """
# email_content_type = 'text/plain'

# sender_address = 'sender_address@gmail.com'
# email_subject = " Urgent: Software Issue - Need Assistance."
# email_text = """
# Dear Company Support,
# I hope you can assist me with a critical issue we are currently facing. My team and I have been using your [Software Name] for the past few months, and we've encountered a persistent issue that is affecting our workflow.
# The problem involves [describe the issue briefly]. We have already tried [mention any troubleshooting steps taken], but the issue persists. This is impacting our productivity, and we need urgent assistance to resolve it.
# Could you please assign this to your technical support team and provide guidance on how we can quickly address and resolve this issue? If there's any additional information needed from our end, please let us know.
# Thank you for your prompt attention to this matter.
#
# Regards,
# Sender.
# """
# email_content_type = 'text/plain'
# html_msgs = [(sender_address, email_subject, email_text, email_content_type)]

# print(config('EMAIL_ADDRESS'))


html_msgs = email_retrieve.get_email_messages(email_address=config('EMAIL_ADDRESS'), password=config('PASSWORD'))


def get_sender_name(email_text):
    sender_name_pattern = re.compile(r"Best\s*regards,\s*([^.\r\n]+)", re.IGNORECASE)
    match = sender_name_pattern.search(email_text)
    if match:
        name = match.group(1).strip()
        return name
    else:
        return None


# Trusted clients list
client_address_ls = config('CLIENT_EMAIL_LIST').split(',')

for email in client_address_ls:
    db_config.insert_data(table_name='clients', data={'email_address': email}, condition={'email_address': email})

# Clients' data from database
client_db = db_config.get_data(table_name='clients')

# Checking and inserting clients' info from list to db. temp.
# for email in client_address_ls:  # temp
#     if email not in [row[3] for row in client_db]:
#         name, surname = email.split('@')[0].split('_')
#         data = {'name': name, 'surname': surname, 'email_address': email}
#         db_config.insert_data(table_name='clients', data=data, condition=data)

print('Clients data: \n', client_db)
# print(db_config.get_data(table_name='clients'))

# # Email message processing
for message in html_msgs:
    sender, subject, body, content_type = message
    # sender = sender.split()[1][1:-1]  # in case, the sender info consists of name and address
    print("SENDER: ", sender)

    if sender in [row[3] for row in client_db]:
        if content_type not in ['text/plain', 'text/html']:
            continue
        print('\nMessage processing.')
        name = get_sender_name(body)
        # print("Name: ", name)
        # translated_body = translate_to_russian(body)
        # print(translated_body)

        # ML
        label_predicted = ml_model.load_and_predict(new_text=body)[0]
        # label_predicted = ml_model.load_and_predict(new_text=translated_body)[0]
        print('\nLabel predicted: ', label_predicted)

        data = {'email_address': sender, 'name': name, 'subject': subject, 'intention': label_predicted,
                'is_solved': False}
        db_config.insert_data(table_name='clients_inquiry_support', data=data, condition=data)
        db_config.update_data(table_name='clients', data={'name': name}, condition=sender)