(function(){var D=[["l","p01.html","人物"],["l","p02.html","序幕——雪后的黄昏，“阔人”的后花园"],["l","p03.html","第一幕——大戏园子的后台，春天晚上"],["l","p04.html","第二幕——次晚，花园里的小楼"],["l","p05.html","第三幕——第四天早晨，“戏子”的家"],["l","p06.html","尾声——二十年后，花园里的小楼，黄昏到夜晚"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
