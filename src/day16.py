import math

class BinaryString:
    def __init__(self, hex_str):
        self.binary = ''.join(format(int(d, 16), '04b') for d in hex_str)
        self.idx = 0

    def get_next(self, count):
        result = self.binary[self.idx:self.idx+count]
        self.idx += count
        return result

    
def fetch_data(path):
    with open(path, 'r') as f:
        return f.readline().rstrip()

def get_packet_details(binary):
    packet = {
        'version': int(binary.get_next(3), 2),
        'type': int(binary.get_next(3), 2)
    }
 
    if packet['type'] == 4:
        val = ''
        got_last_packet = False
        while not got_last_packet:
            chunk = binary.get_next(5)
            if chunk[0] == '0':
                got_last_packet = True
            val += chunk[1:]
        packet['value'] = int(val, 2)
    
    else:
        packet['subs'] = []
        length_type = binary.get_next(1)
        if length_type == '0':
            length_of_subs = int(binary.get_next(15), 2)
            target_idx = binary.idx + length_of_subs

            while binary.idx < target_idx:
                packet['subs'].append(get_packet_details(binary))
        else:
            number_of_subs = int(binary.get_next(11), 2)
            for _ in range(number_of_subs):
                packet['subs'].append(get_packet_details(binary))

    return packet

def sum_of_version_numbers(packet):
    subs = packet.get('subs',[])
    return packet['version'] + sum(sum_of_version_numbers(s) for s in subs)


def run_operations(packet):
    op = packet['type']
    if op == 4:
        return packet['value']
    
    subs = [run_operations(s) for s in packet['subs']]
    if op == 0:
        return sum(subs)
    elif op == 1:
        return math.prod(subs)
    elif op == 2:
        return min(subs)
    elif op == 3:
        return max(subs)
    elif op == 5: 
        return subs[0] > subs[1]
    elif op == 6: 
        return subs[0] < subs[1]
    elif op == 7: 
        return subs[0] == subs[1]


def parse_and_run(hex_str, method):
    binary = BinaryString(hex_str)
    packet = get_packet_details(binary) 
    return method(packet)



#--------------------- tests -------------------------#

def test_hex_to_binary():
    binary = BinaryString('D2FE28')
    assert binary.binary == '110100101111111000101000'

def test_get_packet_details():
    binary = BinaryString('D2FE28')
    assert get_packet_details(binary) == {
        'version': 6, 
        'type': 4,
        'value': 2021
    }

def test_get_packet_and_subs_by_length_in_bits():
    binary = BinaryString('38006F45291200')
    packet = get_packet_details(binary) 
    assert packet['version'] == 1
    assert len(packet['subs']) == 2
    assert packet['subs'][0]['value'] == 10
    assert packet['subs'][1]['value'] == 20

def test_get_packet_and_subs_by_number_of_subs():
    binary = BinaryString('EE00D40C823060')
    packet = get_packet_details(binary) 
    assert packet['version'] == 7
    assert [s['value'] for s in packet['subs']] == [1, 2, 3]

def test_sum_of_version_numbers():
    assert parse_and_run('D2FE28', sum_of_version_numbers) == 6
    assert parse_and_run('8A004A801A8002F478', sum_of_version_numbers) == 16
    assert parse_and_run('A0016C880162017C3686B18A3D4780', sum_of_version_numbers) == 31

def test_run_operations():
    assert parse_and_run('C200B40A82', run_operations) == 3
    assert parse_and_run('04005AC33890', run_operations) == 54
    assert parse_and_run('880086C3E88112', run_operations) == 7
    assert parse_and_run('CE00C43D881120', run_operations) == 9
    assert parse_and_run('D8005AC2A8F0', run_operations) == 1
    assert parse_and_run('F600BC2D8F', run_operations) == 0
    assert parse_and_run('9C005AC2F8F0', run_operations) == 0
    assert parse_and_run('9C0141080250320F1802104A08', run_operations) == 1


#-----------------------------------------------------#

if __name__ == "__main__":
    hex_str = fetch_data('data/day16.txt')
    print(parse_and_run(hex_str, run_operations))
