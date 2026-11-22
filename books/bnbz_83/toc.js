(function(){var D=[["l","p01.html","小引"],["g","干校六记"],["l","p02.html","下放记别"],["l","p03.html","凿井记劳"],["l","p04.html","学圃记闲"],["l","p05.html","“小趋”记情"],["l","p06.html","冒险记幸"],["l","p07.html","误传记妄"],["g","补录"],["l","p08.html","丙午丁未年纪事"],["l","p09.html","风狂雨骤"],["l","p10.html","颠倒过来"],["l","p11.html","一位骑士和四个妖精"],["l","p12.html","精彩的表演"],["l","p13.html","帘子和炉子"],["l","p14.html","披着狼皮的羊"],["l","p15.html","乌云的金边"],["l","p16.html","从“掺沙子”到“流亡”"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
