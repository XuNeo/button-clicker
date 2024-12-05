import time
import pyautogui
import psutil
import os
import signal

# Generate the reference image
# screenshot = pyautogui.screenshot(region=(414-25,148-13, 50, 26))
# screenshot.save("reference.png")

# Locate the reference image on the screen

print("Start the script", flush=True)

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
                print(f"Sending signal {sig} to process {proc.info['name']} (PID: {proc.info['pid']})")
                try:
                    os.kill(proc.info['pid'], sig)
                except PermissionError:
                    pass
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print(f"Sent to '{procname}'")
    return False


while True:
    # Wakeup the process
    send_signal("corplink", sig=signal.SIGCONT)
    time.sleep(5)

    # Turn on the button
    if location := get_is_button_on():
        # Need to turn off firstly
        print("Turn off the button", flush=True)
        pyautogui.click(location)
        time.sleep(5)
    else:
        location = get_is_button_off()
        if not location:
            print("Reference image not found on the screen.")
            break

    # Turn on
    print("Turn on the button", flush=True)
    pyautogui.click(location)
    time.sleep(5)
    send_signal("corplink", sig=signal.SIGSTOP)
    time.sleep(60 * 60 * 10)  # Toggle every 10 hours
