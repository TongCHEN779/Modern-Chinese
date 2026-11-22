(function(){var D=[["l","p01.html","序言"],["l","p02.html","徐志摩"],["l","p03.html","闻一多"],["l","p04.html","饶孟侃"],["l","p05.html","孙大雨"],["l","p06.html","朱湘"],["l","p07.html","邵洵美"],["l","p08.html","方令孺"],["l","p09.html","林徽音"],["l","p10.html","陈梦家"],["l","p11.html","方玮德"],["l","p12.html","梁镇"],["l","p13.html","卞之琳"],["l","p14.html","俞大纲"],["l","p15.html","沈祖牟"],["l","p16.html","沈从文"],["l","p17.html","杨子惠"],["l","p18.html","朱大柟"],["l","p19.html","刘梦苇"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
