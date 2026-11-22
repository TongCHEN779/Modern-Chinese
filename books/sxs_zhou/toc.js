(function(){var D=[["l","p01.html","前言"],["l","p02.html","第一章 始建大周"],["l","p03.html","第二章 华夏雏形"],["l","p04.html","第三章 西周之秋"],["l","p05.html","第四章 西周哀怨"],["l","p06.html","第五章 西周社会"],["l","p07.html","第六章 周室衰微"],["l","p08.html","第七章 春秋争霸"],["l","p09.html","第八章 春秋吴越"],["l","p10.html","第九章 战国风云（上）"],["l","p11.html","第十章 战国风云（下）"],["l","p12.html","第十一章 东周的灭亡"],["l","p13.html","附录一 春秋战国时期的文化思想"],["l","p14.html","附录二 生产力的革新"],["l","p15.html","附录三 周朝历史时间表"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
