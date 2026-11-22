(function(){var D=[["l","p01.html","一个戴水獭皮帽子的朋友"],["l","p02.html","桃源与沅州"],["l","p03.html","鸭窠围的夜"],["l","p04.html","一九三四年一月十八"],["l","p05.html","一个多情水手与一个多情妇人"],["l","p06.html","辰河小船上的水手"],["l","p07.html","箱子岩"],["l","p08.html","五个军官与一个煤矿工人"],["l","p09.html","老伴"],["l","p10.html","虎雏再遇记"],["l","p11.html","一个爱惜鼻子的朋友"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
