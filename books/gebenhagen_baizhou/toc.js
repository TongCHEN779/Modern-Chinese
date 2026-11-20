(function(){var D=[["g","第一部分"],["l","p01.html","1"],["l","p02.html","2"],["l","p03.html","3"],["l","p04.html","4"],["l","p05.html","5"],["l","p06.html","6"],["l","p07.html","7"],["l","p08.html","8"],["l","p09.html","9"],["l","p10.html","10"],["l","p11.html","11"],["l","p12.html","12"],["g","第二部分"],["l","p13.html","1"],["l","p14.html","2"],["l","p15.html","3"],["l","p16.html","4"],["l","p17.html","5"],["l","p18.html","6"],["l","p19.html","7"],["l","p20.html","8"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
