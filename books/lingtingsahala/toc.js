(function(){var D=[["l","p01.html","序言"],["l","p02.html","走不完的心路"],["l","p03.html","自序"],["l","p04.html","童色载一段悠悠华彩岁月光泽"],["l","p05.html","少女投身一个单纯的梦想"],["l","p06.html","色彩最沉默的生命力"],["l","p07.html","远方去奔赴一场盛大的生命"],["l","p08.html","梦乡在撒哈拉收集浪漫时光"],["l","p09.html","浪漫在浩瀚沙漠的盛大之约"],["l","p10.html","点滴刻录撒哈拉的独特记忆"],["l","p11.html","海岛奔赴一段崭新人生"],["l","p12.html","他乡万水千山都是流浪"],["l","p13.html","梦落滚滚红尘，不枉此生"],["l","p14.html","后记"],["l","p15.html","三毛年谱"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
