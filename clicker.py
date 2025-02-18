import time
import pyautogui
import psutil
import os
import signal
import logging

# Generate the reference image
# screenshot = pyautogui.screenshot(region=(414-25,148-13, 50, 26))
# screenshot.save("reference.png")

# Locate the reference image on the screen

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Hello")
logging.info("Start the script")

def get_is_button_on():
    try:
        location = pyautogui.locateCenterOnScreen('reference-on.png')
    except pyautogui.ImageNotFoundException:
        return
    return location

def get_is_button_off():
    try:
        location = pyautogui.locateCenterOnScreen('reference-off.png')
    except pyautogui.ImageNotFoundException:
        return
    return location

def send_signal(procname, sig=signal.SIGSTOP):
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Check if process name contains the given substring
            if procname in proc.info['name']:
                logging.info(f"Sending signal {sig} to process {proc.info['name']} (PID: {proc.info['pid']})")
                try:
                    os.kill(proc.info['pid'], sig)
                except PermissionError:
                    pass
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    logging.info(f"Sent to '{procname}'")
    return False


while True:
    # Wakeup the process
    send_signal("corplink", sig=signal.SIGCONT)
    time.sleep(8)

    # Turn on the button
    if location := get_is_button_on():
        # Need to turn off firstly
        logging.info("Turn off the button")
        pyautogui.click(location)
        time.sleep(8)
    else:
        location = get_is_button_off()
        if not location:
            logging.info("Reference image not found on the screen.")
            break

    # Turn on
    logging.info("Turn on the button")
    pyautogui.click(location)
    time.sleep(8)
    send_signal("corplink", sig=signal.SIGSTOP)
    time.sleep(60 * 60 * 18)  # Toggle every 10 hours
