(function(){var D=[["l","p01.html","第一章"],["l","p02.html","第二章"],["l","p03.html","第三章"],["l","p04.html","第四章"],["l","p05.html","第五章"],["l","p06.html","第六章"],["l","p07.html","第七章"],["l","p08.html","第八章"],["l","p09.html","第九章"],["l","p10.html","第十章"],["l","p11.html","第十一章"],["l","p12.html","第十二章"],["l","p13.html","第十三章"],["l","p14.html","第十四章"],["l","p15.html","第十五章"],["l","p16.html","第十六章"],["l","p17.html","第十七章"],["l","p18.html","第十八章"],["l","p19.html","第十九章"],["l","p20.html","第二十章"],["l","p21.html","第二十一章"],["l","p22.html","第二十二章"],["l","p23.html","第二十三章"],["l","p24.html","第二十四章"],["l","p25.html","第二十五章"],["l","p26.html","第二十六章"],["l","p27.html","第二十七章"],["l","p28.html","代后记 在济南、北京《古船》讨论会上的发言"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
