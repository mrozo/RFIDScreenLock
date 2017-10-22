#!/bin/env python
from serial import Serial
from subprocess import call
PORT = "/dev/ttyUSB0"
channel  = Serial(port=PORT, baudrate=9600)
response = None
authorized_card = "042C5B2A592D80".lower()


def lock_pc():
    print "lock pc"
    call(["./lock.sh"])

def unlock_pc():
    print "unlock pc"
    call(["./unlock.sh"])

while True:
    response = channel.read_until("\n").strip()
    print("response :", response)
    if response.startswith("NewCard "):
        print("new card")
        new_card_id = response[len("NewCard "):]
        new_card_id =  filter(lambda char: char in '0123456789abcdef',
                              new_card_id.lower().replace('0x',''))
        print("id ", new_card_id)
        if new_card_id == authorized_card:
            unlock_pc()
    elif response == "CardRemoved":
        lock_pc()
