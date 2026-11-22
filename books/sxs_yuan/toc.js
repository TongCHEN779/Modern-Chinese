(function(){var D=[["l","p01.html","前言"],["l","p02.html","第一章 成吉思汗统一蒙古"],["l","p03.html","第二章 蒙古帝国"],["l","p04.html","第三章 忽必烈建立元朝"],["l","p05.html","第四章 挥鞭南宋 中华一统"],["l","p06.html","第五章 忽必烈统治时期的元朝"],["l","p07.html","第六章 元朝的中期统治"],["l","p08.html","第七章 帝国的丧钟"],["l","p09.html","附录一 元代中国与世界的关系"],["l","p10.html","附录二 元代的文化发展"],["l","p11.html","附录三 元代的科技发展"],["l","p12.html","附录四 元朝历代皇帝年表"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
