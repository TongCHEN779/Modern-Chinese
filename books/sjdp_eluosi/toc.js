(function(){var D=[["g","序言"],["l","p01.html","总序"],["l","p02.html","编选者序"],["g","卡拉姆辛"],["l","p03.html","可怜的丽莎"],["g","普希金"],["l","p04.html","驿站长"],["l","p05.html","乔装村姑的小姐"],["g","果戈理"],["l","p06.html","五月之夜，又名女落水鬼"],["l","p07.html","鼻子"],["g","莱蒙托夫"],["l","p08.html","塔曼"],["g","屠格涅夫"],["l","p09.html","白净草场"],["l","p10.html","哞哞"],["g","列夫·托尔斯泰"],["l","p11.html","三死"],["l","p12.html","舞会之后"],["g","陀思妥耶夫斯基"],["l","p13.html","一位柔弱的女子（虚构的故事）"],["l","p14.html","一个可笑人的梦（虚构的故事）"],["g","迦尔洵"],["l","p15.html","红花"],["g","契诃夫"],["l","p16.html","一个官吏之死"],["l","p17.html","悲伤"],["g","列斯科夫"],["l","p18.html","珍珠项链"],["g","柯罗连科"],["l","p19.html","马卡尔的梦（圣诞节故事）"],["g","高尔基"],["l","p20.html","马卡尔·楚德拉"],["l","p21.html","女人"],["g","蒲宁"],["l","p22.html","安东诺夫卡苹果"],["l","p23.html","在巴黎"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
