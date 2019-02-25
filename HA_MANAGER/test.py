# -*- coding: utf-8 -*-
import datetime
from time import sleep
import numpy as np
import sys
import json

def main():
    for i in range(1,5):
        #does thing
        timestamp = datetime.datetime.now()
        receipt = json.dumps({
                "Source": "Test",
                "Event": "Literally nothing",
                "Command": "It was a comment",
                "Time Stamp": str(timestamp),
                "Result": "Literally nothing, this is just a test"
                   })
        sys.stdout.write(receipt.encode()+"\n")
        sys.stdout.flush()
        sleep(5)
        
    return
    
if __name__ == "__main__": 
    main()