#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聽音辨字遊戲 - 本機伺服器
提供靜態檔案與 /api/sheet_csv（代理 Google 試算表 CSV），避免 CORS 問題。
執行後用瀏覽器開啟 http://localhost:5002/ 或 http://localhost:5002/index.html
"""

import http.server
import socketserver
import os
import urllib.request
import urllib.parse

PORT = 5002
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class ListeningGameHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/sheet_csv":
            self.handle_sheet_csv(parsed.query)
            return

        super().do_GET()

    def handle_sheet_csv(self, query):
        """代理取得 Google 試算表 CSV"""
        params = urllib.parse.parse_qs(query)
        sheet_id = (params.get("sheet_id") or [""])[0]
        gid = (params.get("gid") or ["0"])[0]
        if not sheet_id:
            sheet_id = "1264gdkuMnIn2k5L5KM69yumBfJFdYVhxzzsC-2R5Q2U"
        try:
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; listening-game/1.0)"},
            )
            opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
            with opener.open(req, timeout=15) as resp:
                csv_data = resp.read().decode("utf-8-sig")
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.end_headers()
            self.wfile.write(csv_data.encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                f"取得試算表錯誤: {e}\n請確認試算表已設為「知道連結的任何人可檢視」".encode(
                    "utf-8"
                )
            )


def main():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), ListeningGameHandler) as httpd:
        print(f"聽音辨字遊戲伺服器: http://localhost:{PORT}/")
        print(f"請開啟: http://localhost:{PORT}/")
        print("按 Ctrl+C 結束")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
