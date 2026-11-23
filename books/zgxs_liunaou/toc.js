(function(){var D=[["l","p01.html","前言"],["g","刘呐鸥小说经典"],["l","p02.html","游戏"],["l","p03.html","风景"],["l","p04.html","流"],["l","p05.html","热情之骨"],["l","p06.html","两个时间的不感症者"],["l","p07.html","礼仪和卫生"],["l","p08.html","残留"],["l","p09.html","方程式"],["g","章衣萍小说经典"],["l","p10.html","桃色的衣裳"],["l","p11.html","第一个恋人"],["l","p12.html","爱丽"],["l","p13.html","阿莲"],["l","p14.html","松萝山下"],["l","p15.html","你教我怎么办呢"],["l","p16.html","痴恋日记"],["l","p17.html","夜遇"],["l","p18.html","红迹"],["l","p19.html","给璐子的信"],["l","p20.html","从你走后"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
