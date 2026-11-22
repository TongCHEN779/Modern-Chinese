(function(){var D=[["l","p01.html","前言"],["l","p02.html","第一章 赵匡胤开创大宋基业"],["l","p03.html","第二章 宋太宗守内虚外"],["l","p04.html","第三章 用银绢换来的和平岁月"],["l","p05.html","第四章 维新派的强国之梦"],["l","p06.html","第五章 北宋时期的农民起义"],["l","p07.html","第六章 北宋朝廷倾覆"],["l","p08.html","第七章 南宋军民抗击外侮"],["l","p09.html","第八章 偏安江南的朝廷"],["l","p10.html","第九章 宋室覆亡"],["l","p11.html","附录一 蔚为大观的词文化"],["l","p12.html","附录二 宋代的科技与建筑"],["l","p13.html","附录三 宋朝历代皇帝年表"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
