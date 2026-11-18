(function(){var D=[["l","p01.html","前言"],["l","p02.html","文选"],["l","p03.html","书信选"],["g","诗选"],["l","p04.html","第一期 出国前（1904年春之前）"],["l","p05.html","第二期 留日时期（1904年夏—1905年）"],["l","p06.html","第三期 归国后直至就义（1906年—1907年）"],["l","p07.html","词选"],["l","p08.html","歌选"],["g","弹词"],["l","p09.html","精卫石"],["g","附录"],["l","p10.html","秋瑾年谱简编"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
