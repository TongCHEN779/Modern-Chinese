(function(){var D=[["l","p01.html","题辞"],["l","p02.html","祝福"],["l","p03.html","在酒楼上"],["l","p04.html","幸福的家庭"],["l","p05.html","肥皂"],["l","p06.html","长明灯"],["l","p07.html","示众"],["l","p08.html","高老夫子"],["l","p09.html","孤独者"],["l","p10.html","伤逝"],["l","p11.html","弟兄"],["l","p12.html","离婚"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
