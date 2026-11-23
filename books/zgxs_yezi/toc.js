(function(){var D=[["l","p01.html","前言"],["l","p02.html","星·第一章"],["l","p03.html","星·第二章"],["l","p04.html","星·第三章"],["l","p05.html","星·第四章"],["l","p06.html","星·第五章"],["l","p07.html","星·第六章"],["l","p08.html","丰收"],["l","p09.html","火"],["l","p10.html","电网外"],["l","p11.html","夜哨线"],["l","p12.html","杨七公公过年"],["l","p13.html","岳阳楼"],["l","p14.html","长江轮上"],["l","p15.html","古渡头"],["l","p16.html","向导"],["l","p17.html","偷莲"],["l","p18.html","鱼"],["l","p19.html","山村一夜"],["l","p20.html","湖上"],["l","p21.html","校长先生"],["l","p22.html","电车上"],["l","p23.html","刀手费"],["l","p24.html","毕业论文"],["l","p25.html","懒捐"],["l","p26.html","广告"],["l","p27.html","菱·第一章"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
