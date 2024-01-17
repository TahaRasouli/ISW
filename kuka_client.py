import xml.etree.ElementTree as ET
from datetime import datetime
import paho.mqtt.client as mqtt
import time
import socket


##### SETTINGS #####
### udp
udp_server_host = '127.0.0.1'
udp_server_port = 12345
message_to_send = 'Hello, server!'
udp_client_interval = 5
###xml
look_for_list = {"Cur", "Eff"}
look_for_list_time = {"Year", "Month", "Day", "Hour", "Min", "Sec"}
###mqtt
mqtt_broker_host = "localhost"
mqtt_broker_port = 1883
mqtt_interval = udp_client_interval
###dict
values_to_send = {
    "Eff_A1": "Robot/Eff/A1",
    "Eff_A2": "Robot/Eff/A2",
    "Eff_A3": "Robot/Eff/A3",
    "Eff_A4": "Robot/Eff/A4",
    "Eff_A5": "Robot/Eff/A5",
    "Eff_A6": "Robot/Eff/A6",
    "Eff_E1": "Robot/Eff/E1",
    "Eff_E2": "Robot/Eff/E2",

    "Cur_A1": "Robot/Cur/A1",
    "Cur_A2": "Robot/Cur/A2",
    "Cur_A3": "Robot/Cur/A3",
    "Cur_A4": "Robot/Cur/A4",
    "Cur_A5": "Robot/Cur/A5",
    "Cur_A6": "Robot/Cur/A6",
    "Cur_E1": "Robot/Cur/E1",
    "Cur_E2": "Robot/Cur/E2",

    "Unix": "Robot/Time/Stamp",
    "Load": "Robot/Load/Mass"
}


##### UDP CLIENT #####
def udp_client(host, port, message):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send data to the server
        client_socket.sendto(message.encode('utf-8'), (host, port))
        #print(f"Sent: {message}")

        # Receive data from the server
        data, server_address = client_socket.recvfrom(1024)
        decoded_data = data.decode('utf-8')
        export_message = decoded_data
        #print(f"Received from {server_address}: {decoded_data}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the socket
        client_socket.close()
        #print("Connection closed")
        return export_message


##### XML PARSING #####
def parse_xml_string(xml_string):
    value_dict = {}
    tree = ET.ElementTree(ET.fromstring(xml_string))
    root = tree.getroot()

    for child in root:
        # <tag>value</tag>
        # result tag=value
        if len(child.attrib) == 0:
            key = child.tag
            value = child.text
            value_dict[key] = value

        # <tag key="value"></tag>
        # result tag_key=value
        for attribute in child.attrib:
            key = child.tag + '_' + attribute
            value = child.attrib.get(attribute)
            value_dict[key] = value

    # convert time info into unix timestamp
    year_str = value_dict.get('Year')
    month_str = value_dict.get('Month')
    day_str = value_dict.get('Day')
    hour_str = value_dict.get('Hour')
    min_str = value_dict.get('Min')
    sec_str = value_dict.get('Sec')

    year = int(year_str.split('.', 1)[0])
    month = int(month_str.split('.', 1)[0])
    day = int(day_str.split('.', 1)[0])
    hour = int(hour_str.split('.', 1)[0])
    min = int(min_str.split('.', 1)[0])
    sec = int(sec_str.split('.', 1)[0])

    dt = datetime(year, month, day, hour, min, sec)
    timestamp = dt.timestamp()
    value_dict["Unix"] = timestamp

    # delete old time from dict
    for time_element in look_for_list_time:
        value_dict.pop(time_element)

    #print("result of xml parsing")
    print(value_dict)
    return value_dict


##### MQTT PUBLISH #####
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def mqtt_pub(client, value_dict):
    for key in values_to_send:
        try:
            client.publish(values_to_send[key], value_dict[key])
            print(f"Sent: {value_dict[key].__str__()}  -  in Topic {values_to_send[key].__str__()}")
        except:
            print("no value for >>" + key + "<<")


##### MAIN #####
def repeat_kuka_client(udp_host, udp_port, message, mqtt_host, mqtt_port , interval):
    while True:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)

        # access udp erver
        udp_message = udp_client(udp_host, udp_port, message)

        # convert xml-string to dictionary of values
        value_dict = parse_xml_string(udp_message)

        # Create an MQTT client instance
        client = mqtt.Client()
        client.on_connect = on_connect
        # Connect to the broker
        client.connect(mqtt_host, mqtt_port, 60)
        # Wait for the connection to be established
        time.sleep(1)
        # Publish
        mqtt_pub(client, value_dict)

        # Sleep
        time.sleep(interval)


# Run the client repeatedly
repeat_kuka_client(udp_server_host,
                   udp_server_port,
                   message_to_send,
                   mqtt_broker_host,
                   mqtt_broker_port,
                   udp_client_interval)
