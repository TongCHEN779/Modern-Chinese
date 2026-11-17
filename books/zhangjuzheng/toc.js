(function(){var D=[["l","p01.html","序"],["l","p02.html","第一章 “荆州张秀才”"],["l","p03.html","第二章 政治生活的开始"],["l","p04.html","第三章 休假三年"],["l","p05.html","第四章 再投入政治漩涡"],["l","p06.html","第五章 内阁中的混斗（上）"],["l","p07.html","第六章 内阁中的混斗（下）"],["l","p08.html","第七章 大政变"],["l","p09.html","第八章 初步的建设（上）"],["l","p10.html","第九章 初步的建设（下）"],["l","p11.html","第十章 第一次打击以后"],["l","p12.html","第十一章 从夺情到归葬"],["l","p13.html","第十二章 元老的成功"],["l","p14.html","第十三章 鞠躬尽瘁"],["l","p15.html","第十四章 尾声"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
