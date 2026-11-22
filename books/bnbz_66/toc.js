(function(){var D=[["l","p01.html","冬阳 童年 骆驼队（《城南旧事》出版后记）"],["l","p02.html","城南旧事（代序）"],["l","p03.html","惠安馆传奇"],["l","p04.html","我们看海去"],["l","p05.html","兰姨娘"],["l","p06.html","驴打滚儿"],["l","p07.html","爸爸的花儿落了"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
