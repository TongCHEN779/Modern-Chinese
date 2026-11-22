(function(){var D=[["l","p01.html","小引"],["l","p02.html","第一辑：给战斗者及其它"],["l","p03.html","第二辑：荣誉战士及其它"],["l","p04.html","第三辑：街头诗一束"],["l","p05.html","第四辑：小叙事诗一束"],["l","p06.html","第五辑：《祝山》外一篇"],["l","p07.html","第六辑：我底田园"],["l","p08.html","第七辑：她底歌（原名《她也要杀人》）"],["l","p09.html","写在《给战斗者》的末页"],["l","p10.html","《给战斗者》写作前后"],["l","p11.html","二〇〇〇年跋"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
