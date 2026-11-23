(function(){var D=[["l","p01.html","悼萧红（代序）"],["l","p02.html","永久的憧憬和追求"],["l","p03.html","蹲在洋车上"],["l","p04.html","家族以外的人"],["l","p05.html","失眠之夜"],["l","p06.html","王阿嫂的死"],["l","p07.html","看风筝"],["l","p08.html","夜风"],["l","p09.html","手"],["l","p10.html","王四的故事"],["l","p11.html","牛车上"],["l","p12.html","桥"],["l","p13.html","旷野的呼喊"],["l","p14.html","山下"],["l","p15.html","逃难"],["l","p16.html","朦胧的期待"],["l","p17.html","小城三月"],["l","p18.html","萧红和她的文学创作"],["l","p19.html","萧红著作编目"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
