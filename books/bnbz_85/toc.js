(function(){var D=[["l","p01.html","序"],["l","p02.html","阿垅"],["l","p03.html","鲁藜"],["l","p04.html","孙钿"],["l","p05.html","彭燕郊"],["l","p06.html","方然"],["l","p07.html","冀汸"],["l","p08.html","钟瑄"],["l","p09.html","郑思"],["l","p10.html","曾卓"],["l","p11.html","杜谷"],["l","p12.html","绿原"],["l","p13.html","胡征"],["l","p14.html","芦甸"],["l","p15.html","徐放"],["l","p16.html","牛汉"],["l","p17.html","鲁煤"],["l","p18.html","化铁"],["l","p19.html","朱健"],["l","p20.html","朱谷怀"],["l","p21.html","罗洛"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
