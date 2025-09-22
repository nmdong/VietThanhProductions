Định nghĩa format API chuẩn

1. Request (client → server)
Json:
	{
	  "action": "login",        // hoặc "order", "remove", "update", ...
	  "data": {                 // payload chính của request
		"username": "user123",
		"password": "mypassword"
	  },
	  "meta": {                 // optional: thông tin thêm
		"requestId": "abc123",
		"timestamp": "2025-09-22T09:15:00Z",
		"client": "web"
	  }
	}
	
	action: định nghĩa loại hành động (login, order, remove…).
	data: nội dung chính mà API xử lý.
	meta: metadata, không bắt buộc (dùng cho trace, log, debug).

2. Response (server → client)
Thành Công:
	{
	  "status": "success",
	  "data": {
		"userId": 101,
		"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
	  },
	  "meta": {
		"requestId": "abc123",
		"timestamp": "2025-09-22T09:15:05Z",
		"processingTimeMs": 120
	  }
	}
	
Thất bại
	{
	  "status": "error",
	  "error": {
		"code": "INVALID_CREDENTIALS",
		"message": "Invalid username or password",
		"details": null
	  },
	  "meta": {
		"requestId": "abc123",
		"timestamp": "2025-09-22T09:15:05Z"
	  }
	}

📐 Nguyên tắc chung

status: "success" hoặc "error" (giúp phân biệt nhanh).
data: luôn trả về object (không trả raw string/array để thống nhất).
error: có code, message, details (chi tiết cho dev).
meta: optional, chứa trace, log, timestamp, requestId để dễ tracking.
consistency: tất cả API (login, order, remove…) đều theo một format như trên.
