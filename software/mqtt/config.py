from configparser import ConfigParser
from os.path import exists
from getpass import getpass

CONFIG_FILENAME = 'mqtt_config.ini'

def create_config ():
    print("Please enter your MQTT Broker information:")    
    config_object = ConfigParser()
    config_object["MQTTBrokerInfo"] = {
        "broker_ip": input("\tEnter broker ip: "),
        "username": input("\tEnter username: "),
        "password": getpass("\tEnter password: ")
    }

    with open(CONFIG_FILENAME, 'w') as conf:
        config_object.write(conf)

def get_config():
    # Read config file
    config_object = ConfigParser()
    config_object.read(CONFIG_FILENAME)
    return config_object

    # Convert to dictionary
    # Reference: https://stackoverflow.com/questions/1773793/convert-configparser-items-to-dictionary
    # return {s:dict(config_object.items(s)) for s in config_object.sections()}
    """
    The above line is useful for converting a config object with multiple sections into
    a dictionary, but since I only have 1 section at the moment, the dictionary is probably
    bigger than it needs to be. I'll have to fix this.
    """


# DEBUG
if __name__ == '__main__':
    if not exists(CONFIG_FILENAME):
        print("Looks like this is the first time you ran the server.")
        create_config()

    mqtt_info = get_config()["MQTTBrokerInfo"]
    print(f'Config: {mqtt_info}')
    print(f'IP: {mqtt_info["broker_ip"]}')
    print(f'User: {mqtt_info["username"]}')
    print(f'Pass: {mqtt_info["password"]}')