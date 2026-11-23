(function(){var D=[["l","p01.html","编辑说明"],["l","p02.html","陈确"],["l","p03.html","黄宗羲"],["l","p04.html","方以智"],["l","p05.html","顾炎武"],["l","p06.html","王夫之"],["l","p07.html","唐甄"],["l","p08.html","颜元"],["l","p09.html","戴震"],["l","p10.html","洪亮吉"],["l","p11.html","龚自珍"],["l","p12.html","魏源"],["l","p13.html","洪秀全"],["l","p14.html","康有为"],["l","p15.html","谭嗣同"],["l","p16.html","严复"],["l","p17.html","章炳麟"],["l","p18.html","孙中山"],["l","p19.html","朱执信"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
