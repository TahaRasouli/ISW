import subprocess
import time

applications = [
    r"C:\Users\Taha\Desktop\Python Dockerzied\kuka_client.py",
    r"C:\Users\Taha\Desktop\Python Dockerzied\udpServer.py",
]

def open_applications(app_list):
    for app in app_list:
        subprocess.Popen(["python.exe", app])
        time.sleep(1)  # Adjust the delay if needed

if __name__ == "__main__":
    open_applications(applications)