(function(){var D=[["l","p01.html","总主编序"],["l","p02.html","作者简介"],["l","p03.html","历史年表"],["l","p04.html","文献来源"],["l","p05.html","导言"],["l","p06.html","第一章 城邦及其文化"],["l","p07.html","第二章 伊奥尼亚学派"],["l","p08.html","第三章 赫拉克利特"],["l","p09.html","第四章 毕达哥拉斯学派和埃利亚学派"],["l","p10.html","第五章 恩培多克勒"],["l","p11.html","第六章 阿那克萨戈拉与原子论者"],["l","p12.html","第七章 智者派"],["l","p13.html","第八章 希腊的算术、几何与和声学：从泰勒斯到柏拉图"],["l","p14.html","第九章 苏格拉底与道德哲学的发端"],["l","p15.html","第十章 柏拉图：形而上学与认识论"],["l","p16.html","第十一章 柏拉图：伦理学与政治学"],["l","p17.html","第十二章 柏拉图：美学与心理学"],["l","p18.html","名词解释"],["l","p19.html","译后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
