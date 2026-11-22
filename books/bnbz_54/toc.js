(function(){var D=[["l","p01.html","编者的话"],["g","第一辑"],["l","p02.html","我在霞村的时候"],["l","p03.html","一个女人翻身的故事"],["l","p04.html","我的两家房东"],["l","p05.html","卫生组长"],["l","p06.html","租佃之间"],["l","p07.html","一天"],["l","p08.html","地雷阵"],["l","p09.html","荷花淀"],["l","p10.html","真假李板头"],["l","p11.html","龙"],["l","p12.html","“俺们毛主席有办法”"],["l","p13.html","陕北游击队历史故事"],["g","第二辑"],["l","p14.html","海上的遭遇"],["l","p15.html","无住地带"],["l","p16.html","窑洞阵地战"],["l","p17.html","一坛血"],["l","p18.html","八面山中"],["l","p19.html","锄草中的陈团长"],["l","p20.html","交通员"],["l","p21.html","三日杂记"],["l","p22.html","“众人原谅”"],["l","p23.html","为解决困难问题而来的"],["l","p24.html","一架机器的诞生"],["l","p25.html","草地"],["l","p26.html","诺尔曼·白求恩片断"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
