
1. Setup Git - https://www.python.org/ftp/python/3.9.10/python-3.9.10.exe
2. Setup pycham: https://www.jetbrains.com/pycharm/download/?section=windows
3. Kiem tra python version: python -c "import platform; print(platform.architecture())"
4. Tao Project tren BackEnd
	Mở PyCharm Community.
		Chọn File → New Project….
		Ở mục New Project:
			Chọn Pure Python (PyCharm Community không có sẵn Flask/Django template như bản Pro).
			Tick vào New environment using → Virtualenv (venv).
			Location: đặt đường dẫn cho project, ví dụ: D:\vietthanh\access_backend
			
		Chọn đúng Python Interpreter (32/64-bit)
			Điểm quan trọng: Access ODBC driver (Microsoft Access Driver (*.mdb, *.accdb)) chỉ hoạt động nếu Python và driver cùng bitness.
			Nếu bạn đã cài ODBC driver 64-bit, thì phải chọn Python 64-bit.
			Nếu bạn đang có driver 32-bit, thì phải cài thêm Python 32-bit rồi chọn interpreter này trong PyCharm.

				👉 Cách kiểm tra driver hiện có:

					Nhấn Win + R, gõ: odbcad32
						C:\Windows\System32\odbcad32.exe → quản lý DSN 64-bit
						C:\Windows\SysWOW64\odbcad32.exe → quản lý DSN 32-bit
						Mở một trong hai và xem có driver Microsoft Access Driver (*.mdb, *.accdb) không.
