(function(){var D=[["l","p01.html","永远的尹雪艳"],["l","p02.html","一把青"],["l","p03.html","岁除"],["l","p04.html","金大班的最后一夜"],["l","p05.html","那片血一般红的杜鹃花"],["l","p06.html","思旧赋"],["l","p07.html","梁父吟"],["l","p08.html","孤恋花"],["l","p09.html","花桥荣记"],["l","p10.html","秋思"],["l","p11.html","满天里亮晶晶的星星"],["l","p12.html","游园惊梦"],["l","p13.html","冬夜"],["l","p14.html","国葬"],["g","附录"],["l","p15.html","《谪仙记》序"],["l","p16.html","白先勇论"],["l","p17.html","白先勇笔下的女人"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
