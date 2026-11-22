(function(){var D=[["l","p01.html","自序"],["l","p02.html","复仇"],["l","p03.html","老鲁"],["l","p04.html","落魄"],["l","p05.html","鸡鸭名家"],["l","p06.html","羊舍一夕"],["l","p07.html","看水"],["l","p08.html","王全"],["l","p09.html","骑兵列传"],["l","p10.html","塞下人物记"],["l","p11.html","黄油烙饼"],["l","p12.html","异秉"],["l","p13.html","受戒"],["l","p14.html","寂寞和温暖"],["l","p15.html","岁寒三友"],["l","p16.html","大淖记事"],["l","p17.html","七里茶坊"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
