(function(){var D=[["l","p01.html","一"],["l","p02.html","二"],["l","p03.html","三"],["l","p04.html","四"],["l","p05.html","五"],["l","p06.html","六"],["l","p07.html","七"],["l","p08.html","八"],["l","p09.html","九"],["l","p10.html","十"],["l","p11.html","十一"],["l","p12.html","十二"],["l","p13.html","十三"],["l","p14.html","十四"],["l","p15.html","十五"],["l","p16.html","十六"],["l","p17.html","十七"],["l","p18.html","十八"],["l","p19.html","十九"],["l","p20.html","二十"],["l","p21.html","二十一"],["l","p22.html","二十二"],["l","p23.html","二十三"],["l","p24.html","二十四"],["l","p25.html","二十五"],["l","p26.html","二十六"],["l","p27.html","二十七"],["l","p28.html","二十八"],["l","p29.html","二十九"],["l","p30.html","三十"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
