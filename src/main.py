import datetime
import time
from urllib.parse import urlparse, parse_qs
import cv2
from pyzbar.pyzbar import decode
import pyotp

def read_qr_code(image_path):
    try:
        # Load the image
        image = cv2.imread(image_path)
        # Convert the image to grayscale for better processing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect QR codes in the image
        qr_codes = decode(gray)
        # Extract data from the first detected QR code (if any)
        if qr_codes:
            qr_data = qr_codes[0].data.decode('utf-8')
            return qr_data
        else:
            return None
    except Exception as e:
        print(f"Error reading QR code: {e}")
        return None
def extract_query_params(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params

def loop_otp(secret:str, period:int, digits: int):
    totp = pyotp.TOTP(secret, interval=period, digits=digits)
    while True:
        otp = totp.now()
        current_time = datetime.datetime.now()
        period_start_time = (current_time.timestamp() // period) * period
        period_end_time = period_start_time + period
        otp_next = totp.at(int(period_end_time) + 1)
        while current_time.timestamp() < period_end_time:
            # Calculate remaining seconds
            remaining_seconds = int(period_end_time - current_time.timestamp())

            # Print the OTP and the remaining seconds
            print(f"\rOTP: {otp} expires in {remaining_seconds} seconds", end='')
            if remaining_seconds < 5:
                print(f". Next OPT is {otp_next}", end='')
            time.sleep(1)
            current_time = datetime.datetime.now()
        print(f"\rOTP: {otp} expired", end='\n')
if __name__ == '__main__':
    # print('hello')
    image_path = "../tmp/totp_secret_vpn_astratech.png"
    qr_data = read_qr_code(image_path)

    if qr_data:
        # print("Decoded QR code data:", qr_data)
        data_map = extract_query_params(qr_data)
        # print("totp data: {}".format(data_map))
        secret = data_map['secret'][0]
        period = int(data_map['period'][0])
        digits = int(data_map['digits'][0])
        loop_otp(secret, period, digits)

    else:
        print("No QR code found in the image.")