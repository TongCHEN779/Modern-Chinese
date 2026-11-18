(function(){var D=[["l","p01.html","前言"],["l","p02.html","窦娥冤"],["l","p03.html","救风尘"],["l","p04.html","梧桐雨"],["l","p05.html","汉宫秋"],["l","p06.html","李逵负荆"],["l","p07.html","张生煮海"],["l","p08.html","秋胡戏妻"],["l","p09.html","赵氏孤儿"],["l","p10.html","魔合罗"],["l","p11.html","虎头牌"],["l","p12.html","合汗衫"],["l","p13.html","倩女离魂"],["l","p14.html","东堂老"],["l","p15.html","生金阁"],["l","p16.html","货郎旦"],["l","p17.html","陈州粜米"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
