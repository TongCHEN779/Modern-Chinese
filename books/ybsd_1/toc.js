(function(){var D=[["l","p01.html","致中国读者"],["l","p02.html","致本书的中国读者"],["g","第一编"],["l","p03.html","序言"],["l","p04.html","第一章 俄罗斯白银时代文学——完整而复杂的体系"],["l","p05.html","第二章 白银时代的哲学和文学——贴近与交叉"],["l","p06.html","第三章 文学与其他门类的艺术"],["g","第二编"],["l","p07.html","第四章 现实主义与自然主义"],["l","p08.html","第五章 现实主义与“新现实主义”"],["l","p09.html","第六章 列夫·托尔斯泰"],["l","p10.html","第七章 安东·契诃夫"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
