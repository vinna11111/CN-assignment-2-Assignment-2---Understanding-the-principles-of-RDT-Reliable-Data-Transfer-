import socket
import struct

# Configuration settings
LOCAL_IP = "10.0.0.2"
LOCAL_PORT = 20002
BUFFER_SIZE = 1024  # Size of each packet in bytes

# Initialize UDP socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind((LOCAL_IP, LOCAL_PORT))

print("Receiver started, waiting for packets...")

expected_sequence = 0  # Expected sequence number for incoming packets

# Open file to write the received data
with open("received_testFile.jpg", "wb") as output_file:
    while True:
        # Receive packet
        packet, sender_address = receiver_socket.recvfrom(BUFFER_SIZE)
        
        # Extract header
        header = packet[:3]
        sequence_number, eof_flag = struct.unpack("!H B", header)
        data = packet[3:]  # Extract data from the packet

        # Check if the received packet is the expected one
        if sequence_number == expected_sequence:
            print("Received packet {} with EOF={}".format(sequence_number, eof_flag))
            output_file.write(data)  # Write the received data to the file
            
            # Send ACK for the received packet
            ack_packet = struct.pack("!H", sequence_number)
            receiver_socket.sendto(ack_packet, sender_address)
            print("Sent ACK for packet {}".format(sequence_number))
            
            # Update expected sequence number
            expected_sequence = (expected_sequence + 1) % 2
            
            # Check for EOF flag to determine if the transmission is complete
            if eof_flag == 1:
                print("Received EOF packet. Ending transmission.")
                break
        else:
            # Handle out-of-order packets by resending the last ACK
            print("Out-of-order packet {} received. Expected {}.".format(sequence_number, expected_sequence))
            ack_packet = struct.pack("!H", (expected_sequence - 1) % 2)  # Resend ACK for the last valid packet
            receiver_socket.sendto(ack_packet, sender_address)
            print("Resent ACK for packet {}".format((expected_sequence - 1) % 2))

# Final confirmation after receiving the file
print("File transfer completed successfully.")
receiver_socket.close()
