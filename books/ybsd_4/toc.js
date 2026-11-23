(function(){var D=[["g","第五编"],["l","p01.html","第二十九章 象征主义后文学（综述）"],["l","p02.html","第三十章 米哈伊尔·库兹明"],["l","p03.html","第三十一章 阿克梅主义"],["l","p04.html","第三十二章 尼古拉·古米廖夫"],["l","p05.html","第三十三章 未来主义"],["l","p06.html","第三十四章 维里米尔·赫列布尼科夫"],["l","p07.html","第三十五章 弗拉基米尔·马雅可夫斯基"],["l","p08.html","第三十六章 各流派与团体之外的诗人：弗拉基米尔·霍达谢维奇、戈奥尔吉·伊万诺夫、玛琳娜·茨维塔耶娃等"],["l","p09.html","第三十七章 新农民诗人与作家：尼古拉·克柳耶夫、谢尔盖·叶赛宁等"],["l","p10.html","结束语"],["l","p11.html","同心协力 架桥铺路——译后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
