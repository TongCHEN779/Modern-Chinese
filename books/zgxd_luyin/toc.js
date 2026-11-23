(function(){var D=[["l","p01.html","序　浅谈庐隐及其作品"],["g","小说"],["l","p02.html","一个著作家"],["l","p03.html","或人的悲哀"],["l","p04.html","海滨故人"],["l","p05.html","曼丽"],["l","p06.html","房东"],["l","p07.html","父亲"],["l","p08.html","胜利以后"],["l","p09.html","何处是归程"],["g","散文"],["l","p10.html","玫瑰的刺"],["l","p11.html","东京小品"],["l","p12.html","丁玲之死"],["l","p13.html","灾还不够"],["l","p14.html","屈伸自如"],["l","p15.html","监守自盗"],["l","p16.html","愧"],["l","p17.html","今后妇女的出路"],["l","p18.html","著作家应有的修养"],["l","p19.html","吹牛的妙用"],["g","资料部分"],["l","p20.html","庐隐论"],["l","p21.html","忆庐隐"],["l","p22.html","黄庐隐"],["l","p23.html","关于庐隐的回忆"],["l","p24.html","庐隐的生平与创作道路"],["l","p25.html","庐隐年表"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
