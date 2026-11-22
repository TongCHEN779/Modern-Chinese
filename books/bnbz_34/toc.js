(function(){var D=[["l","p01.html","扇上的烟云（代序）"],["l","p02.html","墓"],["l","p03.html","秋海棠"],["l","p04.html","雨前"],["l","p05.html","黄昏"],["l","p06.html","独语"],["l","p07.html","梦后"],["l","p08.html","岩"],["l","p09.html","炉边夜话"],["l","p10.html","雾"],["l","p11.html","画梦录"],["l","p12.html","哀歌"],["l","p13.html","货郎"],["l","p14.html","魔术草"],["l","p15.html","楼"],["l","p16.html","弦"],["l","p17.html","静静的日午"],["g","附录"],["l","p18.html","梦中道路"],["l","p19.html","呜咽的扬子江"],["l","p20.html","街"],["l","p21.html","县城风光"],["l","p22.html","乡下"],["l","p23.html","我们的城堡"],["l","p24.html","私塾师"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
