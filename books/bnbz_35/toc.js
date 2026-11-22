(function(){var D=[["l","p01.html","自序"],["g","上海屋檐下"],["l","p02.html","人物"],["l","p03.html","第一幕"],["l","p04.html","第二幕"],["l","p05.html","第三幕"],["l","p06.html","后记"],["l","p07.html","谈《上海屋檐下》的创作"],["g","补录　芳草天涯"],["l","p08.html","芳草天涯　人物"],["l","p09.html","芳草天涯　第一幕"],["l","p10.html","芳草天涯　第二幕"],["l","p11.html","芳草天涯　第三幕"],["l","p12.html","芳草天涯　第四幕"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
