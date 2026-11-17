(function(){var D=[["l","p01.html","前言"],["l","p02.html","夏桀"],["l","p03.html","殷纣王"],["l","p04.html","周幽王宫涅"],["l","p05.html","吴王夫差"],["l","p06.html","燕王喜和太子丹"],["l","p07.html","秦二世胡亥"],["l","p08.html","汉平帝与王莽"],["l","p09.html","东汉献帝刘协"],["l","p10.html","蜀汉后主刘禅"],["l","p11.html","东吴孙皓"],["l","p12.html","南朝陈后主叔宝"],["l","p13.html","隋炀帝杨广"],["l","p14.html","唐昭宗李晔和哀帝李祝"],["l","p15.html","南唐后主李煜"],["l","p16.html","北宋徽宗赵佶"],["l","p17.html","南宋恭帝赵㬎"],["l","p18.html","辽朝天祚皇帝耶律延禧"],["l","p19.html","金哀宗完颜守绪"],["l","p20.html","元顺帝妥欢贴睦尔"],["l","p21.html","明崇祯帝朱由检"],["l","p22.html","清宣统皇帝溥仪"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
