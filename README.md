📌 Repository Description (GitHub “About” section)

A hands-on Windows buffer overflow exploitation lab using Vulnserver and Immunity Debugger.
This repository documents the full exploit development process—from fuzzing to EIP control—using Python scripts and classic exploit development techniques.


📘 Repository Documentation (README.md)

# Windows Buffer Overflow Exploitation (Vulnserver)

This repository contains Python scripts and documentation demonstrating a classic stack-based buffer overflow exploitation workflow against the vulnerable Windows application Vulnserver.

The project focuses on understanding how memory corruption occurs, how control over execution flow is achieved, and how exploits are developed step by step using debugging tools.

⚠️ Educational use only. This software and techniques must not be used against systems you do not own or have explicit permission to test.


🎯 Objectives

- Understand stack memory layout (ESP, EBP, EIP)
- Perform fuzzing to identify crash points
- Calculate the exact offset to overwrite EIP
- Gain control of the instruction pointer
- Prepare for shellcode execution
- Learn Windows exploit development fundamentals


🧰 Environment & Tools

Target Machine
- Windows 10
- Vulnserver (v1.00)
- Immunity Debugger
- Mona.py plugin

Attacker Machine
- Kali Linux
- Python 3
- Metasploit pattern tools


🧠 Vulnerable Application: Vulnserver

Vulnserver is a deliberately vulnerable Windows TCP server used for exploit development training.

- Default port: 9999
- Vulnerable command used: TRUN
- Vulnerability type: Stack-based buffer overflow


📂 Repository Structure

.
├── fuzzing.py           # Fuzzer to trigger application crash
├── pattern_send.py      # Sends cyclic pattern to find EIP offset
├── crush_EIP.py         # Confirms EIP control using BBBB
├── README.md            # Documentation


🧪 Exploitation Workflow

1️⃣ Fuzzing

The fuzzing script sends increasingly large payloads to identify when the application crashes.

Goal:
- Confirm the application is vulnerable
- Estimate crash size

Expected result:
- Vulnserver crashes
- Immunity Debugger shows access violation


2️⃣ Offset Discovery

A cyclic pattern is sent instead of repeated characters.

Steps:
1. Generate pattern:
   pattern_create.rb -l 3000
2. Send pattern to Vulnserver
3. Observe EIP value in Immunity Debugger
4. Calculate offset:
   pattern_offset.rb -q <EIP_VALUE>

Result:
- Exact number of bytes needed to overwrite EIP


3️⃣ EIP Control Confirmation

After finding the offset, a payload is crafted:

- A * offset
- B * 4 (EIP overwrite)

If successful:
- EIP = 0x42424242

This confirms full control of execution flow.


4️⃣ Next Exploitation Steps (Not Included Yet)

- Identify a JMP ESP instruction
- Check for bad characters
- Generate shellcode (e.g. reverse shell)
- Redirect execution to shellcode


🧩 Key Concepts Covered

- Stack memory anatomy
- Instruction Pointer overwrite
- Little-endian addressing
- Debugging with Immunity
- Reliable exploit construction


⚠️ Disclaimer

This repository is strictly for educational and research purposes.

Do not:
- Attack real systems
- Use these techniques without permission
- Deploy in production environments


🧠 Author

Cybersecurity student exploring exploit development and low-level security concepts.

Learning by breaking — responsibly.
