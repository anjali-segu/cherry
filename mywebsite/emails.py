import uuid
import sendgrid

from mywebsite.settings import SENDGRID_API_KEY, FROM_EMAIL, WEBSERVER_URL
from charity.models import CharityProfile

sengrid_client = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
HTML = 'text/html'

RESET_EMAIL_BODY = '''
    <html>
        <body>
            <h3>Your CherryGiver Account has been reset!</h3>
            <p>Please login with the following temporary credentials</p><br>
            <span>Username: <b>{username}</b></span><br>
            <span>Password: <b>{password}</b></span><br>
            <br>
            <p>You will be able to change your password upon <a href="{webserver_url}" target="_blank">login</a>.</p>
            <p>If you did not request a password reset, please contact us immediately.</p>
            <br>
            <p>Thanks,</p>
            <span>CherryGiver Team</span><br>
            <a href="{webserver_url}" target="_blank">www.cherrygiver.org</a><br>
        </body>
    </html>
'''


def send_password_reset_email(user):
    new_password = _reset_password(user)
    body = RESET_EMAIL_BODY.format(
        username=user.username,
        password=new_password,
        webserver_url=WEBSERVER_URL
    )
    data = _get_email_data(user.email, body)
    sengrid_client.client.mail.send.post(request_body=data)


def _reset_password(user):
    new_password = _get_new_password()
    user.set_password(new_password)
    user.save()
    charity_profile = CharityProfile.objects.get(user=user)
    charity_profile.is_password_reset = True
    charity_profile.save()
    return new_password


def _get_new_password():
    return str(uuid.uuid4()).replace('-', '')


def _get_email_data(to_email, body):
    data = {
        'personalizations': [
            {
                'to': [
                    {
                        'email': to_email
                    }
                ],
                'subject': 'CherryGiver Account Password Reset'
            }
        ],
        'from': {
            'email': FROM_EMAIL
        },
        'content': [
            {
                'type': HTML,
                'value': body,
            }
        ]
    }
    return data
