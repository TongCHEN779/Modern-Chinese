(function(){var D=[["l","p01.html","第一章 “奇迹”之神童"],["l","p02.html","第二章 乐器大师"],["l","p03.html","第三章 一部已婚的作曲机器"],["l","p04.html","第四章 莫扎特的歌剧魔法"],["l","p05.html","第五章 一个没有虚度的美好人生"],["l","p06.html","尾声"],["l","p07.html","附录：莫扎特在伦敦"],["l","p08.html","进一步阅读"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
