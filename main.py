import sys
import os
import re
import subprocess
import qrcode
import pathlib


def run_command(command):

    output, _ = subprocess.Popen(
    command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True).communicate()
    return output.decode("cp1252").rstrip('\r\n')


def find_ssid():

    ssid = run_command("netsh wlan show interfaces | findstr SSID")
    ssid = re.findall(r"[^B]SSID\s+:\s(.*)", ssid)[0]
    return ssid


def get_password(ssid):

    password = run_command( f"netsh wlan show profile name=\"{ssid}\" key=clear | findstr Key")
    password = re.findall(r"Key Content\s+:\s(.*)", password)[0]
    return password


def generate_qr_code(ssid, password):
    wifiadress = f"WIFI:T:WPA;S:{ssid};P:{password};;"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,)
    qr.add_data(wifiadress)
    img = qr.make_image()
    img.save("wifi.png")
    img.show()

def main():
    ssid = find_ssid()
    password = get_password(ssid)
    generate_qr_code(ssid,password)

if __name__=="__main__":
    main()





