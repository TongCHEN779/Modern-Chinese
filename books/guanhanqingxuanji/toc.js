(function(){var D=[["l","p01.html","前言"],["g","杂剧"],["l","p02.html","感天动地窦娥冤"],["l","p03.html","赵盼儿风月救风尘"],["l","p04.html","望江亭中秋切鲙"],["l","p05.html","诈妮子调风月"],["l","p06.html","闺怨佳人拜月亭"],["l","p07.html","杜蕊娘智赏金线池"],["l","p08.html","温太真玉镜台"],["l","p09.html","钱大尹智宠谢天香"],["l","p10.html","关大王独赴单刀会"],["l","p11.html","包待制智斩鲁斋郎"],["l","p12.html","包待制三勘蝴蝶梦"],["l","p13.html","钱大尹智勘绯衣梦"],["g","散曲"],["l","p14.html","小令"],["l","p15.html","套数"],["l","p16.html","后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
