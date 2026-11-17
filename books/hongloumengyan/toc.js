(function(){var D=[["l","p01.html","自序"],["l","p02.html","《红楼梦》未完"],["l","p03.html","《红楼梦》插曲之一——高鹗、袭人与畹君"],["l","p04.html","初详《红楼梦》——论全抄本"],["l","p05.html","二详《红楼梦》——甲戌本与庚辰本的年份"],["l","p06.html","三详《红楼梦》——是创作不是自传"],["l","p07.html","四详《红楼梦》——改写与遗稿"],["l","p08.html","五详《红楼梦》——旧时真本"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
