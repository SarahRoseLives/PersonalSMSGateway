# SMS Gateway App

## Overview

This application runs a socket server on your phone that listens for a message and number to send. This allows you to use your real phone to send messages in a programatic way.

## Installation

Grab the apk from the bin folder, once it's open, run the example command with your devices IP address.

## Usage

Once the app is running, it will start a socket server listening for incoming SMS requests on your local IP address at port 5000. You can send messages to this server using any terminal.

### Sending a Message from the Terminal

To send a message, you can use the `netcat` command. Here’s the syntax:

```bash
echo '{"to_number": "1234567890", "message_body": "Hello from the terminal!"}' | nc YOUR_IP 5000
```

Replace `YOUR_IP` with the IP address of the machine running the SMS Gateway App.

### Successful Message Response

Upon successful sending of the message, you will receive a JSON response similar to the following:

```json
{
    "status": "success",
    "recipient": "1234567890",
    "message": "Hello from the terminal!"
}
```

## Using Python to Send messages to multiple numbers

```python
import socket
import json

# Replace with the actual IP address of the machine running the SMS Gateway App
SERVER_IP = "YOUR_IP"  # e.g., "192.168.1.10"
SERVER_PORT = 5000

# List of recipients and message body
recipients = ["1234567890", "0987654321", "1122334455"]
message_body = "Hello to all recipients!"

def send_sms(to_number, message_body):
    # Create a socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_IP, SERVER_PORT))
        
        # Prepare the JSON payload
        payload = {
            "to_number": to_number,
            "message_body": message_body
        }
        
        # Send the payload as a JSON string
        sock.sendall(json.dumps(payload).encode('utf-8'))
        
        # Receive the response
        response = sock.recv(1024)
        print(response.decode('utf-8'))

# Send messages to each recipient
for number in recipients:
    send_sms(number, message_body)

```

## Dependencies

Make sure you have the following dependencies installed:

- Kivy
- KivyMD
- Plyer

You can install the dependencies using pip:

```bash
pip install kivy kivymd plyer
```

