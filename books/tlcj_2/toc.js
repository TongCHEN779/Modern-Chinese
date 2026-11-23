(function(){var D=[["l","p01.html","前言"],["l","p02.html","第一章 权力与梦想"],["l","p03.html","第二章 革出教门"],["l","p04.html","第三章 “生活不仅仅是政治……”"],["l","p05.html","第四章 战斗间隙"],["l","p06.html","第五章 决战阶段：1926—1927年"],["l","p07.html","第六章 阿拉木图一年"],["l","p08.html","参考书目"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
