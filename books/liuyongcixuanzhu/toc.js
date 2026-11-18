(function(){var D=[["l","p01.html","前言"],["l","p02.html","黄莺儿—传花枝"],["l","p03.html","雨霖铃—锦堂春"],["l","p04.html","定风波—过涧歇近"],["l","p05.html","安公子—女冠子"],["l","p06.html","玉山枕—十二时"],["l","p07.html","柳永词评辑要"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
