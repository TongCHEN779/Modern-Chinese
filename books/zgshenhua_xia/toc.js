(function(){var D=[["l","p01.html","第一章 民族的形成及族神"],["l","p02.html","第二章 古代神话序说"],["l","p03.html","第三章 仙乡传说——仙山与归墟的信仰"],["l","p04.html","第四章 死与再生——回归与时间的信仰"],["l","p05.html","第五章 牵牛织女的传说——古代的星辰信仰"],["l","p06.html","第六章 关于石头的古代信仰与神话传说"],["l","p07.html","第七章 夸父神话——古代的幽冥信仰之一"],["l","p08.html","第八章 西王母与周穆王"],["l","p09.html","第九章 王权交替与神话转换"],["l","p10.html","第十章 黄河之水"],["l","p11.html","附录一 神话与诗"],["l","p12.html","附录二 神话研究的开拓者"],["l","p13.html","附录三 我的神话学历程"],["l","p14.html","王孝廉先生著作年表"],["l","p15.html","增订重编后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
