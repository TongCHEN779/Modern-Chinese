(function(){var D=[["l","p01.html","《中国名人轶事丛书》出版缘由"],["l","p02.html","主编絮语"],["l","p03.html","风月一枝莲"],["l","p04.html","窑中奇尸"],["l","p05.html","翻江倒海金鲤鱼"],["l","p06.html","石狮子眼中血"],["l","p07.html","玄门迷药"],["l","p08.html","冤狱怨鬼"],["l","p09.html","大破光棍党"],["l","p10.html","计审花和尚"],["l","p11.html","金钗·玉钗"],["l","p12.html","血光灾"],["l","p13.html","罗汉·乞丐"],["l","p14.html","赵王丧生龙头铡"],["l","p15.html","梦冤"],["l","p16.html","兔子戴帽"],["l","p17.html","绣花鞋"],["l","p18.html","灵龟"],["l","p19.html","假金钗，破奇案"],["l","p20.html","观音·黑龙·秀才"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
