"""
Helper to produce consistent success/error payload format required.

Success format:
{
  "status":"success",
  "data": {...},
  "meta": { "requestId": "...", "timestamp": "...", "processingTimeMs": 120 }
}

Error format:
{
  "status":"error",
  "error": { "code": "...", "message": "...", "details": null },
  "meta": { "requestId": "...", "timestamp":py "..." }
}
"""
from flask import jsonify, g
import time
import uuid
from datetime import datetime, timezone

def now_iso():
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat().replace('+00:00','Z')

def start_request():
    """
    Call at start of request to set request start time and id.
    """
    g._req_start = time.time()
    g._req_id = uuid.uuid4().hex

def finish_meta(include_time=True):
    """
    Build meta dict including requestId, timestamp and optionally processingTimeMs.
    """
    meta = {
        "requestId": getattr(g, "_req_id", uuid.uuid4().hex),
        "timestamp": now_iso()
    }
    if include_time:
        start = getattr(g, "_req_start", None)
        if start is not None:
            meta["processingTimeMs"] = int((time.time() - start) * 1000)
    return meta

def success_response(data: dict, status_code=200):
    """
    Return JSON response with success payload.
    """
    payload = {
        "status": "success",
        "data": data,
        "meta": finish_meta(include_time=True)
    }
    return jsonify(payload), status_code

def error_response(code: str, message: str, details=None, status_code=400):
    """
    Return JSON error payload.
    """
    payload = {
        "status": "error",
        "error": {
            "code": code,
            "message": message,
            "details": details
        },
        "meta": finish_meta(include_time=False)
    }
    return jsonify(payload), status_code
