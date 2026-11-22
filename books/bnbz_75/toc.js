(function(){var D=[["l","p01.html","序言"],["l","p02.html","我的弟弟康雄"],["l","p03.html","家"],["l","p04.html","乡村的教师"],["l","p05.html","那么衰老的眼泪"],["l","p06.html","将军族"],["l","p07.html","一绿色之候鸟"],["l","p08.html","唐倩的喜剧"],["l","p09.html","第一件差事"],["l","p10.html","夜行货车"],["l","p11.html","上班族的一日"],["l","p12.html","山路"],["l","p13.html","赵南栋"],["l","p14.html","陈映真写作年表"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
