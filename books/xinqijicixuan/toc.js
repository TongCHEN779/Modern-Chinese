(function(){var D=[["l","p01.html","前言"],["g","编年部分"],["l","p02.html","水调歌头·寿赵漕介庵—沁园春·带湖新居将成"],["l","p03.html","水调歌头·盟鸥—临江仙·再用韵送祐之弟归浮梁"],["l","p04.html","满江红·中秋寄远—水调歌头·壬子三山被召，陈端仁给事饮饯席上作"],["l","p05.html","鹧鸪天·三山道中—浣溪沙"],["l","p06.html","归朝欢·题赵晋臣敷文积翠岩—瑞鹧鸪·乙丑奉祠归，舟次余干赋"],["g","未编年部分"],["l","p07.html","鹧鸪天·代人赋—霜天晓角·赤壁"],["g","附录"],["l","p08.html","词评辑要"],["l","p09.html","行年事略"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
