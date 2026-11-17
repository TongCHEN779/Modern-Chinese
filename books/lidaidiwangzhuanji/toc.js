(function(){var D=[["l","p01.html","编者的话"],["l","p02.html","秦始皇"],["l","p03.html","汉高祖刘邦"],["l","p04.html","汉文帝"],["l","p05.html","汉武帝"],["l","p06.html","汉光武帝"],["l","p07.html","魏孝文帝"],["l","p08.html","唐太宗"],["l","p09.html","周世宗"],["l","p10.html","宋太祖"],["l","p11.html","元世祖忽必烈"],["l","p12.html","朱元璋"],["l","p13.html","努尔哈赤"],["l","p14.html","康熙皇帝"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
