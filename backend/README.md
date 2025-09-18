
1) Chuẩn bị môi trường (PyCharm / Windows)
	Mở PyCharm → File > New Project → chọn Python (tạo venv).
	Chọn Interpreter đúng bitness (32/64-bit) tương ứng với Access ODBC driver.
	Tạo project folder, ví dụ access_backend/.
	
2) Cấu trúc project (tạo các thư mục & file)
	access_backend/
		│── app.py
		│── config.py
		│── requirements.txt
		│── .env
		│
		├── db/
		│   ├── __init__.py
		│   ├── connection.py
		│   └── dao_user.py
		│
		├── models/
		│   ├── __init__.py
		│   ├── user_schema.py
		│   ├── product_schema.py
		│   └── order_schema.py
		│
		├── routes/
		│   ├── __init__.py
		│   └── user_routes.py
		│
		└── swagger/
			├── generate_spec.py
			└── swagger_generated.yaml   # (sản sinh)

3) Tạo file requirements.txt:
	Cài trong terminal PyCharm: pip install -r requirements.txt
	
4) .env và config.py

5) DB connection (db/connection.py)

6) DAO cho bảng users (db/dao_user.py)

7) Marshmallow schemas (models/*.py)

8) Routes (Blueprint) — routes/user_routes.py: Chỉ implement users full CRUD (các resources khác tương tự):

9) Swagger auto-generate tool (swagger/generate_spec.py): Tool tổng quát — bạn chỉ cần thêm schema mới vào AVAILABLE hoặc pass tên schema qua CLI.
	Chạy (ví dụ sinh cho User và Product): python swagger/generate_spec.py --schemas User Product
	Hoặc mọi schema: python -m swagger.generate_spec

10) app.py (load swagger_generated.yaml)

11) (TÙY CHỌN) Script tạo file .mdb & bảng users tự động (Windows)
	Nếu bạn chưa có sample_db.mdb, dùng script này để tạo file .mdb và tạo bảng users. Yêu cầu: Windows + pywin32 + Jet OLEDB available + đúng bitness. -> python create_mdb.py
	Nếu không muốn dùng COM, bạn có thể tạo file .mdb bằng Access GUI rồi đặt vào path trong .env.
	
12) Chạy ứng dụng & test
	- Generate Swagger spec (lần đầu hoặc sau khi sửa schema): python -m swagger.generate_spec
	- Chạy server: python app.py
	- Mở Swagger UI: http://127.0.0.1:5000/apidocs/ — bạn sẽ thấy tất cả các endpoints CRUD được sinh tự động (từ swagger_generated.yaml).
	
	