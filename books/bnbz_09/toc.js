(function(){var D=[["l","p01.html","序"],["l","p02.html","狂人日记"],["l","p03.html","孔乙己"],["l","p04.html","药"],["l","p05.html","明天"],["l","p06.html","一件小事"],["l","p07.html","头发的故事"],["l","p08.html","风波"],["l","p09.html","故乡"],["l","p10.html","阿Q正传"],["l","p11.html","端午节"],["l","p12.html","白光"],["l","p13.html","兔和猫"],["l","p14.html","鸭的喜剧"],["l","p15.html","社戏"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
