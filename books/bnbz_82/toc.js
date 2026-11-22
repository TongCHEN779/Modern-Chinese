(function(){var D=[["l","p01.html","一九五四年"],["l","p02.html","一九五五年"],["l","p03.html","一九五六年"],["l","p04.html","一九五七年"],["l","p05.html","一九五八年"],["l","p06.html","一九五九年"],["l","p07.html","一九六〇年"],["l","p08.html","一九六一年"],["l","p09.html","一九六二年"],["l","p10.html","一九六三年"],["l","p11.html","一九六四年"],["l","p12.html","一九六五年"],["l","p13.html","一九六六年"],["l","p14.html","附录1 赤子之心——傅聪谈傅雷"],["l","p15.html","附录2 范用与《傅雷家书》"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
