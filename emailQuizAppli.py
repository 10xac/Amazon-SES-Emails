import pandas as pd
import boto3
import gspread
from botocore.exceptions import ClientError
from oauth2client.service_account import ServiceAccountCredentials as sac


def gsheet2df(spreadsheet_name, sheet_num):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials_path = 'appli.json'

    credentials = sac.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(credentials)

    sheet = client.open(spreadsheet_name).get_worksheet(sheet_num).get_all_records()
    df = pd.DataFrame.from_dict(sheet)

    print(df.columns)
    return df

def emailThem():
    SENDER = "10 Academy Training Team <train@10academy.org>"

    AWS_REGION = "eu-west-1"

    SUBJECT = "Reminder - 10 Academy Batch 4 - Proceed to Quiz stage - 15 June 2021 (Tomorrow) 11AM-12PM GMT"

    RECIPIENT = ["gkkarobia@gmail.com", "alaroabubakarolayemi@gmail.com"]

    df = gsheet2df('10 Academy Batch 4 Application form (Responses)', 0)

    for i, firstName in enumerate(df['First Name']):
        BODY_TEXT = (f"Dear {firstName}, \r\n\n"
                     "Thanks for applying to 10 Academy, for our 4th batch of training. As part of the application process, we are pleased to invite you to the next phase of the process, which is an online assessment of your pre-requisite knowledge in the form of a quiz.\r\n\n"
                     "More about the quiz:\r\n"
                     "The quiz will be 1-hour long assessment of your pre-requisite skills. It will be open internet and all online resources are allowed. Collaboration with others is not allowed. Content covered will include statistics, algebra, python coding and probability theory.\r\n\n"
                     "More about the application process:\r\n"
                     "The quiz stage of the application process allows us to gather more information about applicants. Your quiz results, together with the information submitted as part of your application, will be reviewed and successful applicants will get a notification by 19 June 2021 on whether they have been invited to the pre-training assessment week, which runs full-days 21-25 June 2021. We are looking for effort and potential more than current level of knowledge.\r\n\n"
                     "Quiz details:\r\n"
                     "Date: Tues 15 June 2021 \r\n"
                     "Opens: 11AM GMT\r\n"
                     "Closes: 12PM GMT\r\n"
                     "Max duration: 1 hour \r\n"
                     "Quiz location: https://forms.gle/UtGKFMWVZ3LpzgQQ6 \r\n\n"
                     "Requirements: Stable internet connection\r\n\n"
                     "Please write to us at train@10academy.org with any questions.\r\n"
                     "Thanks and all best wishes,\r\n"
                     "10 Academy training team"
                     )

        CHARSET = "UTF-8"

        client = boto3.client('ses', region_name=AWS_REGION)

        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': [df['Email address'][i]]
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    }
                },
                Source=SENDER
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            # df['Email Address']
            print(f"Email sent to {df['Email address'][i]} ! Message ID:")
            print(response["MessageId"])

emailThem()
