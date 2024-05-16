import struct
"""
Parse a pcap file and count the number of connections initiated and acknowledged.
Determine which percentage of connections were acknowledged.

Pcap file structure:
┌──────────────────────────────────────────────┐
│                pcap header                   │ 24 bytes
├──────────────────────────────────────────────┤
│ per_packet_header (pcap_sf_pkthdr)           │ 16 bytes  
│ ───────────────────────────────────────────  │
│ packet_data                                  │       
│   ll_header                                  │ 4 bytes      
│   ip_header                                  │ 20 bytes (without options)
│   tcp_header                                 │ 20 bytes (without options)          
├──────────────────────────────────────────────┤
│ per_packet_header (pcap_sf_pkthdr) 16 bytes  │   
│ ───────────────────────────────────────────  │
│ packet_data                                  │   
|   ll_header                                  │       
│   ip_header                                  │         
│   tcp_header                                 │            
├──────────────────────────────────────────────┤
"""

with open('./synflood.pcap', 'rb') as file:
  # "<"" = little-endian, "I" = unsigned int, "H" = unsigned short
  magic_number, major_version, minor_version, _, _, _, llheader_type = struct.unpack('<IHHIIII', file.read(24))

  pcap_magic_number = 0xa1b2c3d4
  assert magic_number == pcap_magic_number, f"Magic number {magic_number} is not equal to {pcap_magic_number}"
  print(f"Pcap file version: {major_version}.{minor_version}")
  assert llheader_type == 0 # loopback header type

  packets_read = 0
  inited_connections = 0
  acked_connections = 0

  while True:
    per_packet_header = file.read(16)
    if not per_packet_header:
        break
    
    packets_read += 1
    _, _, packet_len, untruc_len = struct.unpack('<IIII', per_packet_header)
    assert packet_len == untruc_len # no truncation
    packet = file.read(packet_len)
    # assert struct.unpack('<I', packet[:4])[0] == 2 # ipv4 for loopback link layer header https://www.tcpdump.org/linktypes/LINKTYPE_NULL.html 
    #  link_layer_header = packet[:4]
    ip_version, internet_header_length = packet[4] >> 4, packet[4] & 0x0F
    assert ip_version == 4 # ipv4
    assert internet_header_length == 5 # 5 * 4 bytes = 20 bytes for ipv4 header without options

    tcp_header = packet[24:38] # read until the flags
    source_port, dest_port, _, _, flags = struct.unpack('!HHIIH', tcp_header)

    syn_flag = (flags & 0x02) > 0
    ack_flag = (flags & 0x10) > 0

    inited_connections += 1 if dest_port == 80 and syn_flag else 0
    acked_connections += 1 if source_port == 80 and ack_flag else 0

    print(f'{source_port} -> {dest_port} {syn_flag and " SYN" or ""}{ack_flag and " ACK" or ""}')

    
  print(f"Packets parsed {packets_read}")
  print(f"Connections initiated {inited_connections}")
  print(f"Connections acknowledged: {(acked_connections / inited_connections * 100):0.2f}%")
