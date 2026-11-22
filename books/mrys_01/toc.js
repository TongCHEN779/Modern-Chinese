(function(){var D=[["l","p01.html","《中国名人轶事丛书》出版缘由"],["l","p02.html","主编絮语"],["l","p03.html","不韦弄巧 赵姬产下秦始皇"],["l","p04.html","中国一统 不韦死始皇独尊"],["l","p05.html","欣慕长生 仙人梦中告生死"],["l","p06.html","独探墓陵 武士俑慰身后寂"],["l","p07.html","两小无猜 稚秦王山盟海誓"],["l","p08.html","阵前倒戈 长安君谋反伏诛"],["l","p09.html","徐福狂言 东海仙山觅灵药"],["l","p10.html","生死相循 天子庶民总一般"],["l","p11.html","雄才大略 一举生灵尽涂炭"],["l","p12.html","浪涛震震 灭六国大展秦威"],["l","p13.html","萧萧易水 壮士血染秦王阶"],["l","p14.html","百姓之恨 声浪阵阵醒秦王"],["l","p15.html","烈女撞墓 始皇椎心难回天"],["l","p16.html","张良莽撞 孟氏女明言得失"],["l","p17.html","慈父心肠 得罪阉人是祸根"],["l","p18.html","赵高千谋 爱子情深是秦王"],["l","p19.html","千古遗恨 始皇错着满盘输"],["l","p20.html","惩恶篇"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
