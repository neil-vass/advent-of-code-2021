
class BinaryString:
    def __init__(self, hex_str):
        self.binary = hex_to_binary(hex_str)
        self.idx = 0

    def get_next(self, count):
        result = self.binary[self.idx:self.idx+count]
        self.idx += count
        return result

    

def fetch_data(path):
    with open(path, 'r') as f:
        return f.readline().rstrip()

def hex_to_binary(hex_str):
    return ''.join(format(int(d, 16), '04b') for d in hex_str)


def get_packet_details(binary):
    packet = { 'version': int(binary.get_next(3), 2)}
    type_id = int(binary.get_next(3), 2)
 
    if type_id == 4:
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

def parse_and_sum(hex_str):
    binary = BinaryString(hex_str)
    packet = get_packet_details(binary) 
    return sum_of_version_numbers(packet)



#--------------------- tests -------------------------#

def test_hex_to_binary():
    assert hex_to_binary('D2FE28') == '110100101111111000101000'

def test_get_packet_details():
    binary = BinaryString('D2FE28')
    assert get_packet_details(binary) == {
        'version': 6, 
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
    assert parse_and_sum('D2FE28') == 6
    assert parse_and_sum('8A004A801A8002F478') == 16
    assert parse_and_sum('A0016C880162017C3686B18A3D4780') == 31

#-----------------------------------------------------#

if __name__ == "__main__":
    print(parse_and_sum(fetch_data('data/day16.txt')))
