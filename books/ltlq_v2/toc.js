(function(){var D=[["l","p01.html","总主编序"],["l","p02.html","作者简介"],["l","p03.html","历史年表"],["l","p04.html","文献来源"],["l","p05.html","导言"],["l","p06.html","第一章 亚里士多德的自然哲学"],["l","p07.html","第二章 亚里士多德的逻辑学和形而上学"],["l","p08.html","第三章 亚里士多德的美学和心灵哲学"],["l","p09.html","第四章 亚里士多德：伦理学与政治学"],["l","p10.html","第五章 漫步学派"],["l","p11.html","第六章 伊壁鸠鲁主义"],["l","p12.html","第七章 斯多亚派"],["l","p13.html","第八章 怀疑派"],["l","p14.html","第九章 希腊化时期的精确科学：原始文本和问题"],["l","p15.html","第十章 希腊化时期的生物学"],["l","p16.html","第十一章 新柏拉图主义"],["l","p17.html","第十二章 奥古斯丁"],["l","p18.html","名词解释"],["l","p19.html","译后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
