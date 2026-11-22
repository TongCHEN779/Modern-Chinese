(function(){var D=[["l","p01.html","重印前记"],["l","p02.html","序"],["l","p03.html","一"],["l","p04.html","二"],["l","p05.html","三"],["l","p06.html","四"],["l","p07.html","五"],["l","p08.html","六"],["l","p09.html","七"],["l","p10.html","八"],["l","p11.html","九"],["l","p12.html","附录 记钱钟书与《围城》"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
