(function(){var D=[["l","p01.html","前言"],["l","p02.html","第一章 明朝兴起，江山一统"],["l","p03.html","第二章 开创期政治局面"],["l","p04.html","第三章 中期的衰弱与危机"],["l","p05.html","第四章 万历中兴"],["l","p06.html","第五章 后期的衰落"],["l","p07.html","第六章 明朝的灭亡"],["l","p08.html","附录一：瑰丽夺目的文学成就"],["l","p09.html","附录二：领先世界的科技学术成就"],["l","p10.html","附录三：光耀千古的思想艺术成就"],["l","p11.html","附录四：明朝历代皇帝年表"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
