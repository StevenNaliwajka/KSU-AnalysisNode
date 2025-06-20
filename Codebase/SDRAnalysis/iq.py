from PyQt5 import QtWidgets, QtCore
import numpy as np
import pyqtgraph as pg
import sys
import os
from PyQt5.QtWidgets import QFileDialog
from scipy.signal import find_peaks

pg.setConfigOption('background', 'w')  # Set white background
pg.setConfigOption('foreground', 'k')  # Set black foreground (axis, labels)


class IQVideoPlayer(QtWidgets.QMainWindow):
    def __init__(self, filename):
        super().__init__()
        short_name = os.path.basename(filename)
        #self.setWindowTitle("IQ Video Player")
        self.setWindowTitle(f"IQ Video Player - {short_name}")
        self.resize(1200, 800)

        self.fs = 20e6  # Sample rate
        self.chunk_size = 1024
        self.playing = False
        self.current_frame = 0
        
        self.all_peaks = []  # Cache of detected peaks
        self.peak_pointer = 0  # Index in peak list


        # Load IQ data
        self.iq = self.load_iq(filename)
        self.total_frames = len(self.iq) - self.chunk_size
        self.t = np.arange(len(self.iq)) / self.fs

        # UI setup
        self.central = QtWidgets.QWidget()
        self.setCentralWidget(self.central)
        self.layout = QtWidgets.QVBoxLayout(self.central)

        self.plot_widget = pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.plot_widget)

        # ---- Time-Domain Plot ----
        self.time_plot = self.plot_widget.addPlot(title="Time-Domain")
        self.time_plot.showGrid(x=True, y=True, alpha=0.3)
        self.curve_i = self.time_plot.plot(pen='b')
        self.curve_q = self.time_plot.plot(pen='r')
        self.time_plot.setLabel('left', 'Amplitude')
        self.time_plot.setLabel('bottom', 'Time', units='s')

        # ---- Instantaneous Phase Shift Plot ----
        self.plot_widget.nextRow()
        self.iqangle_plot = self.plot_widget.addPlot(title="Phase (Time Domain)")
        self.iqangle_plot.showGrid(x=True, y=True, alpha=0.3)
        self.iqangle_plot.setLabel('left', units='Degrees')
        self.iqangle_plot.setLabel('bottom', 'Time', units='s')
        self.iqangle_curve = self.iqangle_plot.plot(pen='m')  
        
        # ---- FFT Magnitude Plot ----
        self.plot_widget.nextRow()
        self.iphase_plot = self.plot_widget.addPlot(title="FFT Magnitude")
        self.iphase_plot.showGrid(x=True, y=True, alpha=0.3)
        self.iphase_plot.setLabel('left', units='dB')
        self.iphase_plot.setLabel('bottom', 'Frequency', units='MHz')
        self.iphase_curve = self.iphase_plot.plot(pen='m')        

        # ---- FFT Phase Shift Plot ----
        self.plot_widget.nextRow()
        self.phase_plot = self.plot_widget.addPlot(title="Phase (Frequency Domain)")
        self.phase_plot.showGrid(x=True, y=True, alpha=0.3)
        self.phase_plot.setLabel('left', units='Degrees')
        self.phase_plot.setLabel('bottom', 'Frequency', units='MHz')
        self.phase_curve = self.phase_plot.plot(pen='m')

        # Slider
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.total_frames - 1)
        self.slider.valueChanged.connect(self.slider_seek)
        self.layout.addWidget(self.slider)

        # Play/Pause Button
        self.button = QtWidgets.QPushButton("Play")
        self.button.clicked.connect(self.toggle_playback)
        self.layout.addWidget(self.button)
        
        # Toggle: Phase or Frequency
        self.show_frequency = True  # Default mode
        self.toggle_button = QtWidgets.QPushButton("Show Phase")
        self.toggle_button.clicked.connect(self.toggle_mode)
        self.layout.addWidget(self.toggle_button)
        
        self.next_peak_btn = QtWidgets.QPushButton("Next Peak")
        self.next_peak_btn.clicked.connect(self.find_next_peak)
        self.layout.addWidget(self.next_peak_btn)

        # Timer for frame update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.next_frame)

        self.update_plots(0)

    def load_iq(self, fname):
        #num_samples = int(len(self.iq)/2)
        with open(fname, 'rb') as f:
            start_byte=0
            f.seek(start_byte,0)
            raw = np.frombuffer(f.read(), dtype=np.int8)#, count=num_samples*2)
        i = raw[0::2].astype(np.float32)
        q = raw[1::2].astype(np.float32)
        return i + 1j * q

    def toggle_playback(self):
        if self.playing:
            self.timer.stop()
            self.button.setText("Play")
        else:
            self.timer.start(100)
            self.button.setText("Pause")
        self.playing = not self.playing

    
    def toggle_mode(self):
        self.show_frequency = not self.show_frequency
        if self.show_frequency:
            self.toggle_button.setText("Show Phase Shift")
            self.iqangle_plot.setLabel('left', units='Degrees')
            self.phase_plot.setLabel('left', units='Degrees')
        else:
            self.toggle_button.setText("Show Phase")
            self.iqangle_plot.setLabel('left', units='Degrees/ms')
            self.phase_plot.setLabel('left', units='Degrees/ms')
        self.update_plots(self.current_frame)

    def next_frame(self):
        if self.current_frame < self.total_frames - 1:
            self.current_frame += 1
        else:
            self.timer.stop()
            self.button.setText("Play")
            self.playing = False
        self.slider.blockSignals(True)
        self.slider.setValue(self.current_frame)
        self.slider.blockSignals(False)
        self.update_plots(self.current_frame)
        
    def find_next_peak(self):
        magnitude = self.iq
        #phasor = np.angle(magnitude)
        #phase_shift = np.diff(phasor)
        fft_vals = np.fft.fftshift(np.fft.fft(magnitude))
        dc_index = len(fft_vals) // 2
        fft_vals[dc_index] = 0  # Zero the DC component
        # Find all peaks only once
        if len(self.all_peaks) == 0:
            self.all_peaks, _ = find_peaks(fft_vals, height=20000)  # adjust height threshold
            if len(self.all_peaks) == 0:
                print("No peaks found in signal.")
                return

        # Find first peak after current frame end
        current_sample = self.current_frame + self.chunk_size
        remaining_peaks = [p for p in self.all_peaks if p > current_sample]

        if not remaining_peaks:
            print("No more peaks found after current position.")
            return

        next_peak = remaining_peaks[0]
        frame_index = max(0, next_peak - self.chunk_size // 2)
        print(f"Jumping to next peak at sample {next_peak}, frame {frame_index}")

        self.slider.setValue(frame_index)
        self.slider_seek(frame_index)


    def slider_seek(self, frame_index):
        self.current_frame = frame_index
        self.update_plots(frame_index)

    def update_plots(self, frame_index):
        start = frame_index
        end = start + self.chunk_size
        segment = self.iq[start:end]
        dur = self.t[start:end]

        # ---- Time Domain Plot ----
        self.curve_i.setData(dur, segment.real)
        self.curve_q.setData(dur, segment.imag)

        # ---- Phase Shift Plot ----
        fft_vals = np.fft.fftshift(np.fft.fft(segment))
        dc_index = len(fft_vals) // 2
        fft_vals[dc_index] = 1  # Zero the DC component
        freqs = np.fft.fftshift(np.fft.fftfreq(len(segment), d=1 / self.fs)) / 1e6  # MHz
        freqs1 = freqs[:-1] + (freqs[1] - freqs[0]) / 2

        iqangle = np.angle(segment)
        iqunwrap = np.unwrap(iqangle)*(360/(2*np.pi))
        phase_spectrum = np.angle(fft_vals)
        unwrapped_phase = np.unwrap(phase_spectrum)*(360/(2*np.pi))

        if self.show_frequency:
            self.iqangle_curve.setData(dur,iqunwrap)
            self.phase_curve.setData(freqs, unwrapped_phase)
            #self.curve_i.setData(dur, segment.real)
            #self.curve_q.setData(dur, segment.imag)

        else:
            self.iqangle_curve.setData(dur[1:end],np.diff(iqunwrap)*19.53125)
            self.phase_curve.setData(freqs1, np.diff(unwrapped_phase)*19.53125)
            #self.curve_i.setData(dur[1:end], np.diff(segment.real))
            #self.curve_q.setData(dur[1:end], np.diff(segment.imag))
        
        self.iphase_curve.setData(freqs,20 * np.log10(abs(fft_vals) + 1e-6))
        #self.phase_curve.setData(freqs1, unwrapped_phase)

        """
        # ----- Annotate Center Frequency Phase Shift -----
        center_index = len(freqs) // 2
        center_freq = freqs[center_index]
        center_phase = unwrapped_phase[center_index]

        # Clear existing text items first
        for item in self.phase_plot.allChildItems():
            if isinstance(item, pg.TextItem):
                self.phase_plot.removeItem(item)

        text = pg.TextItem(f"{center_phase:.2f}", color='y')
        text.setPos(center_freq, center_phase)
        self.phase_plot.addItem(text)
        """


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    fname, _ = QFileDialog.getOpenFileName(None, "Open IQ File", "", "IQ files (*.iq);;All files (*)")
    viewer = IQVideoPlayer(fname)
    viewer.show()
    sys.exit(app.exec_())

