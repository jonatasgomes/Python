import requests
from dotenv import load_dotenv
import os
from datetime import datetime

def send_pushover_notification(
    message,
    title="Trading Alert",
    user_key=None,
    api_token=None,
    priority=0,
    sound="cashregister",
    url=None,
    url_title=None,
    device=None
):
    """
    Send a push notification via Pushover API
    
    Args:
        message (str): The notification message (required)
        title (str): Title of the notification (default: "Trading Alert")
        user_key (str): Your Pushover user key (required)
        api_token (str): Your Pushover application API token (required)
        priority (int): -2=lowest, -1=low, 0=normal, 1=high, 2=emergency (default: 0)
        sound (str): Notification sound (default: "cashregister")
        url (str): Optional supplementary URL
        url_title (str): Optional title for the URL
        device (str): Optional specific device name to send to
    
    Returns:
        dict: Response from Pushover API with status and request info
    """
    
    # Pushover API endpoint
    api_url = "https://api.pushover.net/1/messages.json"
    
    # Build the payload
    payload = {
        "token": api_token,
        "user": user_key,
        "message": message,
        "title": title,
        "priority": priority,
        "sound": sound,
        "timestamp": int(datetime.now().timestamp())
    }
    
    # Add optional parameters if provided
    if url:
        payload["url"] = url
    if url_title:
        payload["url_title"] = url_title
    if device:
        payload["device"] = device
    
    # For emergency priority (2), add retry and expire parameters
    if priority == 2:
        payload["retry"] = 30  # Retry every 30 seconds
        payload["expire"] = 3600  # Stop after 1 hour
    
    try:
        response = requests.post(api_url, data=payload)
        response.raise_for_status()
        
        return {
            "success": True,
            "status_code": response.status_code,
            "response": response.json()
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }


# Example usage for trading notifications:
def notify_order_executed(symbol, action, quantity, price, user_key, api_token):
    """
    Send notification when a trading order is executed
    """
    message = f"{action.upper()} {quantity} shares of {symbol} at ${price:.2f}"
    
    result = send_pushover_notification(
        message=message,
        title="Order Executed ✅",
        user_key=user_key,
        api_token=api_token,
        priority=1,  # High priority for trade executions
        sound="cashregister"
    )
    
    return result


if __name__ == "__main__":
    load_dotenv()
    USER_KEY = os.getenv("PUSHOVER_USER_KEY")
    API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")
    
    notify_order_executed(
        symbol="TSLA",
        action="BUY",
        quantity=10,
        price=242.50,
        user_key=USER_KEY,
        api_token=API_TOKEN
    )
