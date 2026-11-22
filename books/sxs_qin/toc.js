(function(){var D=[["l","p01.html","前言"],["l","p02.html","第一章 秦国的兴起"],["l","p03.html","第二章 秦穆公称霸春秋"],["l","p04.html","第三章 改革变法的商鞅"],["l","p05.html","第四章 合纵连横运动"],["l","p06.html","第五章 辩士与政客范雎"],["l","p07.html","第六章 商人政治家吕不韦"],["l","p08.html","第七章 嬴政独治天下"],["l","p09.html","第八章 养士之风与客卿制度"],["l","p10.html","第九章 帝王师韩非"],["l","p11.html","第十章 从九鼎迁秦到天下归一"],["l","p12.html","第十一章 中华大一统帝国的诞生"],["l","p13.html","第十二章 绝对皇权下的暴君"],["l","p14.html","第十三章 秦帝国的崩溃"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
