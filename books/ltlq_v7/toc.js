(function(){var D=[["l","p01.html","总主编序"],["l","p02.html","致谢"],["l","p03.html","作者简介"],["l","p04.html","历史年表"],["l","p05.html","导言"],["l","p06.html","第一章 早期功利主义者：边沁和詹姆斯·密尔"],["l","p07.html","第二章 惠威尔的科学哲学与伦理哲学"],["l","p08.html","第三章 约翰·斯图尔特·密尔的伦理学和政治学"],["l","p09.html","第四章 约翰·斯图尔特·密尔的逻辑学和形而上学"],["l","p10.html","第五章 西季威克"],["l","p11.html","第六章 孔德和实证主义"],["l","p12.html","第七章 尼采"],["l","p13.html","第八章 狄尔泰"],["l","p14.html","第九章 19世纪的逻辑学和数学哲学"],["l","p15.html","第十章 19世纪的生物学哲学"],["l","p16.html","第十一章 心理学和哲学的分离：心灵科学中的研究(1815—1879)"],["l","p17.html","第十二章 美国实用主义：皮尔士"],["l","p18.html","第十三章 美国实用主义：詹姆斯"],["l","p19.html","第十四章 格林、鲍桑葵和融贯论哲学"],["l","p20.html","第十五章 布拉德雷"],["l","p21.html","名词解释"],["l","p22.html","译后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
