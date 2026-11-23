(function(){var D=[["l","p01.html","几句话"],["g","作品部分"],["l","p02.html","诗"],["l","p03.html","诗人必须说真话"],["l","p04.html","形象思维和艺术魅力"],["l","p05.html","诗论"],["l","p06.html","诗人论"],["g","资料部分"],["l","p07.html","艾青的诗"],["l","p08.html","艾青的狱中诗"],["l","p09.html","附：艾青二十五首狱中诗目录"],["l","p10.html","艾青年表"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
