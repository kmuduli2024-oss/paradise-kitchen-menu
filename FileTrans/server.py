from http.server import HTTPServer, BaseHTTPRequestHandler
import os

PORT = 5000
DIRECTORY = "."

class FileHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.show_home()

        elif self.path.startswith("/download?file="):
            filename = self.path.split("=")[1]
            self.send_file(filename)

        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        if self.path == "/upload":
            self.receive_file()

    # Show homepage
    def show_home(self):
        files = os.listdir(DIRECTORY)

        file_list = ""
        for file in files:
            if file.endswith((".txt", ".pdf", ".jpg", ".png", ".mp3")):
                name = file.replace("uploaded_", "")
                file_list += f'<li>{name} - <a href="/download?file={file}">Download</a></li>'
        html = f"""
        <html>
        <body style="font-family:Arial; text-align:center;">
            <h1>📁 File Transfer System</h1>

            <h3>Download Files</h3>
            <ul style="list-style:none;">
                {file_list}
            </ul>

            <h3>Upload File</h3>
            <form method="POST" action="/upload" enctype="multipart/form-data">
                <input type="file" name="file">
                <br><br>
                <input type="submit" value="Upload">
            </form>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    # Send file to mobile
    def send_file(self, filename):
        try:
            with open(filename, "rb") as file:
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", f"attachment; filename={filename}")
                self.end_headers()

                while True:
                    chunk = file.read(1024)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        except:
            self.send_error(404, "File not found")

    # Receive file from mobile
    def receive_file(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)

        boundary = self.headers['Content-Type'].split("=")[1].encode()
        parts = data.split(boundary)

        for part in parts:
            if b"filename=" in part:
                filename = part.split(b'filename="')[1].split(b'"')[0].decode()
                file_data = part.split(b"\r\n\r\n")[1].rstrip(b"\r\n--")

                with open("uploaded_" + filename, "wb") as f:
                    f.write(file_data)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"File uploaded successfully!")

# Run server
server = HTTPServer(("0.0.0.0", PORT), FileHandler)

print("===================================")
print(" FILE TRANSFER SERVER STARTED ")
print("===================================")
print("Step 1: Turn ON mobile hotspot")
print("Step 2: Connect laptop to hotspot")
print("Step 3: Find IP using ipconfig")
print("Step 4: Open http://YOUR_IP:5000 on phone")
print("===================================")

server.serve_forever()