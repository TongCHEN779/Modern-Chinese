(function(){var D=[["l","p01.html","序"],["l","p02.html","屈原：时间的焦虑"],["l","p03.html","李陵：流亡的孤独"],["l","p04.html","曹丕：乐极的哀情"],["l","p05.html","陶渊明：生死的辨正"],["l","p06.html","杜甫：生活的慰藉"],["l","p07.html","欧阳修：语言的力量"],["l","p08.html","李清照：离失的史诗"],["l","p09.html","文天祥：英雄的省思"],["l","p10.html","吴梅村：艳诗的自赎"],["l","p11.html","后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
