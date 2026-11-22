(function(){var D=[["l","p01.html","防空在“堪察加”的一角"],["l","p02.html","联保主任的消遣"],["l","p03.html","在其香居茶馆里"],["l","p04.html","公道"],["l","p05.html","三斗小麦"],["l","p06.html","没有演出的戏"],["l","p07.html","小城风波"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
