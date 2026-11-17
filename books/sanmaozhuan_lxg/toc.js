(function(){var D=[["l","p01.html","前言"],["l","p02.html","第一章 梦始硝烟雾都城"],["l","p03.html","第二章 渴望自由的少女"],["l","p04.html","第三章 倔强蔷薇孤独绽放"],["l","p05.html","第四章 恋爱的滋味"],["l","p06.html","第五章 山有木兮木有枝"],["l","p07.html","第六章 白首不相离"],["l","p08.html","第七章 聚散离别两茫茫"],["l","p09.html","第八章 万水千山走遍"],["l","p10.html","第九章 花开花落终有时"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
