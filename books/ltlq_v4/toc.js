(function(){var D=[["l","p01.html","总主编序"],["l","p02.html","作者简介"],["l","p03.html","历史年表"],["l","p04.html","导论"],["l","p05.html","第一章 意大利文艺复兴时期的哲学"],["l","p06.html","第二章 文艺复兴时期意大利以外的哲学"],["l","p07.html","第三章 从文艺复兴到笛卡尔的科学和数学"],["l","p08.html","第四章 弗朗西斯·培根和人的双重王国"],["l","p09.html","第五章 笛卡尔：方法论"],["l","p10.html","第六章 笛卡尔：形而上学和心灵哲学"],["l","p11.html","第七章 17世纪的唯物主义：伽森狄和霍布斯"],["l","p12.html","第八章 斯宾诺莎：形而上学与知识"],["l","p13.html","第九章 斯宾诺莎的道德和政治哲学"],["l","p14.html","第十章 偶因论"],["l","p15.html","第十一章 莱布尼兹：真理、知识与形而上学"],["l","p16.html","名词解释"],["l","p17.html","译后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
