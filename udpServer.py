import socket
import time

def udp_server(host, port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))
    print(f"UDP server listening on {host}:{port}")

    while True:
        # Receive data from the client
        data, client_address = server_socket.recvfrom(1024)

        # Process the received data
        print(f"Received data from {client_address}: {data.decode('utf-8')}")

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)

        # Send a response back to the client
        #response = "hello, client!"
        response = '''<RobotState><Pos A1="60.890797" A2="-113.357620" A3="89.076561" A4="131.657974" A5="-39.360229" A6="6.198111" E1="-1848.092041" E2="-0.193168"></Pos><Vel A1="0.038153" A2="0.076306" A3="0.057222" A4="0.057208" A5="-0.038139" A6="0.057222" E1="-0.057222" E2="0.000000"></Vel><Eff A1="-54.349907" A2="-4122.706543" A3="-3479.158691" A4="-191.162201" A5="-23.224775" A6="-63.180576" E1="-62.142090" E2="-138.485306"></Eff><Cur A1="-0.225914" A2="12.467839" A3="9.803446" A4="1.069515" A5="-0.118835" A6="-0.593081" E1="-0.319272" E2="0.799129"></Cur><Year>2023.000000</Year><Month>12.000000</Month><Day>12.000000</Day><Hour>20.000000</Hour><Min>41.000000</Min><Sec>18.000000</Sec><Load>420.000000</Load><RobotCommand Size="0"></RobotCommand></RobotState>'''
        #response = '<RobotState><Month>12.000000</Month></RobotState>'
        server_socket.sendto(response.encode('utf-8'), client_address)

if __name__ == "__main__":
    # Specify the host and port for the server
    host = "127.0.0.1"  # Use "0.0.0.0" for all available interfaces
    port = 12345

    udp_server(host, port)
