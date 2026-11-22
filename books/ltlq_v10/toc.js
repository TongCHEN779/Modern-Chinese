(function(){var D=[["l","p01.html","总主编序"],["l","p02.html","作者简介"],["l","p03.html","历史年表"],["l","p04.html","导言"],["l","p05.html","第一章 语言哲学"],["l","p06.html","第二章 语言哲学的形式化工作"],["l","p07.html","第三章 形而上学Ⅰ（1900—1945）"],["l","p08.html","第四章 形而上学Ⅱ（1945—）"],["l","p09.html","第五章 伦理学Ⅰ（1900—1945）"],["l","p10.html","第六章 伦理学Ⅱ（1945—）"],["l","p11.html","第七章 知识论"],["l","p12.html","第八章 维特根斯坦的后期哲学"],["l","p13.html","第九章 政治哲学"],["l","p14.html","第十章 女性主义哲学"],["l","p15.html","第十一章 法哲学"],["l","p16.html","第十二章 应用伦理学"],["l","p17.html","第十三章 美学"],["l","p18.html","第十四章 宗教哲学"],["l","p19.html","名词解释"],["l","p20.html","译后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
