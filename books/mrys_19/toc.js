(function(){var D=[["l","p01.html","《中国名人轶事丛书》出版缘由"],["l","p02.html","主编絮语"],["l","p03.html","飞熊降世"],["l","p04.html","中年悟道"],["l","p05.html","奉命下山"],["l","p06.html","重访旧友"],["l","p07.html","白发新郎"],["l","p08.html","市廛贩夫"],["l","p09.html","花园收妖"],["l","p10.html","朝歌卜卦"],["l","p11.html","火烧琵琶精"],["l","p12.html","木剑诛妖"],["l","p13.html","金殿辞官"],["l","p14.html","磻溪归隐"],["l","p15.html","八十遇文王"],["l","p16.html","捉放晁雷"],["l","p17.html","冰冻岐山"],["l","p18.html","迷兵困闻仲"],["l","p19.html","智擒土行孙"],["l","p20.html","计赚邓九公"],["l","p21.html","豆兵惑瘟神"],["l","p22.html","念珠锁大鹏"],["l","p23.html","岐山犁殷郊"],["l","p24.html","金台拜将"],["l","p25.html","金鸡岭上逗孔雀"],["l","p26.html","将计就计取汜水"],["l","p27.html","临潼关策反"],["l","p28.html","刨根问柢伏门神"],["l","p29.html","怒焚妲己"],["l","p30.html","马前泼水"],["l","p31.html","后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
