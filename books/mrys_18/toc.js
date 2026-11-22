(function(){var D=[["l","p01.html","《中国名人轶事丛书》出版缘由"],["l","p02.html","主编絮语"],["l","p03.html","一、少小爱诗"],["l","p04.html","二、意气风发"],["l","p05.html","三、菊枕诗情"],["l","p06.html","四、戕羽归来"],["l","p07.html","五、沈园惊鸿"],["l","p08.html","六、元酋授首"],["l","p09.html","七、因谗去国"],["l","p10.html","八、雪溪刺虎"],["l","p11.html","九、单骑入金"],["l","p12.html","十、梦里烟尘"],["l","p13.html","十一、梅花之恋"],["l","p14.html","十二、深入民间"],["l","p15.html","十三、山花满头"],["l","p16.html","十四、南园一记"],["l","p17.html","十五、莲花博士"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
