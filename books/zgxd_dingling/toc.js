(function(){var D=[["l","p01.html","为香港版选集写几句话"],["g","小说"],["l","p02.html","莎菲女士的日记"],["l","p03.html","松子"],["l","p04.html","一颗未出膛的枪弹"],["l","p05.html","我在霞村的时候"],["l","p06.html","夜"],["l","p07.html","在医院中"],["l","p08.html","杜晚香"],["g","散文"],["l","p09.html","三日杂记"],["l","p10.html","诗人应该歌颂您"],["l","p11.html","我所认识的瞿秋白同志"],["l","p12.html","一个真实人的一生"],["l","p13.html","初到密山"],["l","p14.html","“牛棚”小品（三章）"],["l","p15.html","曼哈顿街头夜景"],["l","p16.html","似无情，却有情"],["l","p17.html","我是一棵小草"],["g","资料部分"],["l","p18.html","三访汤原"],["l","p19.html","从《梦珂》到《夜》"],["l","p20.html","记老作家丁玲"],["l","p21.html","丁玲生平及著作年表"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
