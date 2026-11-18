(function(){var D=[["l","p01.html","前言"],["l","p02.html","一 蜀中时期"],["l","p03.html","二 “酒隐安陆”时期及初入长安前后"],["l","p04.html","三 移家东鲁及供奉翰林时期"],["l","p05.html","四 去朝十年"],["l","p06.html","五 从璘及长流夜郎前后"],["l","p07.html","六 晚年"],["l","p08.html","七 未编年"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
