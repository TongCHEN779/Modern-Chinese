(function(){var D=[["l","p01.html","题记"],["g","作品部分"],["l","p02.html","航线"],["l","p03.html","祖父的故事"],["l","p04.html","人物小记"],["l","p05.html","兽道"],["l","p06.html","在祠堂里"],["l","p07.html","代理县长"],["l","p08.html","龚老法团"],["l","p09.html","联保主任的消遣"],["l","p10.html","在其香居茶馆里"],["l","p11.html","公道"],["l","p12.html","和合乡的第一场电影"],["l","p13.html","三斗小麦"],["l","p14.html","一个秋天晚上"],["l","p15.html","替身"],["l","p16.html","范老老师"],["l","p17.html","生日"],["g","资料部分"],["l","p18.html","谈谈人物的创造（节录）"],["l","p19.html","生活是创作的源泉（节录）"],["l","p20.html","《法律外的航线》（节录）"],["l","p21.html","关于沙汀的短篇小说（节录）"],["l","p22.html","论沙汀创作的现实主义特色（节录）"],["l","p23.html","沙汀创作剪影"],["l","p24.html","沙汀生平及著作年表"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
