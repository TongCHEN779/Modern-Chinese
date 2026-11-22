(function(){var D=[["l","p01.html","金锁记"],["l","p02.html","倾城之恋"],["l","p03.html","茉莉香片"],["l","p04.html","沉香屑 第一炉香"],["l","p05.html","沉香屑 第二炉香"],["l","p06.html","琉璃瓦"],["l","p07.html","心经"],["l","p08.html","年青的时候"],["l","p09.html","花凋"],["l","p10.html","封锁"],["g","原书附录"],["l","p11.html","再版的话"],["g","《传奇》增订本中增收的内容"],["l","p12.html","有几句话同读者说"],["l","p13.html","留情"],["l","p14.html","鸿鸾禧"],["l","p15.html","红玫瑰与白玫瑰"],["l","p16.html","等"],["l","p17.html","桂花蒸阿小悲秋"],["l","p18.html","中国的日夜"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
