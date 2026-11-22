(function(){var D=[["l","p01.html","总主编序"],["l","p02.html","作者简介"],["l","p03.html","历史年表"],["l","p04.html","导言"],["l","p05.html","第一章 现象学的开端：胡塞尔和他的先行者"],["l","p06.html","第二章 存在哲学1：海德格尔"],["l","p07.html","第三章 存在哲学2：萨特"],["l","p08.html","第四章 存在哲学3：梅洛-庞蒂"],["l","p09.html","第五章 宗教哲学：马塞尔、雅斯贝尔斯、列维纳斯"],["l","p10.html","第六章 科学哲学：马赫、迪昂、巴什拉"],["l","p11.html","第七章 马克思主义哲学：列宁、卢卡奇、葛兰西、阿尔都塞"],["l","p12.html","第八章 批判理论：霍克海默、阿多诺、哈贝马斯"],["l","p13.html","第九章 诠释学：伽达默尔和利科"],["l","p14.html","第十章 意大利唯心主义及其后继者：金蒂莱、克罗齐及其他"],["l","p15.html","第十一章 法国结构主义及其后继者：索绪尔、列维-斯特劳斯、巴特、拉康、福柯"],["l","p16.html","第十二章 法国女权主义哲学：德·波伏娃、克里斯蒂娃、伊利格瑞、勒杜夫、西苏"],["l","p17.html","第十三章 解构和德里达"],["l","p18.html","第十四章 后现代理论：利奥塔、鲍德里亚及其他"],["l","p19.html","名词解释"],["l","p20.html","译后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
