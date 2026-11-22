(function(){var D=[["l","p01.html","总主编序"],["l","p02.html","作者简介"],["l","p03.html","历史年表"],["l","p04.html","导言"],["l","p05.html","第一章 切尔伯里的赫伯特勋爵与剑桥柏拉图主义者"],["l","p06.html","第二章 科学与英国哲学：波义耳与牛顿"],["l","p07.html","第三章 洛克：知识及其限度"],["l","p08.html","第四章 洛克的政治哲学"],["l","p09.html","第五章 乔治·贝克莱"],["l","p10.html","第六章 大卫·休谟论人类知性"],["l","p11.html","第七章 休谟的道德哲学和政治哲学"],["l","p12.html","第八章 18世纪的英国伦理学家：莎夫茨伯里、巴特勒和普赖斯"],["l","p13.html","第九章 法国启蒙运动一：科学、唯物主义和决定论"],["l","p14.html","第十章 法国启蒙运动二：自然神论、道德与政治"],["l","p15.html","第十一章 苏格兰启蒙运动"],["l","p16.html","第十二章 德国启蒙运动与英国哲学"],["l","p17.html","第十三章 詹巴蒂斯塔·维科"],["l","p18.html","第十四章 卢梭与柏克"],["l","p19.html","名词解释"],["l","p20.html","译后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
