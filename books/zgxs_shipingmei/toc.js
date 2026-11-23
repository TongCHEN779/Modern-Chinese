(function(){var D=[["l","p01.html","前言"],["g","冯铿小说"],["l","p02.html","遇合"],["l","p03.html","友人C君"],["l","p04.html","无着落的心"],["l","p05.html","最后的出路"],["l","p06.html","重新起来"],["g","石评梅小说"],["l","p07.html","“只有梅花知此恨”"],["l","p08.html","病"],["l","p09.html","弃妇"],["l","p10.html","红鬃马"],["l","p11.html","祷告"],["l","p12.html","归来"],["l","p13.html","余辉"],["l","p14.html","白云庵"],["l","p15.html","被践踏的嫩芽"],["l","p16.html","流浪的歌者"],["l","p17.html","匹马嘶风录"],["l","p18.html","忏悔"],["l","p19.html","林楠的日记"],["l","p20.html","晚宴"],["l","p21.html","惆怅"],["l","p22.html","卸妆之夜"],["l","p23.html","冰场上"],["l","p24.html","毒蛇"],["l","p25.html","噩梦中的扮演"],["l","p26.html","偶然来临的贵妇人"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
