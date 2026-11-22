(function(){var D=[["l","p01.html","前记"],["l","p02.html","第一部分 序幕"],["l","p03.html","第二部分 在天回镇"],["l","p04.html","第三部分 交流"],["l","p05.html","第四部分 兴顺号的故事"],["l","p06.html","第五部分 死水微澜"],["l","p07.html","第六部分 余波"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
