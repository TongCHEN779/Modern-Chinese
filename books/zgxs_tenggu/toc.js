(function(){var D=[["l","p01.html","前言"],["l","p02.html","银杏之果"],["l","p03.html","壁画"],["l","p04.html","乡愁"],["l","p05.html","石像的复活"],["l","p06.html","二人之间"],["l","p07.html","水汪汪的眼"],["l","p08.html","百足虫"],["l","p09.html","古董的自杀"],["l","p10.html","葬礼"],["l","p11.html","迷宫"],["l","p12.html","摩托车的鬼"],["l","p13.html","新漆的偶像"],["l","p14.html","一条狗"],["l","p15.html","旧笔尖与新笔尖"],["l","p16.html","平凡的死"],["l","p17.html","眼泪"],["l","p18.html","下层工作"],["l","p19.html","离家"],["l","p20.html","为小小者"],["l","p21.html","Post Obit（死后应验）"],["l","p22.html","逐客"],["l","p23.html","奇南香"],["l","p24.html","待期"],["l","p25.html","独轮车的遭遇"],["l","p26.html","外遇"],["l","p27.html","诀别"],["l","p28.html","丽琳"],["l","p29.html","鹅蛋脸"],["l","p30.html","做寿"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
