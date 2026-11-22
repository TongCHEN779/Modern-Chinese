(function(){var D=[["l","p01.html","总主编序"],["l","p02.html","作者简介"],["l","p03.html","历史年表"],["l","p04.html","导言"],["l","p05.html","第一章 从莱布尼茨到康德"],["l","p06.html","第二章 康德的哥白尼式革命"],["l","p07.html","第三章 康德的道德哲学和政治哲学"],["l","p08.html","第四章 康德：《判断力批判》"],["l","p09.html","第五章 耶拿时期的费希特与谢林"],["l","p10.html","第六章 黑格尔的精神现象学"],["l","p11.html","第七章 黑格尔的逻辑学与精神哲学"],["l","p12.html","第八章 黑格尔：精神与政治"],["l","p13.html","第九章 青年黑格尔派、费尔巴哈与马克思"],["l","p14.html","第十章 亚瑟·叔本华"],["l","p15.html","第十一章 克尔凯郭尔的思辨的绝望"],["l","p16.html","名词解释"],["l","p17.html","译后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
