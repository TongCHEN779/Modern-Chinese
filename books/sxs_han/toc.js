(function(){var D=[["l","p01.html","前言"],["l","p02.html","第一章 楚汉争霸定乾坤"],["l","p03.html","第二章 刘邦登基，汉朝建立"],["l","p04.html","第三章 吕后篡权，图谋天下"],["l","p05.html","第四章 文景之治与七王之乱"],["l","p06.html","第五章 从鼎盛到衰败的西汉王朝"],["l","p07.html","第六章 东汉王朝"],["l","p08.html","附录 汉王朝的文化成就"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
