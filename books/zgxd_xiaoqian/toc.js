(function(){var D=[["l","p01.html","自序"],["g","短篇小说"],["l","p02.html","篱下"],["l","p03.html","矮檐"],["l","p04.html","落日"],["l","p05.html","雨夕"],["l","p06.html","邮票"],["l","p07.html","栗子"],["l","p08.html","皈依"],["l","p09.html","蚕"],["l","p10.html","邓山东"],["g","散文特写"],["l","p11.html","草原即景"],["l","p12.html","南德的暮秋"],["l","p13.html","美国散记"],["l","p14.html","伦敦三日记"],["l","p15.html","血肉筑成的滇缅路"],["l","p16.html","刘粹刚之死"],["l","p17.html","雁荡行"],["l","p18.html","流民图"],["g","资料部分"],["l","p19.html","萧乾的生平与创作"],["l","p20.html","浅读萧乾的散文特写"],["l","p21.html","萧乾年表简编"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
