(function(){var D=[["l","p01.html","《中国名人轶事丛书》出版缘由"],["l","p02.html","主编絮语"],["l","p03.html","楔子"],["l","p04.html","第一章 风云突变"],["l","p05.html","第二章 山雨欲来"],["l","p06.html","第三章 受命危急"],["l","p07.html","第四章 情寄边关"],["l","p08.html","第五章 逃卒乱宫"],["l","p09.html","第六章 慎渡艰危"],["l","p10.html","第七章 感遇知音"],["l","p11.html","第八章 义无反顾"],["l","p12.html","第九章 宦途多难"],["l","p13.html","第十章 烽火再举"],["l","p14.html","第十一章 横遭谗言"],["l","p15.html","第十二章 激流勇进"],["l","p16.html","第十三章 凄风苦雨"],["l","p17.html","第十四章 雪上加霜"],["l","p18.html","第十五章 乡情依依"],["l","p19.html","第十六章 龃龉暗生"],["l","p20.html","第十七章 精谋细划"],["l","p21.html","第十八章 鞠躬尽瘁"],["l","p22.html","尾声"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
