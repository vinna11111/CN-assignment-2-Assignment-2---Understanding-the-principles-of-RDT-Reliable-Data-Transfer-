import socket
import struct
import time
import os

# Configuration settings
DESTINATION_IP = "10.0.0.2"
DESTINATION_PORT = 20002
PACKET_SIZE = 1024  # Size of each packet in bytes
TIMEOUT_INTERVAL = 0.100  # Timeout for ACK in seconds

# UDP socket setup
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.settimeout(TIMEOUT_INTERVAL)

# Transfer file settings
FILE_PATH = "testFile.jpg"
sequence = 0  # Packet sequence tracker
retransmissions = 0  # Retransmission counter
end_of_file_flag = 0  # Indicator for last packet

# Measure start time for throughput calculation
start_time = time.time()

# Open file to send in binary read mode
with open(FILE_PATH, "rb") as file:
    while True:
        # Read data for packet, reserving space for header
        data_block = file.read(PACKET_SIZE - 4)
        if not data_block:
            break  # Stop if no data left to send

        # Check if it’s the last data chunk
        end_of_file_flag = 1 if len(data_block) < (PACKET_SIZE - 4) else 0

        # Create packet with header: sequence number (2 bytes) and EOF flag (1 byte)
        packet_header = struct.pack("!H B", sequence, end_of_file_flag)
        packet_data = packet_header + data_block

        # Send packet and handle potential retransmissions
        while True:
            sender_socket.sendto(packet_data, (DESTINATION_IP, DESTINATION_PORT))
            print("Sent packet", sequence, "with EOF =", end_of_file_flag)

            try:
                # Wait for acknowledgment
                ack_packet, _ = sender_socket.recvfrom(PACKET_SIZE)
                received_seq, = struct.unpack("!H", ack_packet)
                
                # Check if the ACK matches the current sequence number
                if received_seq == sequence:
                    print("ACK received for packet", sequence)
                    sequence = (sequence + 1) % 2  # Toggle sequence number for stop-and-wait
                    break  # Move on to the next packet
                
            except socket.timeout:
                # Retransmit if ACK not received in time
                print("Timeout occurred for packet", sequence, "- retransmitting...")
                retransmissions += 1

# Calculate throughput
end_time = time.time()
transfer_duration = end_time - start_time
file_size_kb = os.path.getsize(FILE_PATH) / 1024  # Convert file size to KB
throughput_kbps = file_size_kb / transfer_duration  # Throughput in KB/s

# Display summary of results
print("\nFile transfer complete.")
print("=" * 50)
print("Total Retransmissions:", retransmissions)
print("Average Throughput: {:.2f} KB/s".format(throughput_kbps))
print("=" * 50)

# Close the socket
sender_socket.close()
