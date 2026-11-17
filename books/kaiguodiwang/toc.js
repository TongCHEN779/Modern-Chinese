(function(){var D=[["l","p01.html","前言"],["l","p02.html","大禹和夏启"],["l","p03.html","商汤"],["l","p04.html","周文王和周武王"],["l","p05.html","秦始皇"],["l","p06.html","汉高祖刘邦"],["l","p07.html","光武帝刘秀"],["l","p08.html","曹操与曹丕"],["l","p09.html","刘备"],["l","p10.html","孙权"],["l","p11.html","司马懿与司马炎"],["l","p12.html","石勒"],["l","p13.html","苻洪与苻坚"],["l","p14.html","刘裕"],["l","p15.html","北魏道武帝拓跋珪"],["l","p16.html","北齐的创业开国者高欢和高洋"],["l","p17.html","梁武帝萧衍"],["l","p18.html","宇文泰与宇文邕"],["l","p19.html","杨坚"],["l","p20.html","李渊与李世民"],["l","p21.html","钱镠"],["l","p22.html","辽太祖耶律阿保机"],["l","p23.html","郭威"],["l","p24.html","宋太祖赵匡胤"],["l","p25.html","金太祖完颜阿骨打"],["l","p26.html","成吉思汗"],["l","p27.html","元世祖忽必烈"],["l","p28.html","朱元璋"],["l","p29.html","皇太极"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
