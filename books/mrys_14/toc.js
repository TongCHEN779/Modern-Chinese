(function(){var D=[["l","p01.html","《中国名人轶事丛书》出版缘由"],["l","p02.html","主编絮语"],["l","p03.html","第一章 塞上绝唱"],["l","p04.html","第二章 暗箭难防"],["l","p05.html","第三章 送你一具尸体"],["l","p06.html","第四章 巧解燃眉急"],["l","p07.html","第五章 天清寺奇遇"],["l","p08.html","第六章 金殿争斗"],["l","p09.html","第七章 密谋暗害"],["l","p10.html","第八章 妹喜兄悲"],["l","p11.html","第九章 岳州赴任"],["l","p12.html","第十章 马儿三条腿"],["l","p13.html","第十一章 严冬蛰伏"],["l","p14.html","第十二章 相府私宴"],["l","p15.html","第十三章 过河卒子"],["l","p16.html","第十四章 泪洒鸳鸯枕"],["l","p17.html","第十五章 左右为难"],["l","p18.html","第十六章 伴君如伴虎"],["l","p19.html","第十七章 不了情"],["l","p20.html","第十八章 虎口余生"],["l","p21.html","第十九章 谪贬出京"],["l","p22.html","第二十章 火起后院"],["l","p23.html","第二十一章 愁泛孤舟"],["l","p24.html","第二十二章 碧波情深"],["l","p25.html","第二十三章 可怜天下父母心"],["l","p26.html","第二十四章 江流不息"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
