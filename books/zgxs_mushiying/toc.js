(function(){var D=[["l","p01.html","前言"],["l","p02.html","黑旋风"],["l","p03.html","咱们的世界"],["l","p04.html","南北极"],["l","p05.html","手指"],["l","p06.html","生活在海上的人们"],["l","p07.html","油布"],["l","p08.html","田舍风景"],["l","p09.html","Craven“A”"],["l","p10.html","公墓"],["l","p11.html","偷面包的面包师"],["l","p12.html","断了条胳膊的人"],["l","p13.html","被当作消遣品的男子"],["l","p14.html","莲花落"],["l","p15.html","夜总会里的五个人"],["l","p16.html","夜"],["l","p17.html","上海的狐步舞（一个断片）"],["l","p18.html","黑牡丹"],["l","p19.html","圣处女的感情"],["l","p20.html","某夫人"],["l","p21.html","玲子"],["l","p22.html","骆驼·尼采主义者与女人"],["l","p23.html","烟"],["l","p24.html","贫士日记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
