import boto3
from botocore.exceptions import ClientError

# following this guide here: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html

SENDER = "Train <train@10academy.org>"

RECIPIENT = "gkkarobia@gmail.com"

CONFIGURATION_SET = "trainMailEvens"
AWS_REGION = "eu-west-1"
SUBJECT = "AMAZON SES TEST (SDK FOR PYTHON)"

BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES for the "
             "Trello Task"
             )

BODY_HTML = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> for the
    <a href='https://trello.com/c/xbI47onZ'>
      Trello Task</a>.</p>
</body>
</html>
            """

CHARSET = "UTF-8"

client = boto3.client('ses', region_name=AWS_REGION)

try:
    response = client.send_email(
        Destination={
            'ToAddresses': [RECIPIENT]
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
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
    print("Email sent! Message ID:")
    print(response["MessageId"])
