(function(){var D=[["l","p01.html","前言"],["l","p02.html","第一章 西晋王朝的建立"],["l","p03.html","第二章 西晋一统中华"],["l","p04.html","第三章 西晋王朝的短暂统治"],["l","p05.html","第四章 晋室南迁建东晋"],["l","p06.html","第五章 北伐空梦"],["l","p07.html","第六章 东晋名流"],["l","p08.html","第七章 偏安江南"],["l","p09.html","第八章 僵死之躯"],["l","p10.html","第九章 东晋的灭亡"],["l","p11.html","附录"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
