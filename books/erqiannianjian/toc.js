(function(){var D=[["l","p01.html","编者的话"],["l","p02.html","导言"],["l","p03.html","二千年的鸟瞰"],["l","p04.html","在“万人之上”的人"],["l","p05.html","一种特殊职业——做官"],["l","p06.html","又一种特殊职业——当兵"],["l","p07.html","一切寄托在土地上"],["l","p08.html","大地下的撼动"],["l","p09.html","不安静的北方边塞"],["l","p10.html","当胡骑踏进中原的时候"],["l","p11.html","逃不了的灭亡命运"],["l","p12.html","附录　读《二千年间》（吴晗）"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
