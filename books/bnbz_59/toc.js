(function(){var D=[["l","p01.html","论《保卫延安》"],["l","p02.html","第一章 延安"],["l","p03.html","第二章 蟠龙镇"],["l","p04.html","第三章 陇东高原"],["l","p05.html","第四章 大沙漠"],["l","p06.html","第五章 长城线上"],["l","p07.html","第六章 沙家店"],["l","p08.html","第七章 九里山"],["l","p09.html","第八章 天罗地网"],["l","p10.html","后记"],["l","p11.html","重印后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
