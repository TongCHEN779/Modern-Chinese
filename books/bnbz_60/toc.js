(function(){var D=[["l","p01.html","序"],["l","p02.html","一 应该怎样唱呀？"],["l","p03.html","二 在阿着底地方"],["l","p04.html","三 天空闪出一朵花"],["l","p05.html","四 成长"],["l","p06.html","五 说媒"],["l","p07.html","六 抢亲"],["l","p08.html","七 盼望"],["l","p09.html","八 哥哥阿黑回来了"],["l","p10.html","九 马铃响来玉鸟叫"],["l","p11.html","十 比赛"],["l","p12.html","十一 打虎"],["l","p13.html","十二 射箭"],["l","p14.html","十三 回声"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
