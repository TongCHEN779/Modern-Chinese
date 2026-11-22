(function(){var D=[["l","p01.html","序"],["l","p02.html","人生哲学的一课"],["l","p03.html","山峡中"],["l","p04.html","松岭上"],["l","p05.html","在茅草地"],["l","p06.html","洋官与鸡"],["l","p07.html","我诅咒你那么一笑"],["l","p08.html","我们的友人"],["l","p09.html","我的爱人"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
