// Usage: node aas/render-day.js plan.json
// plan.json: {"date":"2026-10-17","cards":[{"n":1,"tag":"GIỚI THIỆU","h":"Tiêu đề <em>nhấn</em>","p":"Câu phụ","num":"","pose":"15"}, ...]}
// Optional top-level: prefix (default L04), brand, sig, sig2, cta, theme ('bds' = navy/gold)
// Output: aas/img/<prefix>-<date>-<n>.jpg  (1080x1350)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const plan=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));const dir=__dirname;
const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350}});
for(const c of plan.cards){const q=new URLSearchParams({t:c.tag||'',h:c.h||'',p:c.p||'',n:c.num||'',pose:c.pose||'01'});
if(c.fs)q.set('fs',c.fs);for(const k of ['brand','sig','sig2','cta','theme'])if(plan[k])q.set(k,plan[k]);
await pg.goto('file://'+path.join(dir,'card.html')+'?'+q.toString());await pg.waitForLoadState('networkidle');await pg.waitForTimeout(300);
const out=path.join(dir,'img',`${plan.prefix||'L04'}-${plan.date}-${c.n}.jpg`);await pg.screenshot({path:out,type:'jpeg',quality:90});console.log('ok',out);}
await b.close()})();
