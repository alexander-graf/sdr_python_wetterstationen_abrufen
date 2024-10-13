# RTL-SDR Signal Analyzer

## English

### Description
This program is a GUI-based signal analyzer for RTL-SDR devices. It uses the rtl_433 tool to decode various wireless protocols and displays the received data in real-time.

### Prerequisites
- Linux-based operating system
- RTL-SDR USB dongle
- Python 3.6 or higher
- GTK+ 3.0 or higher

### Installation

#### Ubuntu/Debian:
1. Install required packages:
   ```
   sudo apt update
   sudo apt install python3 python3-pip python3-gi gir1.2-gtk-3.0 rtl-sdr librtlsdr-dev
   ```
2. Install rtl_433:
   ```
   sudo apt install rtl-433
   ```

#### Fedora:
1. Install required packages:
   ```
   sudo dnf install python3 python3-pip python3-gobject gtk3 rtl-sdr
   ```
2. Install rtl_433:
   ```
   sudo dnf install rtl-433
   ```

#### Arch Linux:
1. Install required packages:
   ```
   sudo pacman -S python python-pip python-gobject gtk3 rtl-sdr
   ```
2. Install rtl_433 from AUR:
   ```
   yay -S rtl_433
   ```

### Setting up the project
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rtl-sdr-signal-analyzer.git
   cd rtl-sdr-signal-analyzer
   ```
2. Install Python dependencies:
   ```
   pip3 install -r requirements.txt
   ```

### Usage
1. Connect your RTL-SDR dongle to your computer.
2. Run the program:
   ```
   python3 main.py
   ```
3. The GUI will open. Click "Start" to begin receiving and analyzing signals.
4. Received data will be displayed in the main window and logged to 'zur_analyse.txt'.

### Troubleshooting
- If you encounter permission issues with the RTL-SDR device, add your user to the 'plugdev' group:
  ```
  sudo usermod -a -G plugdev $USER
  ```
  Then log out and log back in for the changes to take effect.

- If rtl_433 is not found, ensure it's installed and in your system PATH.

## Deutsch

### Beschreibung
Dieses Programm ist ein GUI-basierter Signalanalysator für RTL-SDR-Geräte. Es verwendet das rtl_433-Tool zum Dekodieren verschiedener Funkprotokolle und zeigt die empfangenen Daten in Echtzeit an.

### Voraussetzungen
- Linux-basiertes Betriebssystem
- RTL-SDR USB-Dongle
- Python 3.6 oder höher
- GTK+ 3.0 oder höher

### Installation

#### Ubuntu/Debian:
1. Installiere erforderliche Pakete:
   ```
   sudo apt update
   sudo apt install python3 python3-pip python3-gi gir1.2-gtk-3.0 rtl-sdr librtlsdr-dev
   ```
2. Installiere rtl_433:
   ```
   sudo apt install rtl-433
   ```

#### Fedora:
1. Installiere erforderliche Pakete:
   ```
   sudo dnf install python3 python3-pip python3-gobject gtk3 rtl-sdr
   ```
2. Installiere rtl_433:
   ```
   sudo dnf install rtl-433
   ```

#### Arch Linux:
1. Installiere erforderliche Pakete:
   ```
   sudo pacman -S python python-pip python-gobject gtk3 rtl-sdr
   ```
2. Installiere rtl_433 aus dem AUR:
   ```
   yay -S rtl_433
   ```

### Projekt einrichten
1. Klone das Repository:
   ```
   git clone https://github.com/deinbenutzername/rtl-sdr-signal-analyzer.git
   cd rtl-sdr-signal-analyzer
   ```
2. Installiere Python-Abhängigkeiten:
   ```
   pip3 install -r requirements.txt
   ```

### Verwendung
1. Schließe deinen RTL-SDR-Dongle an deinen Computer an.
2. Führe das Programm aus:
   ```
   python3 main.py
   ```
3. Die GUI öffnet sich. Klicke auf "Start", um Signale zu empfangen und zu analysieren.
4. Empfangene Daten werden im Hauptfenster angezeigt und in 'zur_analyse.txt' protokolliert.

### Fehlerbehebung
- Bei Berechtigungsproblemen mit dem RTL-SDR-Gerät füge deinen Benutzer zur 'plugdev'-Gruppe hinzu:
  ```
  sudo usermod -a -G plugdev $USER
  ```
  Melde dich dann ab und wieder an, damit die Änderungen wirksam werden.

- Wenn rtl_433 nicht gefunden wird, stelle sicher, dass es installiert ist und sich in deinem System-PATH befindet.
