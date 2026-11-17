(function(){var D=[["l","p01.html","1 城里的蘑菇"],["l","p02.html","2 长椅上的假期"],["l","p03.html","3 市政府的鸽子"],["l","p04.html","4 消失在雪里的城市"],["l","p05.html","5 黄蜂疗法"],["l","p06.html","6 一个有着阳光、沙子和睡意的星期六"],["l","p07.html","7 饭盒"],["l","p08.html","8 高速公路上的森林"],["l","p09.html","9 好空气"],["l","p10.html","10 和奶牛们旅行"],["l","p11.html","11 毒兔子"],["l","p12.html","12 下错了的车站"],["l","p13.html","13 在河水更蓝的地方"],["l","p14.html","14 月亮与GNAC"],["l","p15.html","15 雨水和叶子"],["l","p16.html","16 马可瓦尔多逛超市"],["l","p17.html","17 烟、风和肥皂泡"],["l","p18.html","18 属于他一个人的城市"],["l","p19.html","19 顽固猫咪的小花园"],["l","p20.html","20 圣诞老人的孩子"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
