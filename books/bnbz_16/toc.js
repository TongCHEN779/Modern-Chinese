(function(){var D=[["l","p01.html","题辞"],["l","p02.html","秋夜"],["l","p03.html","影的告别"],["l","p04.html","求乞者"],["l","p05.html","我的失恋"],["l","p06.html","复仇"],["l","p07.html","复仇（其二）"],["l","p08.html","希望"],["l","p09.html","雪"],["l","p10.html","风筝"],["l","p11.html","好的故事"],["l","p12.html","过客"],["l","p13.html","死火"],["l","p14.html","狗的驳诘"],["l","p15.html","失掉的好地狱"],["l","p16.html","墓碣文"],["l","p17.html","颓败线的颤动"],["l","p18.html","立论"],["l","p19.html","死后"],["l","p20.html","这样的战士"],["l","p21.html","聪明人和傻子和奴才"],["l","p22.html","腊叶"],["l","p23.html","淡淡的血痕中"],["l","p24.html","一觉"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
