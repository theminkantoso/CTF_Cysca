Tải file <code>c18493dcc4281aef5d3c4b24d674d8e3-net02.pcap</code> từ trang chủ của CYSCA<br/>
Mở file (sẽ tự động mở bằng Wireshark) và chọn <code>Conversations</code><br/>
Chọn tab <code>TCP: 5</code> và chọn cái có kích thước lớn nhất <strong>10.0.0.103 -> 10.0.0.104</strong><br/>
Chọn <code>Follow Stream</code><br/>
Chọn checkbox <strong>Raw</strong>, chọn dropdown thay đổi từ "Entire conversation" thành <strong>10.0.0.103:50723 -> 10.0.0.104:37376 (3230287)</strong> và chọn <strong>Save As</strong><br/>
<code>File->Export Objects -> HTTP</code> và chọn tạo 1 folder <strong>export</strong> trên desktop<br/>
Lưu tên file là <code>diskimage.gz</code><br/>
Chạy theo thứ tự các lệnh sau
<code>gzip -d diskimage.gz</code><br/>
<code>file diskimage</code><br/>
<code>icat -o 128 diskimage 589 > secret.7z</code><br/>
<code>7z x -p'nRkmrtp2("u8~/ph' secret.7z</code><br/>
<code>cat secret.txt</code><br/>
Mở txt trên desktop sẽ thấy được cờ là <code>WhiteBelatedBlind439</code>