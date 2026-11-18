(function(){var D=[["l","p01.html","诗人杜甫（代前言）"],["l","p02.html","例言"],["l","p03.html","第一期读书游历时期"],["l","p04.html","第二期困守长安时期"],["l","p05.html","第三期陷安史叛军中、为官时期"],["l","p06.html","第四期漂泊西南时期"],["g","附录《杜甫诗选注》批注"],["l","p07.html","批注辑录说明"],["l","p08.html","正文中批注·第一期读书游历时期"],["l","p09.html","正文中批注·第二期困守长安时期"],["l","p10.html","正文中批注·第三期陷安史叛军中、为官时期"],["l","p11.html","正文中批注·第四期漂泊西南时期"],["l","p12.html","封页等处批注"],["l","p13.html","附记"],["l","p14.html","后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
