(function(){var D=[["l","p01.html","《中国名人轶事丛书》出版缘由"],["l","p02.html","主编絮语"],["l","p03.html","初审石头案"],["l","p04.html","计了私盐案"],["l","p05.html","巧断僧尼案"],["l","p06.html","揭穿善人案"],["l","p07.html","奇侦殉节案"],["l","p08.html","智勘投毒案"],["l","p09.html","复审斗牛案"],["l","p10.html","巧圆赖婚案"],["l","p11.html","重理无尸案"],["l","p12.html","宽判杀人案"],["l","p13.html","附录：郑板桥年谱"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
