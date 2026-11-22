(function(){var D=[["l","p01.html","《中国名人轶事丛书》出版缘由"],["l","p02.html","主编絮语"],["l","p03.html","为酒弃官一隐士"],["l","p04.html","抛却文章做铁匠"],["l","p05.html","黄公酒炉人不俗"],["l","p06.html","才高八斗一酒仙"],["l","p07.html","才子情系鲜卑女"],["l","p08.html","为文救友向子期"],["l","p09.html","八斗不醉记山涛"],["l","p10.html","一门英烈山家后"],["l","p11.html","千里遥集两兄弟"],["l","p12.html","嵇绍血染天子衣"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
