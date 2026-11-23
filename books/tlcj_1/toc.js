(function(){var D=[["l","p01.html","译者前言"],["l","p02.html","前言"],["l","p03.html","致谢"],["l","p04.html","第一章 家庭和学校"],["l","p05.html","第二章 追求理想"],["l","p06.html","第三章 在历史的大门口"],["l","p07.html","第四章 智力合作关系"],["l","p08.html","第五章 1905年的托洛茨基"],["l","p09.html","第六章 “不断革命论”"],["l","p10.html","第七章 沉闷的年代：1907—1914"],["l","p11.html","第八章 大战与国际"],["l","p12.html","第九章 十月革命中的托洛茨基"],["l","p13.html","第十章 人民委员"],["l","p14.html","第十一章 布列斯特—里托夫斯克的戏剧性事件"],["l","p15.html","第十二章 武装共和国"],["l","p16.html","第十三章 革命与征服"],["l","p17.html","托洛茨基军事思想评论"],["l","p18.html","第十四章 胜利中的失败"],["l","p19.html","参考书目"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
