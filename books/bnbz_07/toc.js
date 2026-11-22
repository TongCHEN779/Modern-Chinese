(function(){var D=[["l","p01.html","序诗"],["g","第一辑"],["l","p02.html","女神之再生"],["l","p03.html","湘累"],["l","p04.html","棠棣之花"],["g","第二辑"],["l","p05.html","凤凰涅槃之什"],["l","p06.html","泛神论者之什"],["l","p07.html","太阳礼赞之什"],["g","第三辑"],["l","p08.html","爱神之什"],["l","p09.html","春蚕之什"],["l","p10.html","归国吟"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
