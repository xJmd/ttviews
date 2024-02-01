from flask import Flask, render_template, request, redirect, url_for
import random
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1202604555242577940/zIXeSBlVcPvyJSClaS6WidtayEVbq5vNtm4O62ilxJkUSl4ev_iKptWj5U_0WR3pVPy2'

# Store orders and emails in a dictionary for simplicity. In a real application, use a database.
order_data = {}

def send_discord_notification(order_id, tiktok_link, views_count, email):
    discord_payload = {
        'content': f'----------------\nNew Order!\nOrder ID: {order_id}\nTikTok Link: {tiktok_link}\nViews Count: {views_count}\nEmail: {email}\n----------------'
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=discord_payload)
    if response.status_code != 200:
        print(f'Error sending Discord notification. Status Code: {response.status_code}, Response: {response.text}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/place-order', methods=['POST'])
def place_order():
    tiktok_link = request.form['tiktok-link']
    views_count = request.form['views-select']

    # Generate a random order ID for simplicity. In a real application, use a more robust method.
    order_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))

    order_details = {
        'tiktok_link': tiktok_link,
        'views_count': views_count
    }

    # Log the order
    order_data[order_id] = order_details

    # Simulate pop-up for entering email
    return render_template('email_popup.html', order_id=order_id)

@app.route('/email-submitted/<order_id>', methods=['POST'])
def email_submitted(order_id):
    email = request.form['email']
    order_data[order_id]['email'] = email

    # Send Discord notification after collecting the email
    send_discord_notification(order_id, order_data[order_id]['tiktok_link'], order_data[order_id]['views_count'], email)

    return redirect(url_for('order_details', order_id=order_id))

@app.route('/order-details/<order_id>')
def order_details(order_id):
    order = order_data.get(order_id)
    if order:
        return render_template('order.html', order_id=order_id, tiktok_link=order['tiktok_link'], views_count=order['views_count'], email=order.get('email', ''))
    else:
        return "Order not found."

if __name__ == '__main__':
    app.run(debug=True)
