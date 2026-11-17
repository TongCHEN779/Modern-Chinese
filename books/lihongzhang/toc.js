(function(){var D=[["l","p01.html","序例"],["l","p02.html","第一章 绪论"],["l","p03.html","第二章 李鸿章所处的历史位置"],["l","p04.html","第三章 李鸿章未发达以前及当时中国的形势"],["l","p05.html","第四章 军事家李鸿章（上）"],["l","p06.html","第五章 军事家李鸿章（下）"],["l","p07.html","第六章 洋务运动时期的李鸿章"],["l","p08.html","第七章 中日甲午战争时期的李鸿章"],["l","p09.html","第八章 外交家李鸿章（上）"],["l","p10.html","第九章 外交家李鸿章（下）"],["l","p11.html","第十章 赋闲时期的李鸿章"],["l","p12.html","第十一章 李鸿章的末路"],["l","p13.html","第十二章 结论"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
