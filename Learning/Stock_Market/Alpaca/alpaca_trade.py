from datetime import datetime
import send_email as mail

send_alert_email = False
write_log = True

if write_log:
    with open('alpaca_trade.log', 'a') as f:
        f.write(f'Finished at {str(datetime.now())}\n')

if send_alert_email:
    mail.send_email(
        recipients=['jonatasgomes@gmail.com'],
        subject='Stock Market Alpaca',
        body='First test'
    )
    print('Alert email sent!')
