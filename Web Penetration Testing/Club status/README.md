<code>- Mở Burpsuite (Application/Kali Linux/Top 10 Security Tools/burpsuite) -> Tắt Intercept (Intercrept is off) ở tab Proxy</code><br/>
<code>- Mở trình duyệt Iceweasel -> Edit -> Preferences -> chọn tab Advanced -> chọn tab Network -> Settings -> Manual proxy configuration (HTTP Proxy: 127.0.0.1 Port 8080)</code><br/>
<code>- Duyệt 192.168.100.210/index.php (tab Blog bị mở không click được) -> Click vào Sign In</code><br/>
<code>- Quay lại burpsuite -> chọn tab Options -> chọn tab Sessions -> Chọn Use cookies from Burp's cookie jar (trong phần Session Handling Rules) -> Edit -> chọn tab Scope -> tích chọn Proxy (use with caution), bỏ chọn Scanner, Spider -> OK</code><br/>
<code>- Kéo xuống phần Cookie jar -> chọn Open cookie jar -> chọn dòng có name là vip -> Edit cookie -> chỉnh trường value thành 1 -> OK -> close </code><br/>
<code>- Quay lại trình duyệt Iceweasel reload lại trang sẽ thấy tab Blog sáng lên</code><br/>
<code>- Ấn vào tab BLog</code><br/>
Flag <strong>ComplexKillingInverse411</strong>
