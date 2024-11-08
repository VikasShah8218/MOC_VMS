from pyModbusTCP.client import ModbusClient
import time
delay = 0.2

class AdamService:
        @staticmethod
        def connect_modbus(host, port):
            modbus_client = ModbusClient(host=host, port=port)
            if not modbus_client.open():
                raise ConnectionError(f"Failed to connect to Modbus at {host}:{port}")
            return modbus_client

        @staticmethod
        def close_modbus(modbus_client):
            if modbus_client:
                modbus_client.close()

        @staticmethod
        def read_coils(modbus_client, address):
            if modbus_client:
                coils = modbus_client.read_coils(address)
                return coils
            return None

        @staticmethod
        def write_coils(modbus_client, address, values):
            if modbus_client:
                result = modbus_client.write_multiple_coils(address, values)
                return result
            return None
        
def activate(ip,address1):
    port  = 502
    print(ip,"       ",port, "        " ,address1)  
    return True  
    try:
        modbus_client = AdamService.connect_modbus(ip, int(port))
        coil_status = AdamService.read_coils(modbus_client, address1)[0]
        if coil_status:
            a = AdamService.write_coils(modbus_client, address1, [False])
            time.sleep(delay)
            a = AdamService.write_coils(modbus_client, address1, [True])
            time.sleep(delay)
            a = AdamService.write_coils(modbus_client, address1, [False])
            return a
        else:
            a = AdamService.write_coils(modbus_client, address1, [True])
            time.sleep(delay)
            a = AdamService.write_coils(modbus_client, address1, [False])
            return a
    except Exception as e:
        print(str(e))
        return False









