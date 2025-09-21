# CN-assignment-2-Assignment-2---Understanding-the-principles-of-RDT-Reliable-Data-Transfer-
 Reliable Data Transfer Protocols over UDP

This project implements Reliable Data Transfer (RDT) protocols at the application layer on top of the UDP transport protocol. Two classic ARQ-based protocols are developed and tested in a controlled network environment using Mininet.

⸻

🛠 Features

1. Stop-and-Wait (rdt3.0)
	•	Reliable transfer using sequence numbers and acknowledgements (ACKs).
	•	Timeout and retransmission handling for packet loss.
	•	Duplicate detection at the receiver.

2. Go-Back-N (GBN)
	•	Sliding window protocol for pipelined data transfer.
	•	Dynamic handling of different window sizes.
	•	Improved throughput over Stop-and-Wait in low-delay environments.

⸻
