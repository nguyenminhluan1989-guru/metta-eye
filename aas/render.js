const {chromium}=require('playwright');
const cards=[
["GIỚI THIỆU","Tôi không phải chuyên gia <em>từ trên trời rơi xuống.</em>","Tôi là người trong cuộc. Tôi từng ôm hết mọi việc như bạn.",""],
["5 BÍ QUYẾT","Doanh nghiệp <em>tự chạy</em> không phải câu quảng cáo.","5 bí quyết tôi học được từ những người làm AI Automation đi trước.","5"],
["DỄ LÀM TRƯỚC","5 cách để doanh nghiệp <em>tự chạy</em>, có khách đều.","Không cần làm cả 5. Chọn 1 cách, làm trong tuần này.","5"],
["AI CHĂM KHÁCH 24/7","11 giờ đêm. Khách nhắn. <em>Bạn đang ngủ.</em>","Bạn không cần thức 24 giờ. Bạn cần một hệ thống làm việc khi bạn nghỉ.",""],
["CHATBOT AI","Tôi đã ngừng tự tay trả lời <em>từng tin nhắn.</em>","Không phải vì lười. Mà vì khách không nên phải chờ.",""],
["5 MẸO NHANH","Doanh nghiệp <em>tự chạy</em> bằng AI.","Mẹo nào cũng làm được trong một buổi.","5"],
["GIAO VIỆC CHO AI","Bạn không kiệt sức vì kinh doanh.","Bạn kiệt sức vì <em>ôm hết mọi việc</em> một mình.",""],
["AI AUTOMATION","Lấy lại thời gian. <em>Không để lọt khách.</em>","Vì sao chủ doanh nghiệp nhỏ cài AI Automation.",""]];
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350}});
for(let i=0;i<cards.length;i++){const [t,h,p,n]=cards[i];const pose=['15','06','08','09','10','06','14','07'][i];const ps=p.replace(/<\/?em>/g,'');
const hh=i==6?h+'<br><span style="font-size:.62em;line-height:1.25;display:inline-block;margin-top:18px;color:#9be8c0">Bạn kiệt sức vì ôm hết mọi việc một mình.</span>':h;
const pp=i==6?'Hãy bắt đầu giao việc lặp lại cho AI.':ps;
await pg.goto('file://'+process.cwd()+'/card.html?'+new URLSearchParams({t,h:hh,p:pp,n,pose}).toString());await pg.waitForTimeout(400);
await pg.screenshot({path:`L04-2026-10-16-${i+1}.jpg`,type:'jpeg',quality:90});}
await b.close()})();
