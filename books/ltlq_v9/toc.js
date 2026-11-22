(function(){var D=[["l","p01.html","总主编序"],["l","p02.html","作者简介"],["l","p03.html","致谢"],["l","p04.html","历史年表"],["l","p05.html","导言"],["l","p06.html","第一章 逻辑哲学"],["l","p07.html","第二章 20世纪的数学哲学"],["l","p08.html","第三章 弗雷格"],["l","p09.html","第四章 维特根斯坦的《逻辑哲学论》"],["l","p10.html","第五章 逻辑实证主义"],["l","p11.html","第六章 物理学哲学"],["l","p12.html","第七章 今天的科学哲学"],["l","p13.html","第八章 机运、原因和行为：概率论和人类行为的解释"],["l","p14.html","第九章 控制论"],["l","p15.html","第十章 笛卡尔的遗产：机械论与活力论之争"],["l","p16.html","名词解释"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
