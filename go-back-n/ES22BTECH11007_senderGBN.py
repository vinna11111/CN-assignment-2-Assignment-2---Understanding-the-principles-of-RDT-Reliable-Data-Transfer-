import socket
import time
import struct
import os

# Configuration settings
destination_ip = "10.0.0.1"
destination_port = 20001
ack_address = ("10.0.0.2", 20002)
packet_size = 1024  # Maximum size of each data packet
window_size =256 # Size of the sender's window
ack_wait_time = 0.015  # Acknowledgment timeout in seconds

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Sliding window state variables
base_sequence = 0
next_sequence = 0
end_of_file = 0  # End-of-file indicator
retransmission_count = 0  # Number of retransmissions
start_time = time.time()  # Track transfer start time
file_name = "testFile.jpg"

# Open the specified file in binary read mode
with open(file_name, "rb") as file:
    while True:
        # Fill the window with packets
        while next_sequence < base_sequence + window_size:
            # Read data for one packet
            packet_data = file.read(packet_size - 4)  # Reserve 4 bytes for the header
            if not packet_data:
                end_of_file = 1  # Mark EOF if there's no more data
                break

            # Construct packet with header (2 bytes for sequence number, 1 byte for EOF flag)
            header = struct.pack("!H B", next_sequence, end_of_file)
            packet = header + packet_data
            
            # Send the packet
            sock.sendto(packet, ack_address)
            print("Sent packet {} with EOF={}".format(next_sequence, end_of_file))
            next_sequence += 1
            
            if end_of_file == 1:
                break

        # Wait for ACKs for packets in the current window
        while base_sequence < next_sequence:
            try:
                # Receive ACK with a timeout
                sock.settimeout(ack_wait_time)
                ack_response, _ = sock.recvfrom(1024)
                ack_sequence = struct.unpack("!H", ack_response)[0]

                if ack_sequence >= base_sequence:
                    print("Received ACK for packet {}".format(ack_sequence))
                    base_sequence = ack_sequence + 1  # Move the base of the window up
                else:
                    print("Duplicate ACK for packet {}".format(ack_sequence))

            except socket.timeout:
                # Timeout; retransmit all unacknowledged packets
                print("Timeout. Resending packets starting from sequence {}".format(base_sequence))
                for seq in range(base_sequence, next_sequence):
                    packet_data = file.read(packet_size - 4)  # Read data for retransmission
                    packet = struct.pack("!H B", seq, 0) + packet_data
                    sock.sendto(packet, ack_address)
                    retransmission_count += 1
                    print("Resent packet {}".format(seq))

        # Exit if EOF was reached and all packets acknowledged
        if end_of_file == 1:
            break

# Calculate transfer metrics
end_time = time.time()
transfer_time = end_time - start_time
file_size_kb = os.path.getsize(file_name) / 1024
transfer_rate = file_size_kb / transfer_time

# Display final statistics
print("\nTransfer complete.")
print("=" * 50)
print("Total Retransmissions: {}".format(retransmission_count))
print("Average Throughput: {:.2f} KB/s".format(transfer_rate))
print("=" * 50)

# Close the socket
sock.close()
