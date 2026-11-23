(function(){var D=[["l","p01.html","编辑说明"],["l","p02.html","古代无神论和唯物主义的萌芽"],["l","p03.html","孔子"],["l","p04.html","墨子"],["l","p05.html","杨朱"],["l","p06.html","前期法家"],["l","p07.html","宋钘尹文学派"],["l","p08.html","孙子"],["l","p09.html","孟子"],["l","p10.html","老子"],["l","p11.html","庄子"],["l","p12.html","惠施公孙龙"],["l","p13.html","后期墨家"],["l","p14.html","邹衍"],["l","p15.html","荀子"],["l","p16.html","韩非子"],["l","p17.html","周易"],["l","p18.html","礼记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
