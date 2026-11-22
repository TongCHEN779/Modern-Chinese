(function(){var D=[["l","p01.html","《中国名人轶事丛书》出版缘由"],["l","p02.html","主编絮语"],["l","p03.html","众里寻她千百度"],["l","p04.html","无边丝雨细如愁"],["l","p05.html","舞低杨柳楼心月"],["l","p06.html","相见时难别亦难"],["l","p07.html","欲为圣朝除弊事"],["l","p08.html","从此君王不早朝"],["l","p09.html","愁浓难补眉儿淡"],["l","p10.html","子规啼破城楼月"],["l","p11.html","不斩楼兰终不还"],["l","p12.html","一身报国有万死"],["l","p13.html","秋雨梧桐叶落时"],["l","p14.html","战地风来草木腥"],["l","p15.html","最是仓皇辞庙日"],["l","p16.html","强呼绛树出雕栏"],["l","p17.html","此恨绵绵无绝期"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
