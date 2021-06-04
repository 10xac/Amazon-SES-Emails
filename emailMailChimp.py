import pandas as pd
import boto3
from botocore.exceptions import ClientError

SENDER = "Train <train@10academy.org>"

AWS_REGION = "eu-west-1"

SUBJECT = "Get job-ready as a Machine Learning Engineer in 12 weeks - 10 Academy's 4th batch of training"

RECIPIENT = "gkkarobia@gmail.com"

df = pd.read_csv('mailchimp.csv')
print(df.columns)

kevin = ["Kevin", "Kevin11"]

for i, firstName in enumerate(df['First Name']):
    BODY_TEXT = (f"Dear {firstName}, \r\n"
                 "We're writing to let you know that we've just opened up applications for the 4th batch of training for 10 Academy, and we are looking for highly motivated recent graduates from Africa who want to start their career in this field. Please share this with candidates that you feel could benefit from this opportunity or apply now!\r\n\n"
                 "10 Academy is a not-for-profit program to get the most motivated recent African university graduates placed into global careers in Machine Learning. Training is fully online, where a dedicated team provides industry-relevant challenges, coaching and mentoring, along with industry leaders, guest speakers and dedicated community support. The 4th batch of training starts 12 July 2021.\r\n\n"
                 "Our most recent batch had 75% of trainees placed into work within 6 months, earning 2.5x the median salary of their peers, working for companies around the world. 40% of training spots are for women.\r\n\n"
                 "Costs: There is no application fee, and you only pay it forward once you are getting paid over $500US/month.\r\n\n"
                 "Applications close 13 June 2021. If you have any questions, please contact us at train@10academy.org.\r\n\n"
                 "'10 Academy jump-started my career by multiplying my skills and determination to work before placing me into a great job. -N.N., Batch 3 trainee'\r\n\n"
                 "Application and more information here: 10academy.org/train. \r\n\n"
                 "Best wishes,\r\n"
                 "The 10 Academy team"
                 )

    CHARSET = "UTF-8"

    client = boto3.client('ses', region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [df['Email Address'][i]]
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
        print(f"Email sent to {df['Email Address'][i]} ! Message ID:")
        print(response["MessageId"])
