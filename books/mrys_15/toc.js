(function(){var D=[["l","p01.html","《中国名人轶事丛书》出版缘由"],["l","p02.html","主编絮语"],["l","p03.html","诗词金石珠联璧合　芝芙草拔千古美谈"],["l","p04.html","元宵夜谈古论今　相国寺脱衣市易"],["l","p05.html","人间父女恩情重　忧时伤世感慨多"],["l","p06.html","汴京城中风波恶　青州故里花月鲜"],["l","p07.html","独处深闺相思苦　赌茶金石别样甜"],["l","p08.html","泪湿罗衣脂粉满　一番风露晓妆新"],["l","p09.html","载书千里不辞远　但愁人客建康城"],["l","p10.html","项羽乌江长歌当哭　星河天帝瑰丽词成"],["l","p11.html","草际鸣蛩梧桐惊落　坚城自堕杞妇悲深"],["l","p12.html","巧取难逃万世讥　妙词能夺千秋赞"],["l","p13.html","驵侩下才腹藏剑　囹圄九日才女悲"],["l","p14.html","女中自有嵇中散　《后序》光耀千古文"],["l","p15.html","打马图中寄壮志　八咏楼上泄哀思"],["l","p16.html","和议声嚣乡愁愈烈　英雄赴难再写乌江"],["l","p17.html","孤山梅林但余双泪　落日镕金漱玉集成"],["l","p18.html","后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
