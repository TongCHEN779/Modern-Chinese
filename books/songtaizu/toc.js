(function(){var D=[["l","p01.html","天朝史鉴"],["l","p02.html","前言"],["l","p03.html","第一章 乱世英雄"],["l","p04.html","第二章 黄袍加身"],["l","p05.html","第三章 集权"],["l","p06.html","第四章 恩威并重"],["l","p07.html","第五章 宅心仁厚"],["l","p08.html","第六章 中原王朝"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
