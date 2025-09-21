import socket
import struct
import time

# Configuration parameters
listen_ip = "10.0.0.2"
listen_port = 20002
max_buffer_size = 1024  # Maximum size of each packet
receive_timeout = 5  # Timeout duration for receiving packets

# Create a UDP socket for incoming data
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind((listen_ip, listen_port))
receiver_socket.settimeout(receive_timeout)  # Set a timeout for packet reception

print("Receiver is active, waiting for incoming packets...")

# Initialize the sequence number expected
next_expected_seq = 0

# Open a file to write the incoming data
with open("received_image.png", "wb") as output_file:
    while True:
        try:
            # Wait for a packet to arrive
            incoming_packet, sender_address = receiver_socket.recvfrom(max_buffer_size)

            # Extract the sequence number and EOF flag from the packet header
            header = incoming_packet[:3]
            sequence_number, eof_flag = struct.unpack("!H B", header)
            payload = incoming_packet[3:]  # The actual data portion

            print("Received packet {} with EOF={}".format(sequence_number, eof_flag))

            if sequence_number == next_expected_seq:
                # Write the data to the output file
                output_file.write(payload)

                # Acknowledge the receipt of the current packet
                ack_response = struct.pack("!H", sequence_number)
                receiver_socket.sendto(ack_response, sender_address)
                print("Sent ACK for packet {}".format(sequence_number))

                # Update the expected sequence number for the next packet
                next_expected_seq += 1

                # Check if this is the final packet
                if eof_flag == 1:
                    print("Received the final packet. Stopping transmission.")
                    break
            else:
                # Handle out-of-order packets by resending the last ACK
                print("Received out-of-order packet {}. Expected {}.".format(sequence_number, next_expected_seq))
                ack_response = struct.pack("!H", next_expected_seq - 1)
                receiver_socket.sendto(ack_response, sender_address)
                print("Resent ACK for packet {}".format(next_expected_seq - 1))

        except socket.timeout:
            # Timeout reached; terminate the receiver
            print("No packets received for the last {} seconds. Closing receiver.".format(receive_timeout))
            break

# Confirm successful file reception
print("File transfer completed successfully.")
receiver_socket.close()
