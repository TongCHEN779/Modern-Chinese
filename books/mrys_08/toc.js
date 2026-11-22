(function(){var D=[["l","p01.html","《中国名人轶事丛书》出版缘由"],["l","p02.html","主编絮语"],["l","p03.html","楔子"],["l","p04.html","第一章"],["l","p05.html","第二章"],["l","p06.html","第三章"],["l","p07.html","第四章"],["l","p08.html","第五章"],["l","p09.html","第六章"],["l","p10.html","第七章"],["l","p11.html","第八章"],["l","p12.html","第九章"],["l","p13.html","第十章"],["l","p14.html","第十一章"],["l","p15.html","第十二章"],["l","p16.html","尾声"],["l","p17.html","后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
