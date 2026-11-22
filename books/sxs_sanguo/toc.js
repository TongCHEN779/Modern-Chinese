(function(){var D=[["l","p01.html","前言"],["l","p02.html","第一章 落日残照下的东汉王朝"],["l","p03.html","第二章 群雄割据与群雄逐鹿"],["l","p04.html","第三章 曹操、孙权和刘备的兴起"],["l","p05.html","第四章 扫平北方——谈曹魏政权的兴衰"],["l","p06.html","第五章 入主巴蜀——谈蜀汉政权的兴盛"],["l","p07.html","第六章 盘卧江东——谈东吴政权的发展"],["l","p08.html","第七章 分久必合，天下一统"],["l","p09.html","附录"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
