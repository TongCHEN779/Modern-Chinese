(function(){var D=[["l","p01.html","卷前 大陆时期（1949年以前）"],["l","p02.html","卷一 台湾前期（1950—1974）"],["l","p03.html","卷二 香港时期（1975—1985）"],["l","p04.html","卷三 台湾后期（1985年—）"],["l","p05.html","“钟整个大陆的爱在一只苦瓜”——《余光中诗选》编后"],["l","p06.html","二〇〇〇年版后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
