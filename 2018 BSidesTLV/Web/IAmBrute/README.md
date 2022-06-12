Mở Burpsuite, vào tab Proxy<br/>
Mở Browser của Burpsuite (thì mới intercept được) <br/>
Vào đường link sau http://192.168.189.128:8084/login.php<br/>
Ở Burpsuite, trong tab Proxy mở tab Option<br/>
Trong mục <strong>Match and Replace</strong>, chọn <strong>Add</strong><br/>
<strong>Type</strong> Request header</strong>, để trống <strong>Match</strong>, còn mục <strong>Replace</strong> để là <code>x-forwarded-for: 192.168.20.1</code><br/>
Đăng nhập <strong>username</strong> george và <strong>password</strong> GeorgeTheCrew!<br/>
Ấn vào <code>Authentication Problem</code><br/>
Cờ là <code>BSidesTLV{Brut3Th3W0rld!}</code>
