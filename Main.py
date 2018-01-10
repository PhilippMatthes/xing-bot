from Log import Log
from Driver import Driver
from time import sleep
import traceback
import sys
import os
import errno
from socket import error as socket_error


def loop():
    while True:
        message = Log.get_current_message()
        if message == "Start" or message == "Continue":
            try:
                driver = Driver()
                driver.run()


            except KeyboardInterrupt:
                Log.send("Keyboard Interrupt. Bot will exit now.")
                print("Exiting...")
                break
            except socket_error as err:
                raise err
            except Exception as err:
                for frame in traceback.extract_tb(sys.exc_info()[2]):
                    fname, lineno, fn, text = frame
                error = "Error in " + str(fname) + " on line " + str(lineno) + ": " + str(err)
                print(error)
                Log.send(error)
                pass
        else:
            if message == "Stop" or message == "Exit":
                Log.send("XING Bot will exit now.")
                raise Exception
            sleep(1)


def run():
    while True:
        try:
            Log.send("XING Bot started. Please send >>Start<< to start")
            loop()
        except socket_error as err:
            if err.errno != errno.ECONNREFUSED:
                raise err


if __name__ == "__main__":
    os.makedirs("./log", exist_ok=True)

    run()
