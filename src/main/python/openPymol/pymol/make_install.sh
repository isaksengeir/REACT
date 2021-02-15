pyinstaller --noconfirm --log-level=WARN \
    --onefile --nowindow \
    --add-binary="_cmd.cpython-39-darwin.so:." \
    --upx-dir="/Users/gvi022/Onedrive - UiT Office 365/programming/REACT/src/main/python/openPymol/" \
    pymolapp.spec
