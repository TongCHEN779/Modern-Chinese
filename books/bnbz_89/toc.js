(function(){var D=[["g","北方的河"],["l","p01.html","北方的河"],["l","p02.html","第一章"],["l","p03.html","第二章"],["l","p04.html","第三章"],["l","p05.html","第四章"],["l","p06.html","第五章"],["g","黑骏马"],["l","p07.html","黑骏马"],["g","西省暗杀考"],["l","p08.html","西省暗杀考"],["l","p09.html","第一章"],["l","p10.html","第二章"],["l","p11.html","第三章"],["l","p12.html","第四章"],["l","p13.html","补考"],["g","黄泥小屋"],["l","p14.html","黄泥小屋"],["l","p15.html","第一章"],["l","p16.html","第二章"],["l","p17.html","第三章"],["l","p18.html","结尾"],["l","p19.html","再结尾"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
