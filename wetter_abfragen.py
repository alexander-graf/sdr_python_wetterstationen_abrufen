import subprocess
import json
import gi
import datetime
import re
import math

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Pango

class RTL433Process:
    def __init__(self, data_callback):
        self.data_callback = data_callback
        self.process = None
        self.buffer = ""
        self.debug_log = open('rtl_433_debug.log', 'w')  # Öffne eine Debug-Log-Datei

    def start(self):
        self.process = subprocess.Popen(
            ['rtl_433', '-f', '433.92M', '-A', '-F', 'json'],  # -v für verbose
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        GLib.io_add_watch(
            self.process.stdout,
            GLib.IO_IN | GLib.IO_HUP,
            self.handle_output
        )

    def handle_output(self, source, condition):
        if condition == GLib.IO_HUP:
            return False
        line = source.readline().strip()
        
        self.buffer += line + "\n"
        if line.startswith("{"):
            try:
                data = json.loads(line)
                self.data_callback(data, self.buffer)
                self.buffer = ""  # Reset buffer after processing
            except json.JSONDecodeError:
                pass  # Ignore non-JSON lines
        return True

    def terminate(self):
        if self.process:
            self.process.terminate()
            self.process = None
        self.debug_log.close()  # Schließe die Debug-Log-Datei

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="RTL-433 Daten Logger")
        self.set_default_size(1000, 800)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.vbox)

        # Frame für aktuelle Daten
        self.info_frame = Gtk.Frame(label="Aktuelle Daten")
        self.info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.info_frame.add(self.info_box)
        self.vbox.pack_start(self.info_frame, False, False, 0)

        # Labels für aktuelle Daten
        self.station_label = Gtk.Label()
        self.rssi_label = Gtk.Label()
        self.snr_label = Gtk.Label()
        self.noise_label = Gtk.Label()
        self.model_label = Gtk.Label()
        self.temp_label = Gtk.Label()
        self.humidity_label = Gtk.Label()

        for label in [self.station_label, self.rssi_label, self.snr_label, 
                      self.noise_label, self.model_label, self.temp_label, 
                      self.humidity_label]:
            self.info_box.pack_start(label, True, True, 0)

        # TreeView für tabellarische Darstellung
        self.liststore = Gtk.ListStore(str, str, str)
        self.treeview = Gtk.TreeView(model=self.liststore)
        for i, column_title in enumerate(["Zeitstempel", "Schlüssel", "Wert"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.treeview)
        self.vbox.pack_start(scrolled_window, True, True, 0)

        # Erstellen Sie ein horizontales Box-Layout für die Werte und Meter
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.vbox.pack_start(hbox, False, False, 0)

        # Linke Box für Werte
        self.left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        hbox.pack_start(self.left_box, True, True, 0)

        # Rechte Box für Meter
        self.right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        hbox.pack_start(self.right_box, True, True, 0)

        # Labels für Werte
        self.rssi_label = Gtk.Label()
        self.snr_label = Gtk.Label()
        self.noise_label = Gtk.Label()

        # Labels für Meter
        self.rssi_meter = Gtk.Label()
        self.snr_meter = Gtk.Label()
        self.noise_meter = Gtk.Label()

        for label in [self.rssi_label, self.snr_label, self.noise_label]:
            self.left_box.pack_start(label, True, True, 0)

        for meter in [self.rssi_meter, self.snr_meter, self.noise_meter]:
            self.right_box.pack_start(meter, True, True, 0)

        self.rtl_process = RTL433Process(self.handle_data)
        self.rtl_process.start()

        self.connect("destroy", self.on_destroy)

    def update_info_labels(self, data, rssi, snr, noise):
        self.station_label.set_text(f"Station ID: {data.get('id', 'N/A')}")
        self.rssi_label.set_text(f"RSSI: {rssi} dB")
        self.snr_label.set_text(f"SNR: {snr} dB")
        self.noise_label.set_text(f"Noise: {noise} dB")
        self.model_label.set_text(f"Modell: {data.get('model', 'N/A')}")
        
        temp = data.get('temperature_C')
        if temp is not None:
            self.temp_label.set_text(f"Temperatur: {temp:.1f}°C")
        else:
            temp = data.get('temperature_F')
            if temp is not None:
                temp_c = (temp - 32) * 5/9
                self.temp_label.set_text(f"Temperatur: {temp_c:.1f}°C")
            else:
                self.temp_label.set_text("Temperatur: N/A")
        
        humidity = data.get('humidity')
        if humidity is not None:
            self.humidity_label.set_text(f"Luftfeuchtigkeit: {humidity}%")
        else:
            self.humidity_label.set_text("Luftfeuchtigkeit: N/A")

        # Aktualisieren Sie die Wert-Labels
        self.rssi_label.set_text(f"RSSI: {rssi} dB")
        self.snr_label.set_text(f"SNR: {snr} dB")
        self.noise_label.set_text(f"Noise: {noise} dB")

        # Aktualisieren Sie die Meter
        self.rssi_meter.set_text(create_ascii_meter(rssi, -100, 0))
        self.snr_meter.set_text(create_ascii_meter(snr, 0, 30))
        self.noise_meter.set_text(create_ascii_meter(noise, -100, 0))

    def handle_data(self, data, full_output):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("DEBUG - Vollständige Ausgabe des rtl-433-Befehls:")
        print(full_output)
        print("\n" + "="*50 + "\n")

        rssi, snr, noise = extract_signal_info(full_output)
        
        print(f"RSSI: {rssi} dB")
        print(f"SNR: {snr} dB")
        print(f"Noise: {noise} dB")
        print("\n" + "="*50 + "\n")

        self.update_info_labels(data, rssi, snr, noise)

        for key, value in data.items():
            self.liststore.append([timestamp, key, str(value)])

        # Scroll to the bottom of the TreeView
        self.treeview.scroll_to_cell(len(self.liststore) - 1, None, True, 0.5, 0.5)

        log_entry = f"[{timestamp}] {full_output}\n"
        with open('zur_analyse.txt', 'a') as analyse_file:
            analyse_file.write(log_entry)

    def on_destroy(self, widget):
        self.rtl_process.terminate()
        Gtk.main_quit()

def create_ascii_meter(value, min_val, max_val, width=20):
    if value == 'N/A':
        return '[' + '-' * width + ']'
    try:
        value = float(value)
        fill = int((value - min_val) / (max_val - min_val) * width)
        fill = max(0, min(fill, width))
        return '[' + '#' * fill + '-' * (width - fill) + ']'
    except ValueError:
        return '[' + '?' * width + ']'

def extract_signal_info(full_output):
    rssi = snr = noise = 'N/A'
    
    # Suche nach verschiedenen Formaten für RSSI, SNR und Noise
    patterns = [
        r'RSSI:\s*([-\d.]+)\s*dB\s*SNR:\s*([-\d.]+)\s*dB\s*Noise:\s*([-\d.]+)\s*dB',
        r'RSSI:\s*([-\d.]+)\s*dB',
        r'SNR:\s*([-\d.]+)\s*dB',
        r'Noise:\s*([-\d.]+)\s*dB',
        r'Level estimates \[high, low\]:\s+(\d+),\s+(\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, full_output)
        if match:
            if len(match.groups()) == 3:
                rssi, snr, noise = match.groups()
                break
            elif 'RSSI' in pattern:
                rssi = match.group(1)
            elif 'SNR' in pattern:
                snr = match.group(1)
            elif 'Noise' in pattern:
                noise = match.group(1)
            elif 'Level estimates' in pattern:
                high, low = map(int, match.groups())
                if high > low:
                    snr = f"{10 * math.log10(high/low):.1f}"
    
    # Versuche, fehlende Werte zu berechnen
    if rssi != 'N/A' and noise != 'N/A' and snr == 'N/A':
        try:
            snr = f"{float(rssi) - float(noise):.1f}"
        except ValueError:
            pass
    
    return rssi, snr, noise

def main():
    win = MainWindow()
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
